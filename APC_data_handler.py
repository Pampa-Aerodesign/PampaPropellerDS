import pandas as pd
import numpy as np
import sys
import re
from io import StringIO
import streamlit as st
    
    
def APC_to_csv(file_lines, verbose, save_to_path = None):
    """Converts list of lines in an APC performance file (file_lines) to a csv buffer

    :param file_lines: List with all the lines in a file 
    :type file_lines: list
    :param verbose: If True will print logs
    :type verbose: bool
    :return: Buffer with the lines organized as a CSV
    :rtype: StringIO
    """
    
    num_lines = sum(1 for line in file_lines)
    
    rpm_lines = np.arange(14, num_lines, 37)
    
    count = 1
    line_on_focus = np.array([])
    for i in range(14, num_lines+1, 1):
        if (count==5):
            line_on_focus = np.append(line_on_focus, np.arange(i, i+30, 1)) 
        elif (count==38):
            count = 1
        count = count+1  


    buffer=""

    line_count = 1

    for line in file_lines: 
        if line_count in rpm_lines:
            line = line.strip()
            line = re.sub(" +", " ", line)
            line = re.sub("PROP RPM = ", "", line)
            rpm=line

        if line_count in line_on_focus:
            line = line.strip()
            line = re.sub(" +", " ",line)
            buffer = buffer+line+' ' + rpm + "\n"
        
        line_count = line_count + 1

    buffer=buffer.replace(" ", ",")
        
    buffer = StringIO(buffer)
    
    return buffer
    

def APC_CSV_to_df(buffer, model, verbose = False):
    
    headers=['Velocity (mph)', 'J (Adv Ratio)', 'Pe',
             'Ct', 'Cp', 'PWR (Hp)',
             'Torque (In-Lbf)', 'Thrust(Lbf)', 'RPM']
        
    df=pd.read_csv(buffer, header=None, names=headers)
    
    if verbose:
        print('Erros de NAN:\n',df.isna().sum(), '\n')
    
    df = df.dropna()
    df = df.apply(pd.to_numeric)
    df['Model'] = model
    
    return df


def SI_dataframe (df):
    """Will convert the APC_DataFrame generated by read_APC_txt to SI units

    :param df: APC_DataFrame to be converted
    :type df: Pandas DataFrame
    :return: APC_DataFrame in SI units
    :rtype: Pandas DataFrame
    """
    df['Velocity (mph)'] = df['Velocity (mph)']*0.44704 
    
    df['PWR (Hp)'] = df['PWR (Hp)']*746
    
    df['Torque (In-Lbf)'] = df['Torque (In-Lbf)']*0.112984833333333
    
    df['Thrust(Lbf)'] = df['Thrust(Lbf)']*4.448222
    
    df['RPM'] = df['RPM']/60
    
    df.columns=['Velocity (m/s)', 'J (Adv Ratio)', 'Pe',
                'Ct', 'Cp', 'PWR (W)',
                'Torque (N/m)', 'Thrust (N)', 'Frequency (Hz)',
                'Model'] 
    return df

def read_APC(models_dict, verbose=False, convert_to_SI=True):

    data = []
    
    for model in models_dict.keys():
        if verbose:
            print('Reading Model: '+model)
            print("-------------------------")
        
        filepath_or_buffer = models_dict[model]
        
        if type(filepath_or_buffer) is str:
            with open(filepath_or_buffer) as file:
                file_lines = file.readlines()
            file.close()
            
        else:
            file_lines = filepath_or_buffer.readlines()
        
        buffer = APC_to_csv(file_lines, verbose, save_to_path="test.csv")
        
        cache = APC_CSV_to_df(buffer, model, verbose)
        
        if convert_to_SI:
            cache = SI_dataframe(cache)
        
        data.append(cache)
                
    df = pd.concat(data, ignore_index=True)
    
    return df



if __name__ == "__main__":
        data = []
        models_dict = {'11x7' : '11x7.dat.txt'}
        df = read_APC(models_dict, verbose = True, convert_to_SI=True)
        print(df)


