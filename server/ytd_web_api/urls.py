from django.urls import path
from ytd_web_api.api import download, qualities, search_video

urlpatterns = [
    path("download/video", download.DownloadVideoAPIView.as_view()),
    path("search", search_video.SearchVideoAPIView.as_view()),
    path("search/qualities", qualities.GetQualitiesAPIView.as_view()),
    path("download/audio", download.DownloadAudioAPIView.as_view())
]
