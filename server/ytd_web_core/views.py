from django.http import FileResponse, HttpResponse
from ytd_web_core.models import Downloadable
from django.shortcuts import redirect

# Create your views here.
def serve_downloadable(response, id):
    try:
        downloadable: Downloadable = Downloadable.objects.get(id=id)
        response = HttpResponse()
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment; filename={downloadable.name}'

        return FileResponse(open(downloadable.path, 'rb'))
    except Exception:
        response = redirect("/link-expired/")
        return response
