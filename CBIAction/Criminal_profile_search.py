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
criminal_name = st.selectbox("Choose Criminal Name",Data_Reading.get_all_criminal_names())
if(st.button("Search")):
    search_clicked = True

st.subheader("Seach Criminal Profiles by parameters")
parameters = Data_Reading.get_parameters()
select_parameters = st.multiselect("Select all parameters",list(parameters.keys()))
submit_parameters = {}
if(select_parameters):
    for selected in select_parameters:
        data_type = parameters[selected]
        if data_type == int:
            st.markdown(f"**Filter by {selected} (Range):**")
            col1, col2 = st.columns(2)

            with col1:
                min_val = st.number_input(f"Min {selected}", value=0, key=f"min_{selected}")
            with col2:
                max_val = st.number_input(f"Max {selected}", value=100, key=f"max_{selected}")

            # Store the range as a tuple or sub-dictionary
            submit_parameters[selected] = {"min": min_val, "max": max_val}

            # Scenario B: If the field is a string/text, create a standard text input
        else:
            user_text = st.text_input(f"Enter {selected}:", key=f"text_{selected}")
            submit_parameters[selected] = user_text

if(st.button("Submit Query")):
    search2_clicked = True

st.divider()
#End of UI next will be all results

if(search_clicked and criminal_name):
    profiles,photo = Search_Profile_Data.search_profile_data(criminal_name)
    # 1. Check if the function returned an error message
    if isinstance(profiles, dict) and "Error_Message" in profiles:
        st.error(profiles["Error_Message"])

    else:
        st.success("Criminal Profile Found")
        table_rows = []

        # Create a clean header card for each person
        st.subheader(f"👤 {profiles['name']}")

        # 3. Handle the Profile Image
        image_url = profiles['Image']

        if image_url and image_url.strip() != "":
            try:
                # Renders the image at a reasonable passport-style width
                st.image(image_url, width=300)
            except Exception:
                # In case the link is broken or restricted
                st.warning("⚠️ Profile picture URL unreachable.")
        else:
            # Fallback avatar if no image exists in the database
            st.image("https://cdn-icons-png.flaticon.com/512/149/149071.png", width=300)

        # Loop through each criminal record dynamically
        for keys, details in profiles.items():

            if keys not in ["Image", "name"]:
                # Capitalize keys cleanly for UI readability (e.g., 'money_looted' -> 'Money Looted')
                clean_key = keys.replace("_", " ").title()
                table_rows.append([clean_key, details])

            # Display rows natively as a structured table with Keys in Col 1, Values in Col 2
        st.table(table_rows)

        # Add a clear section divider before rendering the next person
        st.write("###")
        st.divider()

if (search2_clicked and submit_parameters):
    profiles = Search_Profile_Data.get_criminal_name_by_parameters(submit_parameters)

    # 1. Check if the function returned an error message
    if isinstance(profiles, dict) and "Error_Message" in profiles:
        st.error(profiles["Error_Message"])

    else:
        st.success(f"Found {len(profiles)} matching records:")
        st.write("---")  # Visual separator

        # 2. Loop through each criminal record dynamically
        for profile_id, details in profiles.items():

            # Create a clean header card for each person
            st.subheader(f"👤 {details.get('name', profile_id)}")

            # 3. Handle the Profile Image
            image_url = details.get("Image", "")

            if image_url and image_url.strip() != "":
                try:
                    # Renders the image at a reasonable passport-style width
                    st.image(image_url, width=300)
                except Exception:
                    # In case the link is broken or restricted
                    st.warning("⚠️ Profile picture URL unreachable.")
            else:
                # Fallback avatar if no image exists in the database
                st.image("https://cdn-icons-png.flaticon.com/512/149/149071.png", width=300)

            # 4. Format the rest of the details into a Tabular Key-Value view
            # We filter out 'Image' and 'name' since they are already displayed above
            table_rows = []
            for key, value in details.items():
                if key not in ["Image", "name"]:
                    # Capitalize keys cleanly for UI readability (e.g., 'money_looted' -> 'Money Looted')
                    clean_key = key.replace("_", " ").title()
                    table_rows.append([clean_key, value])

            # Display rows natively as a structured table with Keys in Col 1, Values in Col 2
            st.table(table_rows)

            # Add a clear section divider before rendering the next person
            st.write("###")
            st.divider()


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


