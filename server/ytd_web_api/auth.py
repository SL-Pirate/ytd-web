from configparser import ConfigParser
import hashlib
import time

_config = ConfigParser()
_config.read(".env")
_api_key = _config["session"]["key"]
    
def authenticate(request) -> bool:
    timestamp = request.META.get('HTTP_TIMESTAMP')
    # checking timestamp is within 5 minutes
    # and token is valid
    if not timestamp < time.time * 1000 - 300000 and request.META.get('HTTP_TOKEN') == hashlib.md5(
        f"{timestamp}{_api_key}".encode()
    ).hexdigest():
        return True
    else:
        return False
