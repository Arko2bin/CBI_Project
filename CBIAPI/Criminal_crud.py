from fastapi import FastAPI,Path,Query,HTTPException
from pathlib import Path as filePath
from operator import itemgetter
import importlib.util
import os

extract_dic = list(os.getcwd().split("\\"))
project_directory = filePath.cwd().parent
if('cbi_project' in str(project_directory).lower()):
    pass
else:
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
    return Search_Profile_Data.get_criminal_name_by_parameters(address)

@app.get('/sort')
def sort_criminals(sort_by: str = Query(...,description="Sorting on basis of money looted by criminal"),
                   order: str = Query('asc',description="Sorting in ascending order")):
    valid_parameters = []
    parameters = Data_Reading.get_parameters()
    for key,value in parameters.items():
        if(value == int):
            valid_parameters.append(key)
    print(valid_parameters)
    if(sort_by not in valid_parameters):
        raise HTTPException(status_code=400,detail=f'invalid field select from {valid_parameters}')
    if(order not in ['asc','desc']):
        raise HTTPException(status_code=400,detail='Invalid field select from asc and desc')

    submission_data = {}
    if('age' in sort_by.lower()):
        submission_data = {
            'age' : {
                'min' : 0,
                'max' : 100
            }
        }
    if ('money_looted' in sort_by.lower()):
        submission_data = {
            'money_looted': {
                'min': 0,
                'max': 1000000000
            }
        }
    client_data = Search_Profile_Data.get_criminal_name_by_parameters(submission_data)
    sort_type = True if order == 'desc' else False
    sorted_client_data = dict(sorted(client_data.items(),key=lambda x:x[1][f'{sort_by}'],reverse=sort_type))
    return sorted_client_data



