import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from pathlib import Path

#extract_dic = list(os.getcwd().split("\\"))
project_directory = Path.cwd().parent
if('cbi_project' in str(project_directory).lower()):
    pass
else:
    project_directory = project_directory / 'cbi_project'

if not firebase_admin._apps:
    try:
        if "mount" in str(project_directory):
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

# Get a reference to the root of your database (or a specific node)
#add data
def add_criminal_profile(new_data):
    try:
        node_name = new_data['name']
        path = db.reference(f'/{node_name}')
        path.set(new_data)
        return True
    except Exception as e:
        print("Exception: ",e)
        return False

def delete_criminal_profile(node_name):
    try:
        path = db.reference(f'/{node_name}')
        path.delete()
        return True
    except Exception as e:
        print("Exception: ",e)
        return False
