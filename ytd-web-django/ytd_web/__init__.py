from configparser import ConfigParser

config: ConfigParser = ConfigParser()
config.read("server.cfg")

redis: str = config["DEFAULT"]["redis_connection"]

