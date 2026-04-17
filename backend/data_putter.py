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

# ref.child("doctors").child("pKqeRyLKUpPS5U4bCgtw6pQvHzq2").set({
# "id": "pKqeRyLKUpPS5U4bCgtw6pQvHzq2",
# "name": "Asha Kapoor",
# "email": "asha.kapoor@gmail.com",
# "phone": "+91-9876543210",
# "hospital": "City Health Clinic",
# "address": "123 MG Road, Pune, Maharashtra, India",
# "specialty": "Cardiology",
# "license_no": "MH-123456",
# "experience_years": 12,
# "fee": 750,
# "qualifications": "MBBS, MD (Cardiology)",
# "languages": "English, Hindi, Marathi",
# "bio": "Experienced cardiologist with 12 years of clinical practice specializing in heart disease management and preventive cardiology.",
# "profile_picture_url": "",
# "profile_visibility": "public",
# "notif_pref": "All notifications",
# "is_active": "true",
# "created_at": "2024-08-01T10:15:30Z",
# "updated_at": "2026-04-17T08:00:00Z"

# })


data = [
    {
      "patient_id": "101",
      "patient_name": "Rahul Sharma",
      "appointment_id": "201",
      "diagnosis": "Hypertension",

      "medicines": [
        {
          "name": "Amlodipine",
          "dosage": "5mg",
          "frequency": "Once daily",
          "duration": "30 days"
        },
        {
          "name": "Losartan",
          "dosage": "50mg",
          "frequency": "Once daily",
          "duration": "30 days"
        }
      ],

      "instructions": "Take medicines after meals. Reduce salt intake.",
      "date": "2026-04-10",
      "valid_until": "2026-05-10",
      "status": "active"
    },

    {
      "patient_id": "102",
      "patient_name": "Priya Mehta",
      "appointment_id": "-OqPmA83dLvm7O6luBuw",
      "diagnosis": "Viral Fever",

      "medicines": [
        {
          "name": "Paracetamol",
          "dosage": "500mg",
          "frequency": "Thrice daily",
          "duration": "5 days"
        },
        {
          "name": "Cetirizine",
          "dosage": "10mg",
          "frequency": "At bedtime",
          "duration": "3 days"
        }
      ],

      "instructions": "Stay hydrated. Take rest.",
      "date": "2026-04-12",
      "valid_until": "2026-05-12",
      "status": "active"
    },

    {
      "patient_id": "101",
      "patient_name": "Rahul Sharma",
      "appointment_id": "-OqPm9xInKOPqFMIL2ps",
      "diagnosis": "Migraine",

      "medicines": [
        {
          "name": "Sumatriptan",
          "dosage": "50mg",
          "frequency": "As needed",
          "duration": "10 days"
        }
      ],

      "instructions": "Avoid bright light and stress.",
      "date": "2026-03-20",
      "valid_until": "2026-04-20",
      "status": "expired"
    }
  ]

# for idx, record in enumerate(data):
#     ref.child('prescriptions').push(record)
    
       
       
       

appointment_data = [
    {
      "patient_id": "101",
      "patient_name": "Rahul Sharma",
      "patient_phone": "9876543210",

      "date": "2026-04-18",
      "time": "10:30",
      "consultation_type": "In-clinic",
      "reason": "Headache",

      "status": "pending",
      "notes": "",
      "created_at": "2026-04-17T10:00:00"
    },{
      "patient_id": "102",
      "patient_name": "Priya Mehta",
      "patient_phone": "9123456780",

      "date": "2026-04-18",
      "time": "12:00",
      "consultation_type": "Video",
      "reason": "Fever",

      "status": "confirmed",
      "notes": "",
      "created_at": "2026-04-16T09:30:00"
    },{
      "patient_id": "101",
      "patient_name": "Rahul Sharma",
      "patient_phone": "9876543210",

      "date": "2026-04-15",
      "time": "15:00",
      "consultation_type": "In-clinic",
      "reason": "Back pain",

      "status": "completed",
      "notes": "Prescribed medicines",
      "created_at": "2026-04-14T11:00:00"
    },{
      "patient_id": "103",
      "patient_name": "Neha Kapoor",
      "patient_phone": "9012345678",

      "date": "2026-04-14",
      "time": "17:30",
      "consultation_type": "Video",
      "reason": "Skin allergy",

      "status": "cancelled",
      "cancel_reason": "Patient unavailable",
      "cancelled_by": "patient",
      "notes": "",
      "created_at": "2026-04-13T14:20:00"
    }
]

# for idx, appointment in enumerate(appointment_data):
#     ref.child('appointments').push(appointment)


patients = {
    
     "101": {
      "id": "101",
      "name": "Rahul Sharma",
      "email": "rahul@example.com",
      "phone": "9876543210",
      "age": 32,
      "gender": "Male",
      "blood_group": "B+",
      "weight": 72,

      "allergies": "None",
      "conditions": "Migraine",

      "last_visit": "2026-04-15",
      "total_visits": 5,

      "appointments": [
        "-APT1",
        "-APT3"
      ],

      "prescriptions": [
        "-OqPmUx_DoQ8oqyv_EJQ"
      ],

      "records": [
        "-OqP72oUgYTbOvF_7S38"
      ]
    },

    "102": {
      "id": "102",
      "name": "Priya Mehta",
      "email": "priya@example.com",
      "phone": "9123456780",
      "age": 28,
      "gender": "Female",
      "blood_group": "A+",
      "weight": 60,

      "allergies": "Dust",
      "conditions": "None",

      "last_visit": "2026-04-12",
      "total_visits": 3,

      "appointments": [
        "-APT2"
      ],

      "prescriptions": [
        "-OqPmV2Vd68yC-Ph5QYm"
      ],

      "records": []
    },

    "105": {
      "id": "105",
      "name": "Rohit Mehta",
      "email": "rohit@example.com",
      "phone": "9012345678",
      "age": 40,
      "gender": "Male",
      "blood_group": "O+",
      "weight": 78,

      "allergies": "None",
      "conditions": "Diabetes",

      "last_visit": "2025-03-22",
      "total_visits": 2,

      "appointments": [],

      "prescriptions": [],

      "records": [
        "-OqP72oUgYTbOvF_7S38"
      ]
    }
}

for patient_id, patient in patients.items():
    ref.child('patients').child(patient_id).set(patient)