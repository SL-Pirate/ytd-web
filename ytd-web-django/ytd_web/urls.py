"""
URL configuration for ytd_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ytd_web import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # new endpoints
    path('', views.root),
    path('link-expired/', views.link_expired),
    path("proxy", views.cors_proxy),

    # other apps
    path('', include('ytd_web_core.urls')),
    path('api/v1/', include('ytd_web_api.urls')),
]

handler404 = 'ytd_web.views.not_found'
