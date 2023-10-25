from django.urls import path
from ytd_web_api import apis

urlpatterns = [
    path("download/video", apis.download_video),
    path("search", apis.search),
    path("search/qualities", apis.get_qual)
]
