from configparser import ConfigParser
import hashlib
import time
from django.http.response import HttpResponse
from ytd_web.settings import PUBLIC_ENDPOINTS, PUBLIC_URL_PATTERNS, DEBUG

_config = ConfigParser()
_config.read(".env")
_api_key = _config["session"]["key"]

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # desabling authentication on debug mode
        if not DEBUG:
            process_request = self.process_request(request)
            if process_request is not None:
                return process_request
            
        response = self.get_response(request)
        return response

    def process_request(self, request):
        try:
            # bypassing authentication for PUBLIC_ENDPOINTS from settings.py
            if request.path in PUBLIC_ENDPOINTS or '/downloads/' in request.path:
                return None
            
            # bypassing authentication for PUBLIC_URL_PATTERNS from settings.py
            for pattern in PUBLIC_URL_PATTERNS:
                if pattern in request.path:
                    return None
            
            timestamp = request.META.get('HTTP_TIMESTAMP')
            # checking timestamp is within 5 minutes
            # and token is valid
            if (
                (int(timestamp) + 300000) > (time.time() * 1000)
            ) and request.META.get('HTTP_TOKEN') == hashlib.md5(
                f"{timestamp}{_api_key}".encode()
            ).hexdigest():
                return None
            else:
                return HttpResponse('Unauthorized', status=401)
        except Exception:
            return HttpResponse('Unauthorized', status=401)
