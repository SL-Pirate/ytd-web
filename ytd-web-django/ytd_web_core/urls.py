from django.urls import path
from ytd_web_core.views import serve_downloadable

urlpatterns = [
    path('downloads/<int:id>/', serve_downloadable)
]