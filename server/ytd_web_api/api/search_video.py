from ytd_web_core.search_video import search as _search_youtube
from ytd_web_core import Status
from rest_framework.views import APIView, Response
from ..serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class SearchVideoAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'keyword': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='search keywod',
                ),
            },
            required=['keyword']
        ),
        responses={
            200: openapi.Response(
                description='Successful response',
                schema=SearchResultsSerializer,
            ),
            403: 'Invalid API key',
            500: 'Internal error'
        }
    )
    def post(self, request, *args, **kwargs):
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
                        SingleSearchResultSerializer(search_result.JsonSerialize()).data for search_result in results
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
