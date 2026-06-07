from pathlib import Path
import importlib.util
import os

#extract_dic = list(os.getcwd().split("\\"))
project_directory = Path.cwd().parent
if('cbi_project' in str(project_directory).lower()):
    pass
else:
    project_directory = project_directory / 'cbi_project'

Data_Reading_path = project_directory / 'CBIDao' / 'Data_Reading.py'

spec = importlib.util.spec_from_file_location('Dao_layer',str(Data_Reading_path))
Data_Reading = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Data_Reading)

def search_profile_data(criminal_name):
    full_criminal_name = Data_Reading.get_criminal_name(criminal_name)
    if(full_criminal_name is None):
        return "Error Message","No Criminal Record Found"
    else:
        full_criminal_profile = Data_Reading.fetch_criminal_profile(full_criminal_name)
        if("Image" in list(full_criminal_profile.keys())):
            criminal_image = full_criminal_profile['Image']
        else:
            criminal_image = "N/A"
        return full_criminal_profile,criminal_image


def get_criminal_name_by_parameters(parameters):
    total_data = {}

    # Check if parameters dictionary is empty
    if not parameters:
        return {"Error_Message": "No search filters selected"}

    # Get all names to loop through
    criminal_names = Data_Reading.get_all_criminal_names()

    for criminal in criminal_names:
        profile = Data_Reading.fetch_criminal_profile(criminal)

        # If the profile doesn't exist or is empty, skip to next criminal
        if not profile:
            continue

        is_match = True  # Assume the criminal matches until proven otherwise

        # Loop through each search filter provided by the user
        for key, filter_value in parameters.items():
            # If the profile doesn't even contain the searched key, it's a mismatch
            if key not in profile:
                is_match = False
                break

            criminal_value = profile[key]

            # Scenario 1: Handle Integer Ranges (Checking if filter_value is a dict with min/max)
            if isinstance(filter_value, dict) and "min" in filter_value and "max" in filter_value:
                try:
                    current_val = int(criminal_value)
                    # Check if the criminal's value falls OUTSIDE the requested range
                    if current_val < int(filter_value["min"]) or current_val > int(filter_value["max"]):
                        is_match = False
                        break
                except (ValueError, TypeError):
                    # In case data in Firebase isn't a valid number
                    is_match = False
                    break

            # Scenario 2: Handle String/Text Matches (Exact or Case-Insensitive)
            else:
                # Convert both to lowercase strings for a fair case-insensitive match
                if str(criminal_value).strip().lower() != str(filter_value).strip().lower():
                    is_match = False
                    break

        # If the criminal survived all the filter checks, add them to our results!
        if is_match:
            total_data[criminal] = profile

    # Return matching data or a friendly error
    if len(total_data) > 0:
        return total_data
    else:
        return {"Error_Message": "No Criminal Record Found"}
