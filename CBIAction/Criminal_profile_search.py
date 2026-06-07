import streamlit as st
import importlib.util
from pathlib import Path
import os

extract_dic = list(os.getcwd().split("\\"))
project_directory = Path.cwd().parent
if('cbi_project' in str(project_directory).lower()):
    pass
else:
    project_directory = project_directory / 'cbi_project'

Search_Profile_Data_path = project_directory / 'CBIManager' / 'Search_Profile_Data.py'
Create_Profile_Data_path = project_directory / 'CBIManager' / 'Create_Profile_Data.py'
Delete_Profile_Data_path = project_directory / 'CBIManager' / 'Delete_Profile_Data.py'
Data_Reading_path = project_directory / 'CBIDao' / 'Data_Reading.py'


spec = importlib.util.spec_from_file_location('Manager_layer',str(Search_Profile_Data_path))
Search_Profile_Data = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Search_Profile_Data)

spec2 = importlib.util.spec_from_file_location('Manager_layer',str(Create_Profile_Data_path))
Create_Profile_Data = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(Create_Profile_Data)

spec3 = importlib.util.spec_from_file_location('Dao_layer',str(Data_Reading_path))
Data_Reading = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(Data_Reading)

spec4 = importlib.util.spec_from_file_location('Manager_layer',str(Delete_Profile_Data_path))
Delete_Profile_Data = importlib.util.module_from_spec(spec4)
spec4.loader.exec_module(Delete_Profile_Data)

st.set_page_config(page_title='Central Beureau of Investigation',layout="wide",page_icon="https://iconarchive.com/download/i87068/graphicloads/colorful-long-shadow/Cloud.ico")

hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                header {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
def create_criminal_profile():
    st.session_state.update_clicked = False
    st.session_state.delete_clicked = False
    with st.form(key='create_criminal_profile'):
        adress = st.text_input("Enter adress of criminal")
        crime_name = st.text_input("Enter Crime Name of the criminal")
        gender = st.text_input("Enter gender of the criminal")
        image = st.text_input("paste working image of the criminal")
        qualification = st.text_input("Enter qualification of the criminal")
        age = st.number_input("Enter age of the criminal",min_value=18,max_value=100)
        money_looted = st.number_input("Enter amount looted by the criminal",min_value=1)
        name = st.text_input("Enter Full Name of the criminal")
        submit_button = st.form_submit_button('Submit')
    new_profile_details = {}
    if(submit_button  and name != ""):
        new_profile_details.setdefault('Address',adress)
        new_profile_details.setdefault('Crime Name', crime_name)
        new_profile_details.setdefault('Gender', gender)
        new_profile_details.setdefault('Image', image)
        new_profile_details.setdefault('Qualification', qualification)
        new_profile_details.setdefault('age', age)
        new_profile_details.setdefault('money_looted', money_looted)
        new_profile_details.setdefault('name',name)
        result = Create_Profile_Data.add_new_criminal_details(new_profile_details)
        if(result):
            st.success("Data added successfully! ✅")
            # close form
        st.session_state.create_clicked = False
    elif(submit_button):
        st.error("U need to enter the name of the criminal to save details")

def update_criminal_profile(criminal_name):
    st.session_state.create_clicked = False
    st.session_state.delete_clicked = False
    profile_details, photo = Search_Profile_Data.search_profile_data(criminal_name)
    if (profile_details != "No Data"):
        with st.form(key="update_criminal_profile"):
            if("Address" not in list(profile_details.keys())):
                adress = st.text_input("Enter Address of the criminal")
            else:
                adress = st.text_input("Enter Address of the criminal", profile_details['Address'])
            if ("Crime Name" not in list(profile_details.keys())):
                crime_name = st.text_input("Enter Crime Details of the criminal")
            else:
                crime_name = st.text_input("Enter Crime Setails of the criminal", profile_details['Crime Name'])
            if ("Gender" not in list(profile_details.keys())):
                gender = st.text_input("Enter Gender of the criminal")
            else:
                gender = st.text_input("Enter Gender of the criminal", profile_details['Gender'])
            if ("Image" not in list(profile_details.keys())):
                image = st.text_input("paste working image of the criminal")
            else:
                image = st.text_input("paste working image of the criminal", profile_details['Image'])
            if ("Qualification" not in list(profile_details.keys())):
                qualification = st.text_input("Enter qualification of the criminal")
            else:
                qualification = st.text_input("Enter qualification of the criminal", profile_details['Qualification'])
            if ("age" not in list(profile_details.keys())):
                age = st.number_input("Enter age of the criminal", min_value=18,max_value=100)
            else:
                age = st.number_input("Enter age of the criminal", value=int(profile_details['age']), min_value=18,
                                      max_value=100)
            if ("money_looted" not in list(profile_details.keys())):
                money_looted = st.number_input("Enter amount looted by the criminal", min_value=1)
            else:
                money_looted = st.number_input("Enter amount looted by the criminal",
                                               value=int(profile_details['money_looted']), min_value=1)
            submit_button = st.form_submit_button('Submit')
            new_profile_details = {}
            if(submit_button):
                new_profile_details.setdefault('Address', adress)
                new_profile_details.setdefault('Crime Name', crime_name)
                new_profile_details.setdefault('Gender', gender)
                new_profile_details.setdefault('Image', image)
                new_profile_details.setdefault('Qualification', qualification)
                new_profile_details.setdefault('age', age)
                new_profile_details.setdefault('money_looted', money_looted)
                new_profile_details.setdefault('name', profile_details['name'])
                result = Create_Profile_Data.add_new_criminal_details(new_profile_details)
                if (result):
                    st.success("Data updated successfully! ✅")
                    # close form
                st.session_state.update_clicked = False
    else:
        st.error("No details found!")



st.header("Central Beureau of investigation")
search_clicked = False
search2_clicked = False
update_clicked = False
create_clicked = False
delete_clicked = False
if 'create_clicked' not in st.session_state:
    st.session_state.create_clicked = False
if 'delete_clicked' not in st.session_state:
    st.session_state.delete_clicked = False
if 'update_clicked' not in st.session_state:
    st.session_state.update_clicked = False

st.subheader("Create, Update, Delete Criminal Profile: ")
create,update,delete = st.columns(3)
with create:
    if st.button("Create Criminal Profile"):
        st.session_state.create_clicked = True
with delete:
    if st.button("Delete Criminal Profile"):
        st.session_state.delete_clicked = True
with update:
    if(st.button("Update Criminal Profile")):
        st.session_state.update_clicked = True

st.subheader("Search Criminal Profile")
criminal_name = st.text_input("Enter Criminal Name: ")
if(st.button("Search")):
    search_clicked = True

st.subheader("Seach Criminal Profiles by parameters")
parameter = st.text_input("Enter criminal parameters like its adress or gender: ")
if(st.button("search")):
    search2_clicked = True

if(search_clicked and criminal_name):
    profile_details,photo = Search_Profile_Data.search_profile_data(criminal_name)
    if(profile_details != "No Data"):
        st.header('Criminal Details Found')
        st.write("---")
        if(photo != 'N/A' and photo != ""):
            st.image(photo)
        else:
            st.write("No Image available of this criminal")
        st.table(profile_details)
    else:
        st.write("---")
        st.header("No Criminal Record Found")

if(search2_clicked and parameter):
    profiles = Search_Profile_Data.get_criminal_name_by_parameters(parameter)
    for elements in list(profiles.keys()):
        if "Error_Message" in elements:
            st.write("---")
            st.header(profiles[elements])
        else:
            st.header('Criminal Details Found')
            st.write("---")
            if("No Image" in elements):
                st.write("No Image available of this criminal")
                st.table(profiles[elements])
            else:
                st.image(elements)
                st.table(profiles[elements])

if st.session_state.create_clicked:
    create_criminal_profile()


if st.session_state.delete_clicked:
    st.session_state.create_clicked = False
    st.session_state.update_clicked = False
    all_profiles = Data_Reading.get_all_criminal_names()
    selected_profiles = []
    for profile in all_profiles:
        if(st.checkbox(profile,key=profile)):
            selected_profiles.append(profile)

    st.write(selected_profiles)
    # actual delete button
    if st.button("Confirm Delete"):
        result = Delete_Profile_Data.delete_criminal_profile(selected_profiles)
        if result:
            st.success("Profiles deleted successfully!")
        st.session_state.delete_clicked = False

if st.session_state.update_clicked:
    all_profiles = Data_Reading.get_all_criminal_names()
    selected_profile = st.selectbox("Choose Criminal Profile You want to update: ",all_profiles)
    if(selected_profile):
        result = update_criminal_profile(selected_profile)
        if(result):
            st.success("Profile Updated successfully!")


