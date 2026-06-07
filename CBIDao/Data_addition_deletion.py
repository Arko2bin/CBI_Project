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
