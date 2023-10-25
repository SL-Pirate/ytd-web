from django.http import JsonResponse
from ytd_web_core.download_video import download_video as dlvid
from ytd_web_core.exceptions import *
from pytube.exceptions import RegexMatchError, VideoUnavailable
from ytd_web_core.exceptions import AgeRestrictedVideoException
from ytd_web_core.search_video import search as _search_youtube
from ytd_web_core import Status
from ytd_web_core.models import Downloadable
from ytd_web_core.util import get_url_from_video_id
from ytd_web_core.get_qualities import get_qualities
from rest_framework import serializers
from rest_framework.views import APIView, Response
from .serializers import DownloadableSerializer

class DownloadVideoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            downloadable: Downloadable = dlvid(
                get_url_from_video_id(request.GET.get('video_id', '')),
                request.GET.get('resolution', ''),
            )

            serializer = DownloadableSerializer(downloadable, context={'request': request})

            return Response(serializer.data)
        except RegexMatchError:
            return Response(
                {
                    "message": "Invalid link format! Please check again"
                },
                status = 404
            )
        except AgeRestrictedVideoException:
            return Response(
                {
                    "message": "This video is age restricted!"
                },
                status = 404
            )
        except VideoUnavailable:
            return Response(
                {
                    "message": "video unavailable"
                },
                status = 404
            )

class GetQualitiesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            return Response(
                get_qualities(
                    get_url_from_video_id(
                        request.GET.get(
                            'video_id', 
                            ''
                        )
                    )
                )
            )
        except AgeRestrictedVideoException:
            return Response(
                {
                    "message": "Age restricted video"
                },
                status = 403
            )
        except Exception as e:
            return Response(
                {
                    "message": "Internal server error",
                    "error": str(e)
                },
                status = 500
            )

class SearchVideoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        results = _search_youtube(request)
        if (results[0].get_status() != Status.FAILURE):
            return Response(
                {
                    "results": [search_result.JsonSerialize() for search_result in results]
                }
            )

        else:
            return Response(
                {
                    "message": "Failed to connect with youtube"
                },
                status = 500
            )
