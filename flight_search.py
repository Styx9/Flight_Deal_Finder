import os
import requests
from dotenv import load_dotenv
import logging
logging.basicConfig(level=logging.INFO)
load_dotenv()

IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
class FlightSearch:
    """
     Handles searching flights and retrieving IATA codes using Amadeus API.
     """
    def __init__(self):
        self._api_key = os.environ["AMD_API_KEY"]
        self._api_secret = os.environ["AMD_API_SECRET"]
        self._token = self.get_new_token()

    def get_new_token(self) -> str:
        """
            Requests a new OAuth token from Amadeus API.
            :return: Access token string.
        """
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)
        return response.json()['access_token']

    def get_iata_code(self, city_name:str) -> str:
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS",
        }
        response = requests.get(
            url=IATA_ENDPOINT,
            headers=headers,
            params=query
        )
        try:
            return response.json()["data"][0]["iataCode"]
        except (IndexError, KeyError):
            logging.warning(f"No airport code found for {city_name}")
            return "N/A"

    def get_flight_offers(
            self,
            origin_city: str,
            destination_city: str,
            departure_date: str,
            return_date: str,
            is_direct: bool = True
    ) -> dict | None:
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin_city,
            "destinationLocationCode": destination_city,
            "departureDate": departure_date,
            "returnDate": return_date,
            "adults": 1,
            "currencyCode": "EUR",
            "nonStop": "true" if is_direct else "false",
            "max": 100,
        }
        response = requests.get(
            url=FLIGHT_ENDPOINT,
            headers=headers,
            params=query
        )
        if response.status_code != 200:
            logging.error(f"Error: {response.status_code} - {response.text}")
            return None
        return response.json()