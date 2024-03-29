from ytd_web_core.download_video import download_video_dl as dlvid
from ytd_web_core.download_audio import download_audio_dl as dlaud
from pytube.exceptions import RegexMatchError, VideoUnavailable
from ytd_web_core.exceptions import AgeRestrictedVideoException, UnavailableVideoQualityException
from ytd_web_core.models import Downloadable
from ytd_web_core.util import get_url_from_video_id
from rest_framework.views import APIView, Response
from ytd_web_api.serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpRequest

class DownloadVideoAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'url': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='URL of the video.',
                ),
                'resolution': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Video quality. Use the /search/qualities api to determine available qualities',
                ),
                'video_format': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Video output format. If not provided, the format available from youtube will be used. \nAvailable formats: mp4, webm, mkv',
                ),
            },
            required=['url']
        ),
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
    def post(self, request: HttpRequest, *args, **kwargs):
        try:
            downloadable: Downloadable = dlvid(
                request.data.get('url', ''),
                request.data.get('resolution'),
                request.data.get('video_format')
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
        except UnavailableVideoQualityException:
            return Response(
                {
                    "message": "Invalid/Unavailable video resolution"
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

class DownloadAudioAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'url': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='URL of the video.',
                ),
                'bitrate': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Audio quality. Use the /search/qualities api to determine available qualities',
                ),
            },
            required=['url']
        ),
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
    def post(self, request, *args, **kwargs):
        try:
            downloadable: Downloadable = dlaud(
                request.data.get('url', ''),
                request.data.get('bitrate')
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
        except UnavailableVideoQualityException:
            return Response(
                {
                    "message": "Invalid/Unavailable audio bitrate"
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
