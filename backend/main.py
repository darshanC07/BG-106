from flask import Flask, jsonify, request
from os import urandom, getenv
from datetime import datetime, timedelta
from flask_cors import CORS
import requests
from firebase_admin import credentials, initialize_app, db, auth
import jwt
from functools import wraps
import json

app = Flask(__name__)
app.secret_key = getenv("FLASK_SECRET_KEY", urandom(32).hex())
API_KEY = getenv("apiKey")
CORS(app, resources={r"/api/*": {"origins": "*"}},
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=True)

# Firebase Initialization
cred = credentials.Certificate({
    "type": getenv("type"),
    "project_id": getenv("project_id"),
    "private_key_id": getenv("private_key_id"),
    "private_key": getenv("private_key").replace("\\n", "\n"),
    "client_email": getenv("client_email"),
    "client_id": getenv("client_id"),
    "auth_uri": getenv("auth_uri"),
    "token_uri": getenv("token_uri"),
    "auth_provider_x509_cert_url": getenv("auth_provider_x509_cert_url"),
    "client_x509_cert_url": getenv("client_x509_cert_url"),
    "universe_domain": getenv("universe_domain")
})

initialize_app(cred, {
    "databaseURL": getenv("DATABASE_URL")
})

ref = db.reference("/")
SECRET_KEY = getenv("BACKEND_SECRET_KEY")

# ---------------- JWT ---------------- #

def generate_token(uid):
    payload = {
        "uid": uid,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["uid"]
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")

from flask import request

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.method == "OPTIONS":
            return '', 200

        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Missing token"}), 401

        if token.startswith("Bearer "):
            token = token.split(" ")[1]

        try:
            uid = verify_token(token)
            request.uid = uid
        except Exception as e:
            return jsonify({"error": str(e)}), 401

        return f(*args, **kwargs)

    return wrapper
# ---------------- ROUTES ---------------- #

@app.route("/api", methods=["GET"])
def main():
    return jsonify({"message": "Hello from backend"}), 200


@app.route("/db-status", methods=["GET"])
def db_status():
    try:
        db_msg = ref.get()
        return jsonify({"status": "Database connection successful", "response": db_msg}), 200
    except Exception as e:
        return jsonify({"status": "Database connection failed", "error": str(e)}), 500


# ---------------- REGISTER ---------------- #

@app.route("/api/doctor/auth/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = None

    try:
        user = auth.create_user(
            email=email,
            password=password
        )

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyB809K9u_NZ8bbcPDI4LAXFX7vcKHNfOUI"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        response = requests.post(url, json=payload)

        if response.status_code == 200:

            ref.child("doctors").child(user.uid).set({
                "id": user.uid,
                "name": "Asha Kapoor",
                "email": email,
                "phone": "+91-9876543210",
                "hospital": "City Health Clinic",
                "address": "123 MG Road, Pune, Maharashtra, India",
                "specialty": "Cardiology",
                "license_no": "MH-123456",
                "experience": 12,
                "fee": 750,
                "qualifications": "MBBS, MD (Cardiology)",
                "languages": "English, Hindi, Marathi",
                "bio": "Experienced cardiologist with 12 years of clinical practice specializing in heart disease management and preventive cardiology.",
                "profile_picture": "",
                "visibility": "public",
                "notification_preference": "All notifications",
                "is_active": True,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            })

            return jsonify({
                "message": "User created successfully",
                "uid": user.uid
            }), 201

        else:
            if user:
                auth.delete_user(user.uid)
            return jsonify({
                "error": "Firebase login failed",
                "details": response.text
            }), 400

    except Exception as e:
        if user:
            auth.delete_user(user.uid)
        return jsonify({"error": str(e)}), 400


# ---------------- LOGIN ---------------- #

@app.route("/api/doctor/auth/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyB809K9u_NZ8bbcPDI4LAXFX7vcKHNfOUI"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        res_data = response.json()
        uid = res_data.get("localId")

        user_info = ref.child("doctors").child(uid).get() or {}

        token = generate_token(uid)

        return jsonify({
            "message": "Doctor Login successful!",
            "code": 200,
            "token": token,
            "doctor": user_info
        })

    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/api/doctor/profile", methods=["GET"])
@require_auth
def get_profile():
    uid = request.uid
    data = ref.child("doctors").child(uid).get()
    return jsonify(data or {})


@app.route("/api/doctor/profile", methods=["PUT"])
@require_auth
def update_profile():
    uid = request.uid
    updates = request.json

    updates["updated_at"] = datetime.utcnow().isoformat()

    ref.child("doctors").child(uid).update(updates)

    return jsonify({"message": "Profile updated successfully"}), 200


# ---------------- PASSWORD ---------------- #

@app.route("/api/doctor/profile/password", methods=["PUT"])
@require_auth
def update_password():
    uid = request.uid
    data = request.json

    new_password = data.get("new_password")

    try:
        auth.update_user(uid, password=new_password)
        return jsonify({"message": "Password updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/doctor/auth/me", methods=["GET"])
@require_auth
def get_current_user():
    token = request.headers.get("Authorization")
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    try:    
        start_time = datetime.now()
        uid = verify_token(token)
        user_info = ref.child("doctors").child(uid).get() or {}
        end_time = datetime.now()
        print("response time : " + str((end_time - start_time).total_seconds()) + " seconds")
        return jsonify(user_info), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route('/api/doctor/records', methods=['GET'])
@require_auth
def get_records():
    patient_id = request.args.get('patient_id')
    record_type = request.args.get('type')
    search = request.args.get('search')
    
    start = datetime.now()
    docs = ref.child('medical_records').get()
    records = []
    
    # for doc_id,doc in docs.items():
    end = datetime.now()
    print("response time : " + str((end - start).total_seconds()) + " seconds")
    for doc_id, doc in (docs or {}).items():
        if patient_id and doc.get('patient_id') != patient_id:
            continue
        if record_type and doc.get('type') != record_type:
            continue
        if search and search.lower() not in doc.get('description', '').lower():
            continue
        records.append(doc)
        
    return jsonify({"records": records}), 200

@app.route('/upload-dummy', methods=['GET'])
def upload_dummy():
    with open('medical_records.json') as f:
        data = json.load(f)

    for record in data:
        ref.child('medical_records').push(record)

    return jsonify({"message": "Dummy data uploaded!"})

@app.route('/api/doctor/patients', methods=['GET'])
@require_auth
def get_patients():
    search = request.args.get('search', '').lower()
    
    data = ref.child('patients').get() or {}
    
    patients = []
    
    for pid, p in data.items():
        # if search and search not in p.get('name', '').lower():
        #     continue

        patients.append({
            "id": pid,
            "name": p.get("name"),
            "email": p.get("email"),
            "phone": p.get("phone"),
            "age": p.get("age"),
            "gender": p.get("gender"),
            "last_visit": p.get("last_visit"),
            "total_visits": p.get("total_visits", 0)
        })

    print(f"Fetched {len(patients)} patients from database")
    return jsonify(patients), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)