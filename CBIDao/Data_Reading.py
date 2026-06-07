import firebase_admin

from firebase_admin import credentials
from firebase_admin import db
import os

extract_dic = list(os.getcwd().split("\\"))
project_directory = '\\'.join(extract_dic[:len(extract_dic)-1])

if not firebase_admin._apps:
    try:
        print(extract_dic)
        if "mount" in extract_dic:
            import streamlit as st
            # Streamlit automatically converts TOML tables into Python dictionaries!
            firebase_info = dict(st.secrets["firebase_creds"])
            cred = credentials.Certificate(firebase_info)
            db_url = st.secrets["database"]["url"]
            print("Running on Streamlit Cloud using Secrets.")
        # If it doesn't exist, initialize it normally
        else:
            print("System Running in localhost")
            cred = credentials.Certificate(f"{project_directory}\.gitignore\Credentials.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://cbi-project-14e33-default-rtdb.firebaseio.com/'  # Replace with your DB URL
            })
    except Exception as e:
        print("System Running is localhost")
        cred = credentials.Certificate(f"{project_directory}\.gitignore\Credentials.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://cbi-project-14e33-default-rtdb.firebaseio.com/'  # Replace with your DB URL
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
        data = list(db.reference('/').get().keys())
        for letter_divition in data:
            if(sample_name.lower() in letter_divition.lower()):
                return letter_divition

def get_all_criminal_names():
    try:
        data = list(db.reference('/').get().keys())
        return data
    except Exception as e:
        print("Exception at get_criminal_Name dao layer: ",e)




