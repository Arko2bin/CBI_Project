from fastapi import FastAPI,Path
from pathlib import Path
import importlib.util
import os

extract_dic = list(os.getcwd().split("\\"))
project_directory = Path.cwd().parent
if('cbi_project' in str(project_directory).lower()):
    print("Successfully passed if condition on env")
else:
    print("inside else")
    project_directory = project_directory / 'cbi_project'

Data_Reading_path = project_directory / 'CBIDao' / 'Data_Reading.py'
Search_Profile_Data_path = project_directory / 'CBIManager' / 'Search_Profile_Data.py'

spec = importlib.util.spec_from_file_location('Dao_layer',str(Data_Reading_path))
Data_Reading = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Data_Reading)

spec2 = importlib.util.spec_from_file_location('Manager_layer',str(Search_Profile_Data_path))
Search_Profile_Data = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(Search_Profile_Data)


app = FastAPI()

@app.get('/')
def who_we_are():
    message = "We are Central Bureau of Investigation we keep criminal records u can go to entries tab to see what data we are keeping"
    return {'message' : f'{message}'}

@app.get('/entries')
def entry():
    final_datas = []
    indexs = Data_Reading.get_all_criminal_names()
    for index in indexs:
        final_data = {
            index : Data_Reading.fetch_criminal_profile(index)
        }
        final_datas.append(final_data)
    return final_datas

@app.get('/criminal_name/{criminal_name}')
def get_criminal_details(criminal_name: str = Path(...,description="Need the Name ofthe criminal", example="Abhishek Banerjee")):
    criminal_name = Data_Reading.get_criminal_name(criminal_name)
    return Data_Reading.fetch_criminal_profile(criminal_name)

@app.get('/criminal_details/{address}')
def get_criminal_details(address: str = Path(...,description="Enter the adress where the criminal holds power", example="Bhawanipore")):
    return Data_Reading.get_criminal_name_by_parameters(address)

