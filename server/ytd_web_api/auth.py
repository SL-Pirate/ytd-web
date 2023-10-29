from configparser import ConfigParser

_config = ConfigParser()
_config.read(".env")
_api_key = _config["session"]["key"]
    
def authenticate(request) -> bool:
    api_key = request.META.get('key')
    if api_key == _api_key:
        return True
    else:
        return False
