import json
import redis
import yaml

class DataProcessor:
    """
    A class to process currency data.
    
    Attributes:
    - redis_config (dict): Configuration for connecting to the Redis database.
    """

    def __init__(self, redis_config):
        """
        Initializes the DataProcessor object.

        Args:
        - redis_config (dict): Configuration for connecting to the Redis database.
        """
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

if __name__ == "__main__":
    # Load Redis configuration from YAML file
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    processor = DataProcessor(config['redis'])
    data = processor.fetch_data_from_redis()
    rates_data = data.get('rates', {})
    if rates_data:
        count = 0
        for currency, rate in rates_data.items():
            if int(rate) < 20:
                print(f"{currency}: {rate}")
                count += 1
                if count == 20:
                    break
    else:
        print("Failed to fetch data from Redis.")
