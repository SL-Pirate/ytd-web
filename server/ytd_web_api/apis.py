from ytd_web_core.download_video import download_video as dlvid
from ytd_web_core.exceptions import *
from pytube.exceptions import RegexMatchError, VideoUnavailable
from ytd_web_core.exceptions import AgeRestrictedVideoException
from ytd_web_core.search_video import search as _search_youtube
from ytd_web_core import Status
from ytd_web_core.models import Downloadable
from ytd_web_core.util import get_url_from_video_id
from ytd_web_core.get_qualities import get_qualities
from rest_framework.views import APIView, Response
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class DownloadVideoAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'video_id',
                openapi.IN_QUERY,
                description='ID of the video',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'quality',
                openapi.IN_QUERY,
                description='Video quality. Use the /search/qualities api to determine available qualities',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'video_format',
                openapi.IN_QUERY,
                required=False,
                description='Video output format. If not provided, the format available from youtube will be used. \nAvailable formats: mp4, webm, mkv',
                type=openapi.TYPE_STRING,
            )
        ],
        responses={
            200: openapi.Response(
                description='Successful response',
                schema=DownloadableSerializer,
                examples={
                    "downloadable_link": "downloadable link",
                    "file_name": "video file name with extension",
                    "valid for": "(int) time duration which video is available for download Eg: 5"
                }
            ),
            400: 'Bad Request',
            403: 'Invalid API key',
            404: 'Video not found',
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            downloadable: Downloadable = dlvid(
                get_url_from_video_id(request.GET.get('video_id', '')),
                request.GET.get('resolution', ''),
                request.GET.get('video_format', '')
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
        except Exception as e:
            return Response(
                {
                    "message": "Bad request",
                    "error": str(e)
                },
                status = 400
            )

class GetQualitiesAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'video_id',
                openapi.IN_QUERY,
                description='ID of the video',
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: openapi.Response(
                description='Successful response',
                schema=QualitiesSerializer,
            ),
            403: 'Invalid API key',
            403: 'Age Restricted',
            500: 'Internal error'
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            data = get_qualities(
                    get_url_from_video_id(
                        request.GET.get(
                            'video_id', 
                            ''
                        )
                    )
                )
            return Response(
                QualitiesSerializer({
                    "audio_qualities": data["audio_qualities"],
                    "video_qualities": data["video_qualities"]
                }).data
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
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'keyword',
                openapi.IN_QUERY,
                description='search keywod',
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: openapi.Response(
                description='Successful response',
                schema=SearchResultsSerializer,
            ),
            403: 'Invalid API key',
            500: 'Internal error'
        }
    )
    def get(self, request, *args, **kwargs):
        results = _search_youtube(request)
        if (len(results) == 0):
            return Response(
                {
                    "message": "No results found"
                },
                status = 404
            )
        if (results[0].get_status() != Status.FAILURE):
            return Response(
                SearchResultsSerializer({
                    'results': [
                        SingleSearchResultSerializer({
                            'video_id': search_result.get_video_id(),
                            'title': search_result.get_title(),
                            'description': search_result.get_description(),
                            'thumbnail_url': search_result.get_thumbnail_url(),
                            'channel_name': search_result.get_channel_name(),
                            'channel_thumbnail_url': search_result.get_channel_thumbnail_url()
                        }).data for search_result in results
                    ]
                }).data
            )

        else:
            return Response(
                {
                    "message": "Failed to connect with youtube"
                },
                status = 500
            )
