import firebase_admin
from firebase_admin import credentials, firestore, auth

cred = credentials.Certificate('AI_PersonTrainer/firebase-sdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


def create_new_user():
    email = input("Please Enter your email address")
    password = input("Please Enter your password")

    user = auth.create_user(email = email, password = password)
    print("User sucessfully Created : {0}".format(user.uid))

def authen