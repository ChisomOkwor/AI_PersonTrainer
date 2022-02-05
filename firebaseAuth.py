import firebase_admin
from firebase_admin import credentials, firestore, auth

from datetime import datetime


cred = credentials.Certificate('AI_PersonTrainer/firebase-sdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


def add_performance_to_db(email, workout_performance):
  doc_ref = db.collection('user-workout-performance').document(email)
  print(email)

def create_new_user():
    email = input("Please Enter your email address")
    password = input("Please Enter your password")

    user = auth.create_user(email = email, password = password)

    now = datetime.now()

    doc_ref = db.collection(email).document()
    doc_ref.set({})
    print("User sucessfully Created : {0}".format(user.uid))
