import logging

import pandas as pd
import requests
from bs4 import BeautifulSoup


class DataStore:
    """Class to handle the data fetching."""

    def __init__(
        self,
        url: str = "https://github.com/Pampa-Aerodesign/PampaPropellerDS/tree/master/data/csv_files",
    ):
        """Initialize the DataStore.

        Args:
            url (str, optional): Data Store URL. Defaults to "https://github.com/Pampa-Aerodesign/PampaPropellerDS/tree/master/data/csv_files".
        """
        self.url = url
        self.soup = self._get_soup()
        self.propellers_list = self._get_propellers_list()

    def _get_soup(self) -> BeautifulSoup:
        """Return the BeautifulSoup object of the url.

        Returns:
            BeautifulSoup: The BeautifulSoup object of the url.
        """
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException as e:
            logging.error(e)
        return BeautifulSoup(response.text, "html.parser")

    def _get_propellers_list(self) -> list:
        """Return the list of propellers in Data Store.

        Returns:
            list: The list of propellers in Data Store.
        """
        propellers_list = []
        for link in self.soup.find_all("a"):
            if link.get("href").endswith(".csv"):
                propellers_list.append(
                    link.get("href")
                    .split("/")[-1]
                    .split(".csv")[0]  # get the name of the propeller
                )
        return propellers_list

    def get_propeller_data(
        self,
        propeller: str,
        data_url: str = "https://raw.githubusercontent.com/Pampa-Aerodesign/PampaPropellerDS/master/data/csv_files",
    ) -> pd.DataFrame:
        """Return the raw DataFrame of the propeller.

        Args:
            propeller (str): The propeller to get the data from.
            data_url (str, optional): URL where data is stored. Defaults to "https://raw.githubusercontent.com/Pampa-Aerodesign/PampaPropellerDS/master/data/csv_files".

        Returns:
            pd.DataFrame: The raw DataFrame of the propeller.
        """

        propeller_url = data_url + "/" + propeller + ".csv"

        try:
            return pd.read_csv(propeller_url, index_col=0)
        except Exception as e:
            logging.error(e)
