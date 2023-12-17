from ytd_web_core.exceptions import AgeRestrictedVideoException
from ytd_web_core.util import get_url_from_video_id
from ytd_web_core.get_qualities import get_qualities
from rest_framework.views import APIView, Response
from ..serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
