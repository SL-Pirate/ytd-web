#!/usr/bin/env python

from flask import Flask, redirect, render_template, url_for, request, session, send_file
from pytube import YouTube as yt
from pytube.exceptions import RegexMatchError
from subprocess import run as cmd
from os import mkdir
import os
from time import sleep
import threading
import requests
from search_result import SearchResult
from configparser import ConfigParser
from errors import *
import traceback

app = Flask(__name__)

# google API key for accessing youtube data api
config = ConfigParser()

config.read('secrets.key')
googleApiKey = config['googleApiKey']['key']

config.read('server.cfg')
max_vids: int = int(config['DEFAULT']['max_vids'])
keep_time: int = int(config["DEFAULT"]['keep_time'])
api_server_root: str = config["DEFAULT"]["api_server_root"]

app.secret_key = config["session"]['key']

num_vids = 0

def getName():
    global num_vids, max_vids
    if num_vids > max_vids:
        num_vids = 0
    ID = num_vids
    num_vids += 1
    return "vid" + str(ID) + ".mp4"

# Cleaning downloaded files to save storage
def cleanFunc(item):
    sleep(keep_time * 60)
    try:
        os.remove(item)
    except FileNotFoundError:
        pass

def clean(item):
    clean_thread = threading.Thread(target=cleanFunc, args=(item, ))
    clean_thread.start()

def downloader():
    link = session['yt_link']
    yt_vid = yt(link)
    # if yt_vid.age_restricted:
    #     print("age restrictedZ")
    #     raise Exception("video is age restricted")
    tit = yt_vid.title
    img = yt_vid.thumbnail_url
    vid_stream = yt_vid.streams.filter(mime_type="video/mp4")
    aud_stream = yt_vid.streams.filter(type="audio")

    button_set = {}
    button_set = set()
    for stream in vid_stream:
        button_set.add(str(stream.resolution))
    buttons = list(button_set)
    buttons.sort()

    button_set_audio = {}
    button_set_audio = set()
    for stream in aud_stream:
        button_set_audio.add(str(stream.abr))
    buttons_audio = list(button_set_audio)
    buttons_audio.sort()

    return tit, img, buttons, buttons_audio, link

def downloader_via_api(yt_link: str, resolution: str):
    session["yt_link"] = yt_link
    session["reso"] = resolution
    yt_vid = yt(yt_link)
    tit = yt_vid.title
    img = yt_vid.thumbnail_url

    return tit, img, None, None, yt_link

@app.route("/video")
def download_vid():
    if ("yt_link" in session.keys()):
        session['reso'] = request.args.get("reso")
        return render_template("downloading.html")
    else:
        return redirect("/home")

@app.route("/audio")
def download_aud():
    if ("yt_link" in session.keys()):
        session['qual'] = request.args.get("qual")
        return render_template("downloading_aud.html")
    else:
        return redirect("/home")

@app.route("/download")
def export():
    if ("yt_link" in session.keys()):
        try:
            process_video()
            return render_template("get_file.html", file_link="file_get", keep_time=keep_time)
        except VideoProcessingFailureException as e:
            return render_template("went_wrong.html", exception=e)
    else:
        return redirect("/home")

def process_video() -> None:
    reso = session['reso']
    yt_vid = yt(session['video'][4])
    vid_file = yt_vid.streams.filter(res=str(reso)).first()
    aud_file = yt_vid.streams.filter(only_audio=True).first()
    name = getName()
    vid_file.download("./web/yt_temp/vid", name)
    aud_file.download("./web/yt_temp/aud", name)
    in_vid = "./web/yt_temp/vid"
    in_aud = "./web/yt_temp/aud"
    out = "./web/yt_temp/final"
    try:
        mkdir(out)
    except FileExistsError:
        pass

    try:               
        stream = name
        #convert(stream)
        ffmpeg_command = 'ffmpeg -i "'+str(in_vid)+'/'+str(stream)+'" -i "'+str(in_aud)+'/'+str(stream)+'" -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -y "'+str(out)+'/'+str(stream)+'"'
        cmd(str(ffmpeg_command) ,shell=True)
        os.rename(out + '/' + stream, out + '/' + session['video'][0] + ".mp4")
        clean(out + '/' + session['video'][0] + ".mp4")
        
    except FileNotFoundError:
        raise VideoProcessingFailureException()
        

@app.route("/download_aud")
def export_aud():
    if ("yt_link" in session.keys()):
        try:
            process_video()
            return render_template("get_file.html", file_link="file_get_aud", keep_time=keep_time)
        except AudioProcessingFailureException as e:
            return render_template("went_wrong.html", exception=e)
    else:
        return redirect("/home")

def process_audio() -> None:
    qual = session['qual']
    yt_vid = yt(session['video'][4])
    aud_file = yt_vid.streams.filter(abr=str(qual)).first()
    loc = "./web/yt_temp/aud"
    out_file = aud_file.download(loc)
    base = os.path.splitext(out_file)
    new_file = base + '.mp3'
    try:
        os.rename(out_file, new_file)
    except FileExistsError:
        try:
            os.remove(new_file)
            os.rename(out_file, new_file)
        except Exception as e:
            raise AudioProcessingFailureException(str(e))
    clean(new_file)

    

@app.route("/get")
def file_get():
    if ("yt_link" in session.keys()):
        tit = session['video'][0]
        try:
            down_file = f"web/yt_temp/final/{tit}.mp4"
            return send_file(down_file, as_attachment=True)
        except FileNotFoundError as e:
            return render_template("link_expired.html")
        except Exception as e:
            return render_template("went_wrong.html", exception=e)
    else:
        return redirect("/home")

@app.route("/get_aud")
def file_get_aud():
    if ("yt_link" in session.keys()):
        tit = session['video'][0]
        try:
            audio_file = f'web/yt_temp/aud/{tit}.mp3'
            return send_file(audio_file, as_attachment=True)
        except FileNotFoundError as e:
            return render_template("link_expired.html")
        except Exception as e:
            return render_template("went_wrong.html", exception=e)
    else:
        return redirect("/home")
    
# _____________________Search Video Page____________________

@app.route("/browse")
def browse():
    if ("search_term" in session.keys()):
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
            request_url = f"https://youtube.googleapis.com/youtube/v3/search?part=id%2Csnippet&maxResults=5&q={session['search_term']}&regionCode={region_code}&type=video&key={googleApiKey}"
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

                return render_template("browse.html", search_term=session['search_term'], results=search_result_objs)
            else:
                return redirect("/Error")
        except Exception as e:
            return render_template("went_wrong.html", exception=e)
    else:
        return redirect("/home")

# _____________________HOME PAGE___________________________

@app.route("/", methods=['POST', 'GET'])
@app.route("/main", methods=['POST', 'GET'])
@app.route("/home", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        yt_link = request.form['link']
        if yt_link == "":
            return redirect("#")
        else:
            session['yt_link'] = yt_link
            return redirect("/select")
    elif request.method == "GET":
        try:
            yt_link = request.args.get('link')
            if yt_link == None or yt_link == "":
                return render_template("index.html")
            session['yt_link'] = yt_link
            return redirect("/select")
        except ValueError:
            return render_template("index.html")
    else:
        return render_template("index.html")

@app.route("/Error")
def not_found():
    if ("yt_link" in session.keys()):
        return render_template("error.html")
    else: 
        return redirect("/home")

@app.route("/select")
def select():
    if "yt_link" in session:
        try:
            session['video'] = downloader()
            return render_template("select.html", vid_tit=session['video'][0], vid_img=session['video'][1], buttons=session['video'][2], buttons_aud=session['video'][3])
        except RegexMatchError:
            session['search_term'] = session['yt_link']
            return redirect("/browse")
        except Exception as e:
            return render_template("went_wrong.html", exception=e)
            
    else:
        return redirect("/main")

# _____________________ API FOR DIREC VIDEO DOWNLOADING WITH LINK _________________________
api_key = "some gibberish here"
@app.route("/get_video", methods=['POST'])
def getVideo():
    '''
        request 
        {
            "key": "api key",
            "video_link": "video link",
            "resolution": "resolution"
        }

        response 
        {
            "status": status_code,
            "title": "video title",
            "resolution": "video resolution",
            "format": "video format"
            "download_link": "download_link"
        }
    '''
    for item in ("key", "video_link", "resolution"):
        if item not in request.args.keys():
            return {'status': 416, 'request': request.args, "description": f"missing key: {item}"}, 416
    
    if request.args.get('key') == api_key:
        try:
            dl = downloader_via_api(request.args.get("video_link"), request.args.get("resolution"))
            session["video"] = dl
            try:
                process_video()
                return {'status': 200, 'title': dl[0], 'resolution': request.args.get('resolution'), 'format': "mp4", 'download_link': api_server_root + url_for("download_from_link", file_name=f"{dl[0]}.mp4")}
            except AttributeError:
                return {'status': 404, 'description': "Resolution " + request.args.get("resolution") + " not found"}
            except Exception as e:
                print(traceback.format_exc())
                return {'status': 500,"description": str(e)}, 500
        except RegexMatchError:
            return {'status': 404, 'description': "Invalid URL"}, 404
    
    else:
        return {'status': 401,"description": "Invalid API Key"}, 401
    
@app.route("/download/path", methods=['GET'])
def download_from_link():
    return send_file(f"./web/yt_temp/final/{request.args.get('file_name')}", as_attachment=True)

# for testing purposes
if __name__ == "__main__":
    app.run(debug=True, port=5000)
