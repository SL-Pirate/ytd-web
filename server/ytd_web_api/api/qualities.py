from ytd_web_core.exceptions import AgeRestrictedVideoException
from ytd_web_core.util import get_url_from_video_id
from ytd_web_core.get_qualities import get_qualities
from rest_framework.views import APIView, Response
from ..serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class GetQualitiesAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'url': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='URL of the video.',
                ),
            },
            required=['url']
        ),
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
    def post(self, request, *args, **kwargs):
        try:
            return Response(
                QualitiesSerializer(get_qualities(request.data.get('url'))).data
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
