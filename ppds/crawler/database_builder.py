import os
import logging
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB

from ppds.crawler.APC_data_handler import get_model_name, read_APC

logging.basicConfig(level=logging.INFO)

class DatabaseBuilder:
    def __init__(self, raw_files_path:str, csv_files_path:str, num_files:int=None):
        """DatabaseBuilder constructor

        Args:
            raw_files_path (str): Path where raw files will be stored.
            csv_files_path (str): Path where csv files will be stored.
            num_files (int, optional): Maximum number of files to download. Defaults to None.
        """
        os.makedirs(raw_files_path, exist_ok=True)
        os.makedirs(csv_files_path, exist_ok=True)
        self.raw_files_path = raw_files_path
        self.csv_files_path = csv_files_path

        if num_files is not None:
            self.num_files = num_files

    def _get_APC_links(self, archive_URL:str="https://www.apcprop.com/files/") -> list:
        """Will get all propeller links from the APC website.

        Args:
            archive_URL (_type_, optional): Archive where files will be fetched. Defaults to "https://www.apcprop.com/files/".

        Returns:
            _type_: List of propeller links.
        """        

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 13729.72.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.116 Safari/537.36"
        }

        try:
            response = requests.get(archive_URL, headers=headers)
        except requests.exceptions.RequestException as e:
            logging.error(e)

        soup = BeautifulSoup(response.content, "lxml")

        links = soup.find_all("a")

        propeller_links = []
        for link in links:
            if link["href"].startswith("PER3"):
                propeller_links.append(archive_URL + link["href"])

        if self.num_files is not None:
            return propeller_links[: self.num_files]

        return propeller_links

    def download_APC_data(self):
        """Will download all propeller data from the website.
        """        
        propeller_links = self._get_APC_links()
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 13729.72.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.116 Safari/537.36"
        }

        for index, link in enumerate(propeller_links):
            file_name = self.raw_files_path + link.split("/")[-1]

            logging.info("Downloading file:%s" % file_name.split("/")[-1])

        try:
            r = requests.get(link, stream=True, headers=headers)
        except requests.exceptions.RequestException as e:
            logging.error(e)

            with open(file_name, "wb+") as file:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        file.write(chunk)
            file.close()

            logging.info("Propeller {} downloaded!".format(file_name.split("/")[-1]))
            logging.info(
                "{} out of {} propellers downloaded \n".format(
                    index + 1, len(propeller_links)
                )
            )

        print("All data downloaded!")

    def generate_CSVs(self):
        """Will generate all csv files from the raw files.
        """        
        if self.num_files is not None:
            file_list = [
                self.raw_files_path + file
                for file in os.listdir(self.raw_files_path)[: self.num_files]
            ]

        else:
            file_list = [
                self.raw_files_path + file for file in os.listdir(self.raw_files_path)
            ]

        for file_path in file_list:
            model = get_model_name(file_path)

            df = read_APC(file_path, save_to_path=self.csv_files_path + model + ".csv")


if __name__ == "__main__":
    db = DatabaseBuilder("/data/raw_files/", "/data/csv_files/", num_files=2)
    db.download_APC_data()
