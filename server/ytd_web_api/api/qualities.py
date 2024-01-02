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
                description="""ID of the YouTube video. Either this or the url parameter is required. 
                    If both are provided, video_id will be used.""",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'url',
                openapi.IN_QUERY,
                description='URL of the video. Either this or the video_id parameter is required.',
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="""Returns a list of available qualities. 
                Audio qualities will be in kbps and video qualities will be in
                either progressive or adaptive resolutions.""",
                schema=QualitiesSerializer,
            ),
            403: 'Invalid API key',
            403: 'Age Restricted',
            500: 'Internal error'
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            assert request.GET.get('video_id') is not None or request.GET.get('url') is not None
            
            return Response(
                QualitiesSerializer(get_qualities(
                    get_url_from_video_id(request.GET.get('video_id')) if request.GET.get('video_id') is not None else request.GET.get('url')
                )).data
            )
        except AgeRestrictedVideoException:
            return Response(
                {
                    "message": "Age restricted video"
                },
                status = 403
            )
        except AssertionError:
                return Response(
                    {
                        "message": "video_id or url parameter is required"
                    },
                    status = 400
                )
        except Exception as e:
            return Response(
                {
                    "message": "Internal server error",
                    "error": str(e)
                },
                status = 500
            )
