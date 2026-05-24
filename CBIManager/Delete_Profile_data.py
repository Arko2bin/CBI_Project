import importlib.util
import os

extract_dic = list(os.getcwd().split("\\"))
project_directory = "\\".join(extract_dic[:len(extract_dic)-1])

spec = importlib.util.spec_from_file_location('Dao_layer',f'{project_directory}\CBIDao\Data_addtion_deletion.py')
Data_addition_deletion = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Data_addition_deletion)

def delete_criminal_profile(criminal_names):
    for name in criminal_names:
        result = Data_addition_deletion.delete_criminal_profile(name)
        if not result:
            break
    return result

