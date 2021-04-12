import pandas as pd
import re
from io import StringIO    
    
def APC_to_csv(file_lines, verbose):
    """Converts list of lines in an APC performance file (file_lines) to a csv buffer

    :param file_lines: A Python list with all the lines in a file 
    :type file_lines: list
    :param verbose: If True will print logs
    :type verbose: bool
    :return: Buffer with the lines organized as a CSV
    :rtype: StringIO
    """
    buffer=""
    searching_headers = True
    searching_units = False
    for line in file_lines:
        if  re.search("PROP RPM", line):
            rpm = line.strip()
            rpm = re.sub("  +", "", rpm)
            rpm = re.sub("[^0-9]", "", rpm)

        if (not re.search(r'[a-zA-z]', line)) and (not line.isspace()):
            data_line = line.strip()
            data_line = re.sub(" +", ",",data_line)
            
            buffer = buffer + data_line + ',' + rpm + "\n"
        
        if ((not re.search(r'[0-9\(\)\:]', line)) and (not line.isspace()) and searching_headers):
            headers_line = line.strip()
            headers_line = re.sub(" +", ",", headers_line)
            
            buffer = buffer + headers_line + ',' + 'RPM' + "\n"
            
            searching_headers = False
            searching_units = True
            continue
            
        if searching_units:
            units_line = line.strip()
            units_line = re.sub("  +", ",", units_line)
            
            if len(headers_line.split(',')) != len(units_line.split(',')):
                units_line = units_line[:18] + "-,-,-," + units_line[18:]
            
            buffer = buffer + units_line + ',' + 'RPM' + "\n"
            searching_units = False

    buffer = StringIO(buffer)
    return buffer

def get_model_name(filepath_or_buffer):
    if type(filepath_or_buffer) is str:
        with open(filepath_or_buffer, "r") as file:
            file_lines = file.readlines(1)
        file.close()
    else:
        file_lines = filepath_or_buffer.readlines()

    line = file_lines[0]
    line = line.strip()
    line = re.sub(" +", "", line)
    return line.split("(")[0] 

def read_APC(filepath_or_buffer, verbose=False, save_to_path=None, save_model_name=False):
    """Will read a dictionary with APC data and convert it to a Pandas DataFrame  

    :param models_dict: Python dictionary structured as: {'Model_1_name' : 'path_to_file' or StringIO, ...}
    :type models_dict: dict
    :param verbose: If True will print what it's doing, defaults to False
    :type verbose: bool, optional
    :param save_to_path: If True will save dataframe to a csv file, defaults to False
    :type save_to_path: bool, optional
    :param save_model_name: If True will create a column on dataframe with the model name, defaults to False
    :type save_model_name: bool, optional
    :return: Pandas Dataframe with the data
    :rtype: Pandas DataFrame
    """    
    if type(filepath_or_buffer) is str:
        with open(filepath_or_buffer) as file:
            file_lines = file.readlines()
        file.close()   
    else:
        file_lines = filepath_or_buffer.readlines()
    
    if save_model_name or verbose:
        model_name = get_model_name()
    
    if verbose:
        print('Reading Model: ' + model_name)
        print("------------------------------")
    
    df = pd.read_csv(APC_to_csv(file_lines, verbose))
    
    if save_to_path is not None:
        df.to_csv(save_to_path)
        
    return df
