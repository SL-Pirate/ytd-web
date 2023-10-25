from django.urls import path
from ytd_web_api import apis

urlpatterns = [
    path("download/video", apis.DownloadVideoAPIView.as_view()),
    path("search", apis.SearchVideoAPIView.as_view()),
    path("search/qualities", apis.GetQualitiesAPIView.as_view())
]
