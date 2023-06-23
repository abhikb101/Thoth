import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase import firebase

cred = credentials.Certificate('')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()
firebase = firebase.FirebaseApplication('', None)