import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase import firebase
from settings import FIREBASE_PATH, FIREBASE_APPLICATOIN
cred = credentials.Certificate(FIREBASE_PATH)
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()
firebase = firebase.FirebaseApplication(FIREBASE_APPLICATOIN, None)