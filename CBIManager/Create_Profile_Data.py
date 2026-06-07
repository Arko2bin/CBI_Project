from pathlib import Path
import importlib.util
import os

#extract_dic = list(os.getcwd().split("\\"))
project_directory = Path.cwd().parent
if('cbi_project' in str(project_directory).lower()):
    print("Successfully passed if condition on env")
else:
    print("inside else")
    project_directory = project_directory / 'cbi_project'

Data_addition_deletion_path = project_directory / 'CBIDao' / 'Data_addition_deletion.py'

spec = importlib.util.spec_from_file_location('Dao_layer',str(Data_addition_deletion_path))
Data_addition_deletion = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Data_addition_deletion)



def add_new_criminal_details(criminal_details):
    result = Data_addition_deletion.add_criminal_profile(criminal_details)
    return result