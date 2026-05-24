import importlib.util
spec = importlib.util.spec_from_file_location('Dao_layer','F:\PyCharm Community Edition 2022.3.1\FastAPI_project_demo\CBIDao\Data_Reading.py')
Data_Reading = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Data_Reading)

def search_profile_data(criminal_name):
    full_criminal_name = Data_Reading.get_criminal_name(criminal_name)
    if(full_criminal_name is None):
        return "No Data","No Data"
    else:
        full_criminal_profile = Data_Reading.fetch_criminal_profile(full_criminal_name)
        if("Image" in list(full_criminal_profile.keys())):
            criminal_image = full_criminal_profile['Image']
        else:
            criminal_image = "N/A"
        return full_criminal_profile,criminal_image

def get_criminal_name_by_parameters(parameters):
    total_data = {}
    criminal_names = Data_Reading.get_all_criminal_names()
    for criminal in criminal_names:
        data = Data_Reading.fetch_criminal_profile(criminal)
        data_modified = [
            sub_item
            for item in list(data.values())
            for sub_item in (item.lower().split() if isinstance(item, str) else [item])
        ]
        if parameters.lower() in data_modified:
            if data['Image'] != "":
                total_data[data['Image']] = data
            else:
                total_data[f'No Image {data["name"]}'] = data
    if(len(total_data) > 0):
        return total_data
    else:
        return {"Error_Message": "No Criminal Record Found"}
