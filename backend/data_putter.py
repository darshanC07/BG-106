from firebase_admin import credentials, initialize_app, db, auth 
import os
import json
from dotenv import load_dotenv

load_dotenv()

cred = credentials.Certificate({
    "type": os.getenv("type"),
    "project_id" : os.getenv("project_id"),
    "private_key_id": os.getenv("private_key_id"),
    "private_key": os.getenv("private_key"),
    "client_email": os.getenv("client_email"),
    "client_id": os.getenv("client_id"),
    "auth_uri": os.getenv("auth_uri"),
    "token_uri": os.getenv("token_uri"),
    "auth_provider_x509_cert_url": os.getenv("auth_provider_x509_cert_url"),
    "client_x509_cert_url": os.getenv("client_x509_cert_url"),
    "universe_domain": os.getenv("universe_domain")
})

initialize_app(cred, {
    'databaseURL': os.getenv("DATABASE_URL")    
})

ref = db.reference("/")

ref.child("doctors").child("pKqeRyLKUpPS5U4bCgtw6pQvHzq2").set({
"id": "pKqeRyLKUpPS5U4bCgtw6pQvHzq2",
"name": "Asha Kapoor",
"email": "asha.kapoor@gmail.com",
"phone": "+91-9876543210",
"hospital": "City Health Clinic",
"address": "123 MG Road, Pune, Maharashtra, India",
"specialty": "Cardiology",
"license_no": "MH-123456",
"experience_years": 12,
"fee": 750,
"qualifications": "MBBS, MD (Cardiology)",
"languages": "English, Hindi, Marathi",
"bio": "Experienced cardiologist with 12 years of clinical practice specializing in heart disease management and preventive cardiology.",
"profile_picture_url": "",
"profile_visibility": "public",
"notif_pref": "All notifications",
"is_active": "true",
"created_at": "2024-08-01T10:15:30Z",
"updated_at": "2026-04-17T08:00:00Z"

})
       