from fastapi import FastAPI,Path
import importlib.util

spec = importlib.util.spec_from_file_location('Dao_layer','F:\PyCharm Community Edition 2022.3.1\FastAPI_project_demo\CBIDao\Data_Reading.py')
Data_Reading = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Data_Reading)

spec2 = importlib.util.spec_from_file_location('Manager_layer','F:\PyCharm Community Edition 2022.3.1\FastAPI_project_demo\CBIManager\Search_Profile_Data.py')
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

