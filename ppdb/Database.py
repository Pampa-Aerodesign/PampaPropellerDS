import os
from datetime import datetime

from ppdb.misc import get_model_name
from tinydb import TinyDB


class Database(TinyDB):
    """This class aims to add methods to the TinyBD class. 
    """
    
    def __init__(self, data_store_path=os.getcwd()+"/data/",
                 path_to_db_file=os.getcwd() + "/data/"+ "propeller_db.json",
                 num_files = None):
        
        self.raw_files_path = data_store_path + "raw_files/"
        self.csv_files_path = data_store_path + "csv_files/"
        self.num_files = num_files
        self.path_to_db_file = path_to_db_file
        super().__init__(path_to_db_file)
    
    def get_model_info(self, file_name):
        full_raw_path = self.raw_files_path + file_name
        
        model_name = get_model_name(full_raw_path)
        
        diameter = model_name.split("x")[0]
        pitch = model_name.split("x")[1]

        full_csv_path = self.csv_files_path+model_name+".csv"

        return model_name, diameter, pitch, full_raw_path, full_csv_path
        
    def append_model(self, model_raw_path):
        model_name, diameter, pitch, raw_path, csv_path = self.get_model_info(model_raw_path)
        
        self.insert({"Name" : model_name,
                "manufacturer" : "APC",
                "diameter" : diameter,
                "pitch" : pitch,
                "raw_path" : raw_path,
                "csv_path" : csv_path,
                "timestamp_of_entry" : datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")})
    
    def build_local_db(self, from_scratch=True):
        
        if self.num_files is not None:
            raw_files_list = os.listdir(self.raw_files_path)[:self.num_files]
        else:
            raw_files_list = os.listdir(self.raw_files_path)
        
        for model_raw_path in raw_files_list:
            self.append_model(model_raw_path)
            
            
if __name__ == "__main__":
    db = Database()
    db.truncate()
    db.build_local_db()
