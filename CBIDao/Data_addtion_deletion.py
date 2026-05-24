import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

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