from configparser import ConfigParser

# google API key for accessing youtube data api
config = ConfigParser()

config.read('secrets.key')
googleApiKey = config['googleApiKey']['key']
api_key = config['self_api']['key']

config.read('server.cfg')
max_vids: int = int(config['DEFAULT']['max_vids'])
keep_time: int = int(config["DEFAULT"]['keep_time'])
api_server_root: str = config["DEFAULT"]["api_server_root"]

secret_key = config["session"]['key']

num_vids = 0
