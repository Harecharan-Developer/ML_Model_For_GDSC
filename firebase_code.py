import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize Firebase
cred = credentials.Certificate("pyfirebasesdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Variables
id = 240
fish_name = "Salmone"
batch = db.batch()

