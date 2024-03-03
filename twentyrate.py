import requests

class DataProcessor:
    """
    A class to process currency data.
    
    Attributes:
    - api_url (str): The URL of the currency conversion API.
    - api_key (str): The API key for accessing the currency conversion API.
    - headers (dict): The headers required for making requests to the API.
    """

    api_url = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/latest"
    api_key = "0191caf90emshe2eff9a25e7212ep133f98jsn9f930db0d2cd"

    headers = {
        "X-RapidAPI-Host": "currency-conversion-and-exchange-rates.p.rapidapi.com",
        "X-RapidAPI-Key": api_key
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        exchange_rates = data['rates']

        # Print only rates below 20
        for currency, rate in exchange_rates.items():
            if rate < 20:
                print(f"{currency}: {rate}")
    else:
        print(f"Failed to fetch data from API: {response.status_code}")
