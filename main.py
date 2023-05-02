#!/usr/bin/env python

from flask import Flask, redirect, render_template, url_for, request, session, send_file, after_this_request
from pytube import YouTube as yt
from pytube.exceptions import RegexMatchError
from subprocess import run as cmd
from os import mkdir
import os
from time import sleep
import threading

app = Flask(__name__)

cmd("which python", shell=True)


#### CONFIG VARIABLES ####
# Maximum number of videos that can exists.
# This number should be adjusted according to the requirement and capabilities (mostly Disk space capacity) of the host machiene
max_vids = 1

# Time duration a particular downloadable video file is kept on the host system (in minuites).
# This value should be set depending on the usage and the disk space capabilities.
keep_time = 1


############################


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

# # Formatting video file titles to remove invalid characters for ffmpeg
# def getFormattedTitle(unformatted_title) :
#         tit = unformatted_title
#         tit = tit.replace(".", "")
#         tit = tit.replace(":", "")
#         tit = tit.replace("|", "")
        
#         return f"{tit}.mp4"

def downloader():
    link = session['yt_link']
    yt_vid = yt(link)
    t=5
    while t > 0:
        try:
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

            break
        except:
            t -= 1
            if t==0:
                return redirect ("/Error")
            else:
                continue
    return tit, img, buttons, buttons_audio, yt_vid

@app.route("/video")
def download_vid():
    session['reso'] = request.args.get("reso")
    return render_template("downloading.html")

@app.route("/audio")
def download_aud():
    session['qual'] = request.args.get("qual")
    return render_template("downloading_aud.html")

@app.route("/download")
def export():
    reso = session['reso']
    yt_vid = downloader()[4]
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
        os.rename(out + '/' + stream, out + '/' + downloader()[0] + ".mp4")
        clean(out + '/' + downloader()[0] + ".mp4")
        return render_template("get_file.html")
    except FileNotFoundError as e:
        return render_template("went_wrong.html", exception=e)
        

@app.route("/download_aud")
def export_aud():
    qual = session['qual']
    yt_vid = downloader()[4]
    aud_file = yt_vid.streams.filter(abr=str(qual)).first()
    loc = "./web/yt_temp/aud"
    out_file = aud_file.download(loc)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    try:
        os.rename(out_file, new_file)
    except FileExistsError:
        try:
            os.remove(new_file)
            os.rename(out_file, new_file)
        except Exception as e:
            return render_template("went_wrong.html", exception=e)
    clean(new_file)
    return render_template("get_file_aud.html")

@app.route("/get")
def file_get():
    tit = downloader()[0]
    try:
        down_file = f"web/yt_temp/final/{tit}.mp4"
        return send_file(down_file, as_attachment=True)
    except Exception as e:
        return render_template("went_wrong.html", exception=e)

@app.route("/get_aud")
def file_get_aud():
    tit = downloader()[0]
    try:
        audio_file = f'web/yt_temp/aud/{tit}.mp3'
        return send_file(audio_file, as_attachment=True)
    except FileNotFoundError as e:
        return render_template("went_wrong.html", exception=e)


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
    else:
        return render_template("index.html")

@app.route("/Error")
def not_found():
    return render_template("error.html")

@app.route("/test")
def test():
    reso = request.args.get("reso")
    return f"test pass. this works. {reso}"

@app.route("/select")
def select():
    if "yt_link" in session:
        try:
            return render_template("select.html", vid_tit=downloader()[0], vid_img=downloader()[1], buttons=downloader()[2], buttons_aud=downloader()[3])
        except RegexMatchError:
            return redirect("/Error")
    else:
        return redirect("/main")

if __name__ == "__main__":
    app.secret_key = 'DqdZrlQE+hyrg?SSEn@N0jPb8/>&`7'
    app.run(debug=True, host='0.0.0.0')
