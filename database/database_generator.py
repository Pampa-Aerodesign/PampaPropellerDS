import requests
from bs4 import BeautifulSoup 
import os


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
    
    #Need the User-Agent otherwise will get the 403 HTTPs error (No response)
    headers = {"User-Agent" : "Mozilla/5.0 (X11; CrOS x86_64 13729.72.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.116 Safari/537.36"
               }
    #Get the path to this folder
    path = os.getcwd() + "/raw_files/"

    
    for link in propeller_links:         
        # obtain filename by splitting url and getting 
        # last string 
        file_name = path+link.split('/')[-1] 
  
        print( "Downloading file:%s"%file_name.split('/')[-1]) 
          
        # create response object 
        r = requests.get(link, stream = True, headers=headers) 
          
        # download started
 
        with open(file_name, 'wb+') as f: 
            for chunk in r.iter_content(chunk_size = 1024*1024): 
                if chunk: 
                    f.write(chunk) 
          
        print( "Propeller %s downloaded!\n"%file_name.split('/')[-1])
  
    print ("All data downloaded!")
    return
  
  
if __name__ == "__main__": 
  
    # Data from APC propellers
    archive_URL = "https://www.apcprop.com/files/"
    
    # getting all propeller file links 
    propeller_links = get_propeller_links(archive_URL) 
    # download all propeller data
    download_propeller_data(propeller_links)