import requests
from bs4 import BeautifulSoup 
import os
from APC_data_handler import read_APC
import re


def get_propeller_links(archive_URL): 
    
    # create response object 
    headers = {"User-Agent" : "Mozilla/5.0 (X11; CrOS x86_64 13729.72.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.116 Safari/537.36"
               }
    
    r = requests.get(archive_URL, headers=headers)
      
    # create beautiful-soup object 
    soup = BeautifulSoup(r.content, 'lxml') 
      
    # find all links on web-page 
    links = soup.find_all('a')

    # filter the link starting with PER3
    propeller_links = []
    
    for link in links:
        if link['href'].startswith('PER3'):
            propeller_links.append(archive_URL + link['href'])
  
    return propeller_links


def download_propeller_data(propeller_links): 
    
    #Need the User-Agent otherwise will get the 403 HTTPs error (No response) (https://stackoverflow.com/questions/54154583/beautifulsoup-returning-403-error-for-some-sites)
    headers = {"User-Agent" : "Mozilla/5.0 (X11; CrOS x86_64 13729.72.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.116 Safari/537.36"
               }
    #Get the path to this folder
    path = os.getcwd() + "/database/raw_files/"
    
    for index, link in propeller_links:         
        # obtain filename by splitting url and getting the last string 
        file_name = path+link.split('/')[-1] 
  
        print( "Downloading file:%s"%file_name.split('/')[-1]) 
          
        # create response object 
        r = requests.get(link, stream = True, headers=headers) 
          
        # Download
        with open(file_name, 'wb+') as f: 
            for chunk in r.iter_content(chunk_size = 1024*1024): 
                if chunk: 
                    f.write(chunk) 
          
        print( "Propeller {} downloaded!\n".format(file_name.split('/')[-1]))
        print( "{} out of {} propellers downloaded (%d)\ \n"%file_name.split('/')[-1])
  
    print ("All data downloaded!")
    return

def get_model_name(file_path):
    with open(file_path, "r") as file:
        file_lines = file.readlines(1)
    file.close()

    line = file_lines[0]
    line = line.strip()
    line = re.sub(" +", "", line)
    return line.split("(")[0] 


def generate_CSVs(raw_files_path=os.getcwd() + "/database/raw_files/", num_files = None, csv_files_path = os.getcwd()+"/database/csv_files/"):
    
    if num_files is not None:
        file_list = [raw_files_path + file for file in os.listdir(raw_files_path)[:num_files]]
    
    else:
        file_list = [raw_files_path + file for file in os.listdir(raw_files_path)]
    
    for file_path in file_list:
        model = get_model_name(file_path)
        
        df = read_APC(file_path, save_to_path=csv_files_path+model+".csv")
  
if __name__ == "__main__": 
  
    # Data from APC propellers
    archive_URL = "https://www.apcprop.com/files/"
    
    # getting all propeller file links 
    propeller_links = get_propeller_links(archive_URL) 
    # download all propeller data
    download_propeller_data(propeller_links)