from time import sleep
import os
from ytd_helper import keep_time, max_vids
import threading
from pytube import YouTube as yt
from os import mkdir
from ytd_helper.error import *
from subprocess import run as cmd

class Helper:
    # constants for temporary naming or src files
    num_vids: int = 0

    def __init__(self, session):
        self.session = session

    @staticmethod
    def getName():
        if Helper.num_vids > max_vids:
            Helper.num_vids = 0
        ID = Helper.num_vids
        Helper.num_vids += 1
        return "vid" + str(ID) + ".mp4"
    

    # Cleaning downloaded files to save storage
    @staticmethod
    def cleanFunc(item):
        sleep(keep_time * 60)
        try:
            os.remove(item)
        except FileNotFoundError:
            pass
    
    @staticmethod
    def clean(item):
        clean_thread = threading.Thread(target=Helper.cleanFunc, args=(item, ))
        clean_thread.start()

    def downloader(
            self,
            link: str=None,
            resolution: str=None,
            quality: str=None
            ) -> list[any]:
        '''
            return:
                [
                    video title: str,
                    link to the thumbnail of the video: str,
                    available video resolutions: list(str),
                    available audio qualities: list(str),
                    video_link: str
                ]
        '''

        if (link == None):
            link = self.session['yt_link']
        else:
            self.session["yt_link"] = link

        self.session["reso"] = resolution
        self.session['qual'] = quality
        yt_vid = yt(link)
        tit = yt_vid.title
        img = yt_vid.thumbnail_url

        # Querring resolutions and qualities
        buttons = None
        buttons_audio = None
        if (resolution == None and quality == None):
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

        return [tit, img, buttons, buttons_audio, link]

    def process_video(self) -> None:
        reso = self.session['reso']
        yt_vid = yt(self.session['video'][4])
        vid_file = yt_vid.streams.filter(res=str(reso)).first()
        aud_file = yt_vid.streams.filter(only_audio=True).first()
        name = Helper.getName()
        in_vid = "./web/yt_temp/vid"
        in_aud = "./web/yt_temp/aud"
        out = "./web/yt_temp/final"
        out_file = vid_file.download(in_vid)
        self.session['out_file'] = out_file
        try:
            os.rename(out_file, in_vid + "/" + name)
        except FileExistsError:
            os.remove(in_vid + name)
            os.rename(out_file, in_vid + "/" + name)
        aud_file.download(in_aud, name)

        try:
            mkdir(out)
        except FileExistsError:
            pass

        try:               
            stream = name
            ffmpeg_command = 'ffmpeg -i "'+str(in_vid)+'/'+str(stream)+'" -i "'+str(in_aud)+'/'+str(stream)+'" -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -y "'+str(out)+'/'+str(stream)+'"'
            cmd(str(ffmpeg_command) ,shell=True)
            try:
                os.rename(out + '/' + name, out_file)
            except FileExistsError:
                os.remove(out_file)
                os.rename(out + '/' + name, out_file)
            Helper.clean(out_file)
            
        except FileNotFoundError:
            raise VideoProcessingFailureException()
        except Exception as e:
            raise VideoProcessingFailureException(str(e))

    def process_audio(self) -> None:
        try:
            qual = self.session['qual']
            yt_vid = yt(self.session['video'][4])
            aud_file = yt_vid.streams.filter(abr=str(qual)).first()
            out_path = "web/yt_temp/aud"
            out: str = aud_file.download(out_path)
            pre, ext = os.path.splitext(out)
            out_file = out.replace(ext, ".mp3")
            try:
                os.rename(out, pre + ".mp3")
            except FileExistsError:
                os.remove(out_file)
                os.rename(out, pre + ".mp3")

            self.session['out_file'] = out_file
            print(out)
            print(out_file)
        except Exception as e:
            raise AudioProcessingFailureException(str(e))

        Helper.clean(out_file)