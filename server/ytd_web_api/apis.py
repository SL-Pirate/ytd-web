from ytd_web_core.download_video import download_video as dlvid
from ytd_web_core.download_video import VideoFormat
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

        return Response(SearchResultsSerializer(
            {
                "results": [
                    {
                        "video_id": "v6IAJOOmDMg",
                        "title": "The Chainsmokers, XYLØ - Setting Fires (Lyric) ft. XYLØ",
                        "description": "The Chainsmokers debut album 'Memories... Do Not Open' is out now! Buy & Stream: http://smarturl.it/TCSMemories Physical CD: ...",
                        "thumbnail_url": "http://localhost:8000/proxy?url=https://i.ytimg.com/vi/v6IAJOOmDMg/hqdefault.jpg",
                        "channel_name": "ChainsmokersVEVO",
                        "channel_thumbnail_url": "http://localhost:8000/proxy?url=https://yt3.ggpht.com/7LLsTxYTnoAUm3zd4ANd9xh1Tr5VhDkBesxTQhn1QWAEW3Eii-CTxlzthvi1qpyD-gN1dU1pgkc=s88-c-k-c0x00ffffff-no-nd-rj"
                        # "channel_thumbnail_url": None
                    },
                    {
                        "video_id": "TKJrq_hS0_g",
                        "title": "The Chainsmokers, XYLØ - Setting Fires (Lyrics)",
                        "description": "Follow 7clouds on Spotify : http://bit.ly/7CLOUDS The Chainsmokers, XYLØ - Setting Fires (Lyrics) ⏬ Download / Stream: ...",
                        "thumbnail_url": "http://localhost:8000/proxy?url=https://i.ytimg.com/vi/TKJrq_hS0_g/hqdefault.jpg",
                        "channel_name": "7clouds",
                        "channel_thumbnail_url": "http://localhost:8000/proxy?url=https://yt3.ggpht.com/bhG7T_FzfLoxqmJwGobKF1B9u9FhIXiYA8JYRPPoHcOASht0psOD3LZHZ3HqPEICEn30FWkDfg=s88-c-k-c0x00ffffff-no-rj"
                    },
                    {
                        "video_id": "ZrM9JmKwpHs",
                        "title": "The Chainsmokers, XYLØ - Setting Fires (Acoustic Version) ft. XYLØ",
                        "description": "Collage EP OUT NOW: http://smarturl.it/TCSCollage Urban Outfitters White Vinyl: http://smarturl.it/CollageVinyl Amazon Physical: ...",
                        "thumbnail_url": "http://localhost:8000/proxy?url=https://i.ytimg.com/vi/ZrM9JmKwpHs/hqdefault.jpg",
                        "channel_name": "ChainsmokersVEVO",
                        "channel_thumbnail_url": "http://localhost:8000/proxy?url=https://yt3.ggpht.com/7LLsTxYTnoAUm3zd4ANd9xh1Tr5VhDkBesxTQhn1QWAEW3Eii-CTxlzthvi1qpyD-gN1dU1pgkc=s88-c-k-c0x00ffffff-no-nd-rj"
                    },
                    {
                        "video_id": "jWhV70gVTEo",
                        "title": "The Chainsmokers - Setting Fires ft. XYLØ",
                        "description": "Proximity - Your favorite music you haven't heard yet. » Spotify!: http://spoti.fi/Proximity » Facebook: http://bit.ly/FBProximity The ...",
                        "thumbnail_url": "http://localhost:8000/proxy?url=https://i.ytimg.com/vi/jWhV70gVTEo/hqdefault.jpg",
                        "channel_name": "Proximity",
                        "channel_thumbnail_url": "http://localhost:8000/proxy?url=https://yt3.ggpht.com/ytc/AIf8zZTc6BcK0_84_i5alboja5Ca6XKP9W1qYa80AxnVcw=s88-c-k-c0x00ffffff-no-rj"
                    },
                    {
                        "video_id": "7UWf6sQU4oQ",
                        "title": "The Chainsmokers Ft. XYLØ - Setting Fires (it&#39;s different Remix)",
                        "description": "Trap City Merch: http://trapcity.tv/shop Subscribe here: http://trapcity.tv/subscribe Buy / Stream the original: https://trapcity.tv/2w8YX ...",
                        "thumbnail_url": "http://localhost:8000/proxy?url=https://i.ytimg.com/vi/7UWf6sQU4oQ/hqdefault.jpg",
                        "channel_name": "Trap City",
                        "channel_thumbnail_url": "http://localhost:8000/proxy?url=https://yt3.ggpht.com/E8WhdAlUKLu36Zx2Y46Q3NoLxvPzQ4VxPV8QlHlISy2Kdn_nEnIOYWUV4deOq36-ACXJEfUu9F8=s88-c-k-c0x00ffffff-no-rj"
                    },
                    {
                        "video_id": "R0mZdxMrHhQ",
                        "title": "The Chainsmokers, XYLØ - Setting Fires (Audio Clip) ft. XYLØ",
                        "description": "The Chainsmokers debut album 'Memories... Do Not Open' is out now! Buy & Stream: http://smarturl.it/TCSMemories Physical CD: ...",
                        "thumbnail_url": "http://localhost:8000/proxy?url=https://i.ytimg.com/vi/R0mZdxMrHhQ/hqdefault.jpg",
                        "channel_name": "ChainsmokersVEVO",
                        "channel_thumbnail_url": "http://localhost:8000/proxy?url=https://yt3.ggpht.com/7LLsTxYTnoAUm3zd4ANd9xh1Tr5VhDkBesxTQhn1QWAEW3Eii-CTxlzthvi1qpyD-gN1dU1pgkc=s88-c-k-c0x00ffffff-no-nd-rj"
                    },
                    {
                        "video_id": "oc64W6N9U2I",
                        "title": "The Chainsmokers, XYLØ - Setting Fires (Sigma Remix Audio) ft. XYLØ",
                        "description": "The Chainsmokers debut album 'Memories... Do Not Open' is out now! Buy & Stream: http://smarturl.it/TCSMemories Physical CD: ...",
                        "thumbnail_url": "http://localhost:8000/proxy?url=https://i.ytimg.com/vi/oc64W6N9U2I/hqdefault.jpg",
                        "channel_name": "ChainsmokersVEVO",
                        "channel_thumbnail_url": "http://localhost:8000/proxy?url=https://yt3.ggpht.com/7LLsTxYTnoAUm3zd4ANd9xh1Tr5VhDkBesxTQhn1QWAEW3Eii-CTxlzthvi1qpyD-gN1dU1pgkc=s88-c-k-c0x00ffffff-no-nd-rj"
                    },
                    {
                        "video_id": "DEJAd7Zp87U",
                        "title": "The Chainsmokers ft. XYLØ - Setting Fires (VANIC Remix)",
                        "description": "The Chainsmokers ft. XYLØ - Setting Fires (VANIC Remix) STREAM NOW: https://trapnation.komi.io The Chainsmokers ...",
                        "thumbnail_url": "http://localhost:8000/proxy?url=https://i.ytimg.com/vi/DEJAd7Zp87U/hqdefault.jpg",
                        "channel_name": "Trap Nation",
                        "channel_thumbnail_url": "http://localhost:8000/proxy?url=https://yt3.ggpht.com/ZoViy6jSW8lGsT7Fgz7PsxsWznVseOVjGNkqh9U34cJ-7eXAGs_f2s0yCWwgxsxZT6d7icafVr8=s88-c-k-c0x00ffffff-no-rj"
                    },
                    {
                        "video_id": "kclCH4yINhM",
                        "title": "The Chainsmokers ft. XYLØ - Setting Fires",
                        "description": "Purchase/Stream it here: http://smarturl.it/TCSCollage The Chainsmokers with XYLØ, DAMN what a collab!! Literally fire ...",
                        "thumbnail_url": "http://localhost:8000/proxy?url=https://i.ytimg.com/vi/kclCH4yINhM/hqdefault.jpg",
                        "channel_name": "xKito Music",
                        "channel_thumbnail_url": "http://localhost:8000/proxy?url=https://yt3.ggpht.com/i6xNr7EQzSvIOZ2E4BC2twnqlFqi-QeruOUDQOM0pgPC7OvygMKHCnXDqDgJe-DTgACJbtALMQ=s88-c-k-c0x00ffffff-no-rj"
                    },
                    {
                        "video_id": "54HTh0HP-s8",
                        "title": "Setting Fires - The Chainsmokers ft. XYLØ / Yoojung Lee Choreography",
                        "description": "Yoojung teaches choreography to Setting Fires by The Chainsmokers ft. XYLØ . Learn from instructors of 1MILLION Dance Studio ...",
                        "thumbnail_url": "http://localhost:8000/proxy?url=https://i.ytimg.com/vi/54HTh0HP-s8/hqdefault.jpg",
                        "channel_name": "1MILLION Dance Studio",
                        "channel_thumbnail_url": "http://localhost:8000/proxy?url=https://yt3.ggpht.com/ytc/AIf8zZRvDNBJNIlVV_beH50MXTiJwDiiHC1PyAxApEDMRA=s88-c-k-c0x00ffffff-no-rj"
                    }
                ]
            }
        ).data)

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
