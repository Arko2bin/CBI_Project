import importlib.util
spec = importlib.util.spec_from_file_location('Dao_layer','F:\PyCharm Community Edition 2022.3.1\FastAPI_project_demo\CBIDao\Data_addtion_deletion.py')
Data_addition_deletion = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Data_addition_deletion)

def delete_criminal_profile(criminal_names):
    for name in criminal_names:
        result = Data_addition_deletion.delete_criminal_profile(name)
        if not result:
            break
    return result

