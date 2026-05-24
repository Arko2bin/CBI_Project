import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os

if not firebase_admin._apps:
    # If it doesn't exist, initialize it normally
    cred = credentials.Certificate("F:\PyCharm Community Edition 2022.3.1\FastAPI_project_demo\CBIDao\Credentials.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://fastapi-project-9cde0-default-rtdb.firebaseio.com/'  # Replace with your DB URL
    })
else:
    # If it already exists, just get the existing instance
    #print("Firebase app already initialized. Using existing instance.")
    pass

def fetch_criminal_profile(profile):
    try:
        # Read Data
        data = db.reference('/').get()
        if (profile in list(data.keys())):
            record = data[f'{profile}']
            return record
        else:
            return {"Error_Message" : "No Criminal Record Found"}
    except Exception as e:
        print("Exception at Data_Reading.py: ",e)
        return e

def get_criminal_name(sample_name):
    try:
        data = list(db.reference('/').get().keys())
        for letter_divition in data:
            if(sample_name.lower() in letter_divition.lower()):
                return letter_divition
    except Exception as e:
        print("Exception at get_criminal_Name dao layer: ",e)

def get_all_criminal_names():
    try:
        data = list(db.reference('/').get().keys())
        return data
    except Exception as e:
        print("Exception at get_criminal_Name dao layer: ",e)




