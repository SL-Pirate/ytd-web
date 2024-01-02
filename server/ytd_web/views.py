from django.shortcuts import render
from django.http import FileResponse, JsonResponse
import requests
import io
from ytd_web_core.util import base64_to_str

def root(request):
    return render(request, 'root/welcome.html', {})

def not_found(request, exception=Exception):
    return render(request, 'root/404.html', {})

def link_expired(request):
    return render(request, 'root/link_expired.html', {})

def cors_proxy(request):
    if request.method == 'GET':
        remote_url = base64_to_str(request.GET.get('url'))
        if remote_url:
            response = requests.get(remote_url)
            if response.status_code != 200:
                return JsonResponse({'error': 'Resource not found'}, status=404)
            return FileResponse(io.BytesIO(response.content), filename="ytimg.jpg")

    return JsonResponse({'error': 'Invalid request'}, status=400)
