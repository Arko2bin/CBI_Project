import importlib.util
import os

extract_dic = list(os.getcwd().split("\\"))
project_directory = "\\".join(extract_dic[:len(extract_dic)-1])

spec = importlib.util.spec_from_file_location('Dao_layer',f'{project_directory}\CBIDao\Data_addtion_deletion.py')
Data_addition_deletion = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Data_addition_deletion)



def add_new_criminal_details(criminal_details):
    result = Data_addition_deletion.add_criminal_profile(criminal_details)
    return result