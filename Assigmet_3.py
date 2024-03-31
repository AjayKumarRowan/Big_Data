import requests
import json
from db_config import get_redis_connection

class DataProcessor:
    """
    A class to fetch data from a currency conversion API, process it, and insert it into a Redis database.

    Attributes:
    - api_url (str): The URL of the currency conversion API.
    - api_key (str): The API key required for accessing the currency conversion API.
    - redis_client: A Redis client object used for interacting with the Redis database.
    """

    def __init__(self, api_url, api_key):
        """
        Initializes the DataProcessor object.

        Args:
        - api_url (str): The URL of the currency conversion API.
        - api_key (str): The API key required for accessing the currency conversion API.
        """
        self.api_url = api_url
        self.api_key = api_key
        self.redis_client = get_redis_connection()

    def fetch_data_from_api(self):
        """
        Fetches currency conversion data from the API.

        Returns:
        - dict: A dictionary containing the fetched currency conversion data.
        """
        headers = {
            "X-RapidAPI-Host": "currency-conversion-and-exchange-rates.p.rapidapi.com",
            "X-RapidAPI-Key": self.api_key
        }
        response = requests.get(self.api_url, headers=headers)
        if response.status_code == 200:
            print("Fetching data from API is competed.")
            return response.json()
        else:
            raise Exception(f"Failed to fetch data from API: {response.status_code}")

    def insert_into_redis(self, data):
        """
        Inserts currency conversion data into a Redis database.

        Args:
        - data (dict): A dictionary containing the currency conversion data to be inserted into Redis.
        """
        for currency, rate in data.items():
            self.redis_client.hset("currency_data", currency, json.dumps(rate))

if __name__ == "__main__":
    api_url = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/latest"
    api_key = " "

    processor = DataProcessor(api_url, api_key)
    data = processor.fetch_data_from_api()
    processor.insert_into_redis(data)
