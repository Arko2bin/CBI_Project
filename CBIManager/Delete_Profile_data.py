from pathlib import Path
import importlib.util
import os

extract_dic = list(os.getcwd().split("\\"))
project_directory = Path.cwd().parent

Data_addition_deletion_path = project_directory / 'CBIDao' / 'Data_addition_deletion.py'

spec = importlib.util.spec_from_file_location('Dao_layer',str(Data_addition_deletion_path))
Data_addition_deletion = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Data_addition_deletion)

def delete_criminal_profile(criminal_names):
    for name in criminal_names:
        result = Data_addition_deletion.delete_criminal_profile(name)
        if not result:
            break
    return result

