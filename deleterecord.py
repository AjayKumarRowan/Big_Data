import requests

class DataProcessor:
    """
    A class to fetch, process, search, and delete currency exchange rates data from a RapidAPI endpoint.

    Attributes:
    - api_url (str): The URL of the RapidAPI endpoint to fetch the data from.
    - api_key (str): The API key required for accessing the RapidAPI endpoint.
    - headers (dict): The headers required for making the HTTP request to the RapidAPI endpoint.
    - response (requests.Response): The response object obtained after making the HTTP request.
    - data (dict): The JSON data obtained from the response.
    - exchange_rates (dict): A dictionary containing the currency exchange rates data.
    """

    api_url = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/latest"
    api_key = "0191caf90emshe2eff9a25e7212ep133f98jsn9f930db0d2cd"

    headers = {
        "X-RapidAPI-Host": "currency-conversion-and-exchange-rates.p.rapidapi.com",
        "X-RapidAPI-Key": api_key
    }

    def __init__(self):
        """
        Initializes the DataProcessor object by fetching data from the RapidAPI endpoint.
        """
        self.response = requests.get(self.api_url, headers=self.headers)
        if self.response.status_code == 200:
            self.data = self.response.json()
            self.exchange_rates = self.data['rates']
        else:
            print(f"Failed to fetch data from API: {self.response.status_code}")

    def search_by_country(self, query):
        """
        Searches for currency exchange rates by country.

        Args:
        - query (str): The country code or name to search for.

        Returns:
        - list: A list of dictionaries containing the country code and its corresponding exchange rate.
        """
        search_results = []
        for country, currency in self.exchange_rates.items():
            if query.lower() in country.lower():
                search_results.append({country: currency})
        return search_results

    def delete_by_country(self, query):
        """
        Deletes currency exchange rate records by country code.

        Args:
        - query (str): The country code or name to search for and delete its corresponding record.

        Returns:
        - list: A list of dictionaries containing the deleted country code and its corresponding exchange rate.
        """
        deleted_records = []
        for country in list(self.exchange_rates.keys()):
            if query.lower() in country.lower():
                currency = self.exchange_rates.pop(country)
                deleted_records.append({country: currency})
        return deleted_records

if __name__ == "__main__":
    processor = DataProcessor()
    search_query = "ANG"  # search query
    results = processor.search_by_country(search_query)
    if results:
        print(f"Search Results for '{search_query}':")
        for result in results:
            print(result)
        
        # Delete records
        deleted_records = processor.delete_by_country(search_query)
        if deleted_records:
            print(f"Deleted records for '{search_query}':")
            for record in deleted_records:
                print(record)
        else:
            print(f"No records found for '{search_query}' to delete")
    else:
        print(f"No results found for '{search_query}'")
