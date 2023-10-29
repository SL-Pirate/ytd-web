from configparser import ConfigParser
import hashlib

_config = ConfigParser()
_config.read(".env")
_api_key = _config["session"]["key"]
    
def authenticate(request) -> bool:
    if request.META.get('HTTP_TOKEN') == hashlib.md5(
        f"{request.META.get('HTTP_TIMESTAMP')}{_api_key}".encode()
    ).hexdigest():
        return True
    else:
        return False
