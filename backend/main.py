from flask import Flask, jsonify, request,Response
from os import urandom, getenv
from flask_cors import CORS
import requests
import json
from firebase_admin import credentials, initialize_app, db, auth 



app = Flask(__name__)
app.secret_key = getenv("FLASK_SECRET_KEY", urandom(32).hex())
API_KEY = getenv("apiKey")
CORS(app,supports_credentials=True)

cred = credentials.Certificate({
    "type": getenv("type"),
    "project_id" : getenv("project_id"),
    "private_key_id": getenv("private_key_id"),
    "private_key": getenv("private_key"),
    "client_email": getenv("client_email"),
    "client_id": getenv("client_id"),
    "auth_uri": getenv("auth_uri"),
    "token_uri": getenv("token_uri"),
    "auth_provider_x509_cert_url": getenv("auth_provider_x509_cert_url"),
    "client_x509_cert_url": getenv("client_x509_cert_url"),
    "universe_domain": getenv("universe_domain")
})

initialize_app(cred, {
    'databaseURL': getenv("DATABASE_URL")
})
ref = db.reference("/")


@app.route("/", methods=["GET"])
def main():
    return jsonify({"message": "Hello from backend"}), 200

@app.route("/db-status", methods=["GET"])
def db_status():
    try:
        db_msg = ref.get()
        return jsonify({"status": "Database connection successful", "response" : db_msg}), 200
    except Exception as e:
        return jsonify({"status": "Database connection failed", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)