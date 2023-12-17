from ytd_web_core.search_video import search as _search_youtube
from ytd_web_core import Status
from rest_framework.views import APIView, Response
from ..serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
