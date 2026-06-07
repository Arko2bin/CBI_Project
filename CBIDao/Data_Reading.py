import firebase_admin
from pathlib import Path
from firebase_admin import credentials
from firebase_admin import db
import os

#extract_dic = list(os.getcwd().split("\\"))
project_directory = Path.cwd().parent
if('cbi_project' in str(project_directory).lower()):
    pass
else:
    project_directory = project_directory / 'cbi_project'

if not firebase_admin._apps:
    try:
        # 1. Handle Streamlit Cloud Environment
        if "mount" in str(project_directory):
            import streamlit as st
            firebase_info = dict(st.secrets["firebase_creds"])
            cred = credentials.Certificate(firebase_info)
            db_url = st.secrets["database"]["url"]
            print("Running on Streamlit Cloud using Secrets.")

        # 2. Handle Localhost Environment
        else:
            print("System Running in localhost")
            # Using the corrected Pathlib forward slash from your previous fix
            cred = credentials.Certificate(project_directory / '.gitignore' / 'Credentials.json')
            db_url = 'https://cbi-project-14e33-default-rtdb.firebaseio.com/'

        # 3. CRITICAL: Run the initialization for whichever environment was picked!
        firebase_admin.initialize_app(cred, {
            'databaseURL': db_url
        })

    except Exception as e:
        # Fallback security block if initialization fails unexpectedly
        print(f"Failed to initialize Firebase: {e}")
else:
    # If it already exists, use the existing active instance smoothly
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

def get_parameters():
    try:
        parameters = {}
        database = list(db.reference('/').get().keys())
        if(database is not None):
            database2 = fetch_criminal_profile(database[0])
            if(database2 is not None):
                for key,value in database2.items():
                    parameters[key] = type(value)
                return parameters
            else:
                return {"Error_Message" : "No Parameters found"}
        else:
            return {"Error_Message": "Database Empty"}

    except Exception as e:
        print("Exception at get_parameters: ",e)
