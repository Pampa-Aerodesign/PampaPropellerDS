import requests
import os
from datetime import datetime

from ppdb.APC_data_handler import read_APC
from ppdb.misc import get_model_name

from bs4 import BeautifulSoup 


class DataStore:
    """This class builds a database.
    
    Attributes:
        csv_files_path      The path in which to store the .CSV files.
        raw_files_path      The path in which to store the raw files downloaded from a provider.
     
    """
    def __init__(self, raw_files_path, csv_files_path, num_files = None):
        os.makedirs(raw_files_path, exist_ok=True)
        os.makedirs(csv_files_path, exist_ok=True)
        
        self.raw_files_path = raw_files_path
        self.csv_files_path = csv_files_path
        
        if num_files is not None:
            self.num_files = num_files
    
    def get_APC_links(self, archive_URL="https://www.apcprop.com/files/"): 
        
        headers = {"User-Agent" : "Mozilla/5.0 (X11; CrOS x86_64 13729.72.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.116 Safari/537.36"}
        
        r = requests.get(archive_URL, headers=headers)
        
        soup = BeautifulSoup(r.content, 'lxml') 
        
        links = soup.find_all('a')

        propeller_links = []
        for link in links:
            if link['href'].startswith('PER3'):
                propeller_links.append(archive_URL + link['href'])
        
        if self.num_files is not None:
            return propeller_links[:self.num_files]

        return propeller_links
    
    def download_APC_data(self):
        propeller_links = self.get_APC_links()
        headers = {"User-Agent" : "Mozilla/5.0 (X11; CrOS x86_64 13729.72.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.116 Safari/537.36"}
        
        for index, link in enumerate(propeller_links):         
            file_name = self.raw_files_path+link.split('/')[-1] 
    
            print( "Downloading file:%s"%file_name.split('/')[-1]) 
            
            r = requests.get(link, stream = True, headers=headers) 
            
            with open(file_name, 'wb+') as file: 
                for chunk in r.iter_content(chunk_size = 1024*1024): 
                    if chunk: 
                        file.write(chunk)
            file.close()
            
            print( "\nPropeller {} downloaded!\n".format(file_name.split('/')[-1]))
            print( "{} out of {} propellers downloaded \n".format(index+1, len(propeller_links)))
    
        print ("All data downloaded!")
        
    def generate_CSVs(self):
        if self.num_files is not None:
            file_list = [self.raw_files_path + file for file in os.listdir(self.raw_files_path)[:self.num_files]]
        
        else:
            file_list = [self.raw_files_path + file for file in os.listdir(self.raw_files_path)]
        
        for file_path in file_list:
            model = get_model_name(file_path)
            
            df = read_APC(file_path, save_to_path=self.csv_files_path+model+".csv")
    

if __name__ == "__main__":
    test_ds = DataStore("/data/raw_files/", "/data/csv_files/", num_files=2)
    test_ds.download_APC_data()
    test_ds.generate_CSVs()
    