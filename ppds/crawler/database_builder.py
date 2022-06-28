import logging
import os

import requests
from bs4 import BeautifulSoup

from ppds.crawler.apc_data_handler import apc_to_csv, get_model_name

logging.basicConfig(level=logging.INFO)


class DatabaseBuilder:
    def __init__(self, raw_files_path: str, csv_files_path: str, num_files: int = None):
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
        self.num_files = num_files

    def _get_APC_links(
        self, archive_URL: str = "https://www.apcprop.com/files/"
    ) -> list:
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

        if self.num_files:
            return propeller_links[: self.num_files]
        else:
            return propeller_links

    def download_APC_data(self):
        """Will download all propeller data from the website."""
        propeller_links = self._get_APC_links()
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 13729.72.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.116 Safari/537.36"
        }

        for index, link in enumerate(propeller_links):
            file_name = self.raw_files_path + link.split("/")[-1]

            logging.debug("Downloading file:%s" % file_name.split("/")[-1])

            try:
                r = requests.get(link, stream=True, headers=headers)

            except requests.exceptions.RequestException as e:
                logging.error(e)

            with open(file_name, "wb+") as file:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        file.write(chunk)
            file.close()

            logging.debug("Propeller {} downloaded.".format(file_name.split("/")[-1]))
            logging.info(
                "{} out of {} propellers downloaded. \n".format(
                    index + 1, len(propeller_links)
                )
            )

    def generate_CSVs(self):
        """Will generate the csv files from the raw files."""
        if self.num_files:
            raw_files_list = [
                self.raw_files_path + file for file in os.listdir(self.raw_files_path)
            ][: self.num_files]
        else:
            raw_files_list = [
                os.path.join(self.raw_files_path, file)
                for file in os.listdir(self.raw_files_path)
            ]

        csv_files_list = [
            os.path.join(self.csv_files_path, get_model_name(file) + ".csv")
            for file in raw_files_list
        ]

        for i in range(0, len(raw_files_list)):
            logging.debug("Generating CSV file: {}".format(csv_files_list[i]))
            apc_to_csv(raw_files_list[i], csv_files_list[i])
            logging.info(
                "{} out of {} propellers converted to csv. \n".format(
                    i + 1, len(raw_files_list)
                )
            )


if __name__ == "__main__":
    NUM_FILES = 3
    db = DatabaseBuilder(
        os.path.join("data", "raw_files", ""),
        os.path.join("data", "csv_files", ""),
        num_files=NUM_FILES,
    )
    db.download_APC_data()
    db.generate_CSVs()
