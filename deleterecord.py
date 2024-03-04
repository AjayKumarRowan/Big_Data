import yaml
import redis
import json

class DataProcessor:
    """
    A class to fetch and process currency exchange rates data from a Redis database.
    
    Attributes:
    - redis_config (dict): Configuration for connecting to the Redis database.
    - redis_client: A Redis client object used for interacting with the Redis database.
    """

    def __init__(self, redis_config_file):
        """
        Initializes the DataProcessor object.

        Args:
        - redis_config_file (str): Path to the YAML file containing Redis configuration.
        """
        with open(redis_config_file, 'r') as file:
            redis_config = yaml.safe_load(file)['redis']
        
        self.redis_config = redis_config
        self.redis_client = redis.StrictRedis(
            host=redis_config['host'],
            port=redis_config['port'],
            db=redis_config['db'],
            password=redis_config.get('password')
        )

    def fetch_data_from_redis(self):
        """
        Fetches currency conversion data from Redis.

        Returns:
        - dict: A dictionary containing the fetched currency conversion data.
        """
        currency_data = self.redis_client.hgetall("currency_data")
        return {currency.decode(): json.loads(rate.decode()) for currency, rate in currency_data.items()}

    def search_by_country(self, query):
        """
        Searches for currency exchange rates by country.

        Args:
        - query (str): The country code or name to search for.

        Returns:
        - list: A list of dictionaries containing the country code and its corresponding exchange rate.
        """
        data = self.fetch_data_from_redis()
        rates_data = data.get('rates', {})
        search_results = []
        for country, currency in rates_data.items():
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
        data = self.fetch_data_from_redis()
        rates_data = data.get('rates', {})
        deleted_records = []
        for country, currency in rates_data.items():
            if query.lower() in country.lower():
                self.redis_client.hdel("currency_data", country)
                deleted_records.append({country: currency})
        return deleted_records

if __name__ == "__main__":
    redis_config_file = "config.yaml"
    processor = DataProcessor(redis_config_file)
    search_query = "ANG"  # search query
    results = processor.search_by_country(search_query)
    if results:
        print(f"Search Results for '{search_query}':")
        for result in results:
            print(result)
    else:
        print(f"No results found for '{search_query}'")

    # Delete records
    deleted_records = processor.delete_by_country(search_query)
    if deleted_records:
        print(f"Deleted records for '{search_query}':")
        for record in deleted_records:
            print(record)
    else:
        print(f"No records found for '{search_query}' to delete")
