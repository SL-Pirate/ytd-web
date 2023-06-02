from flask import request, render_template, redirect, Blueprint
import requests
from ytd_helper.search_result import SearchResult
from ytd_helper import googleApiKey

browse_page = Blueprint('browse_page', __name__)

# _____________________Search Video Page____________________
@browse_page.route("/browse", methods=["GET"])
def browse():
    if (request.args.get("q") != None and request.args.get("q") != ""):
        try:
            # Getting user's region code
            region_code = "US" # defaulting to US
            user_ip = request.remote_addr
            try:
                location_response = requests.get(f"https://ipinfo.io/{user_ip}/json")
                if location_response:
                    region_code = location_response.json()['country']
            except Exception:
                pass
            request_url = f"https://youtube.googleapis.com/youtube/v3/search?part=id%2Csnippet&maxResults=5&q={request.args.get('q')}&regionCode={region_code}&type=video&key={googleApiKey}"
            response = requests.get(request_url)
            if response:
                result = response.json()

                # decoding the json
                search_results = result['items']
                search_result_objs = list()
                for search_result in search_results:
                    search_result_objs.append(SearchResult(
                        search_result['id']['videoId'], 
                        search_result['snippet']['title'], 
                        # description=search_result['snippet']['description'], 
                        thumbnail_link=search_result['snippet']['thumbnails']['high']['url'],
                        channel_name=search_result['snippet']['channelTitle']
                    ))

                return render_template("browse.html", q=request.args.get('q'), results=search_result_objs)
            else:
                return redirect("/Error")
        except Exception as e:
            return render_template("went_wrong.html", exception=e)
    else:
        return redirect("/home")
