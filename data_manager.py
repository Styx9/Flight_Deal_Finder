import os
import requests
from requests.auth import HTTPBasicAuth
import logging
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.INFO)
class DataManager:
    """
    Handles retrieving and updating flight data in Google Sheets via Sheety API.
    """

    def __init__(self) -> None:
        self._user: str = os.environ["USER"]
        self._password: str = os.environ["PASS"]
        self._sheety_endpoint: str = os.environ["SHEETY_END_GET"]
        self._sheety_endpoint_put: str = os.environ["SHEETY_END_PUT"]
        self._sheety_users_get: str = os.environ["SHEETY_USERS_GET"]
        self._sheety_users_post: str = os.environ["SHEETY_USERS_POST"]
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data: list[dict] = []
        self.customer_data: list[dict] = []
    def get_destination_data(self) -> list[dict]:
        """
            Retrieves destination data from Sheety API.
        """
        response = requests.get(self._sheety_endpoint, auth=self._authorization)
        response.raise_for_status()
        self.destination_data = response.json()["prices"]
        return self.destination_data
    def update_destination_codes(self):
        for row in self.destination_data:
                payload = {"price": {"iataCode": row["iataCode"]}}
                row_id = row["id"]
                put_url = f"{self._sheety_endpoint_put}/{row_id}"
                put_resp = requests.put(put_url, json=payload, auth=HTTPBasicAuth(self._user, self._password))
                put_resp.raise_for_status()
        logging.info("Destination codes updated successfully.")
    def get_customer_email(self):
        """
            Retrieves customer emails from Sheety API.
        """
        response = requests.get(self._sheety_users_get, auth=self._authorization)
        response.raise_for_status()
        self.customer_data = response.json()["users"]
        logging.info("Customer emails retrieved successfully.")
        return self.customer_data