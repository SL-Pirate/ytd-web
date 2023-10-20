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

def download_video(request) -> JsonResponse:
    try:
        downloadable: Downloadable = dlvid(
            get_url_from_video_id(request.GET.get('video_id', '')),
            request.GET.get('resolution', ''),
        )

        server_ip = request.build_absolute_uri().split("/api")[0]

        return JsonResponse({
            "downloadable_link": f"{server_ip}/downloads/{downloadable.id}/",
            "file_name": downloadable.name,
            "valid for": downloadable.expiration_period
        })
    except RegexMatchError:
        return JsonResponse(
            {
                "message": "Invalid link format! Please check again"
            },
            status = 404
        )
    except AgeRestrictedVideoException:
        return JsonResponse(
            {
                "message": "This video is age restricted!"
            },
            status = 404
        )
    except VideoUnavailable:
        return JsonResponse(
            {
                "message": "video unavailable"
            },
            status = 404
        )


def get_qual(request) -> JsonResponse:
    try:
        return JsonResponse(
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
        return JsonResponse(
            {
                "message": "Age restricted video"
            },
            status = 403
        )
    except Exception as e:
        return JsonResponse(
            {
                "message": "Internal server error",
                "error": e
            },
            status = 500
        )



def search(request) -> JsonResponse:
    results = _search_youtube(request)
    if (results[0].get_status() != Status.FAILURE):
        return JsonResponse(
            {
                "results": [search_result.JsonSerialize() for search_result in results]
            }
        )

    else:
        return JsonResponse(
            {
                "message": "Failed to connect with youtube"
            },
            status = 500
        )
