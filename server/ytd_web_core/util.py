from shutil import rmtree
from ytd_web_core import max_vids
import base64

num_vids = 0

def get_name() -> str:
    global num_vids
    if num_vids > max_vids:
        num_vids = 0
    ID = num_vids
    num_vids += 1
    return "vid" + str(ID) + ".mp4"

# Cleaning downloaded files to save storage
def clean_immediate(item) -> None:
    try:
        rmtree(item, ignore_errors=True)
    except FileNotFoundError:
        pass

def get_url_from_video_id (video_id) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"

def str_to_base64(string: str) -> str:
    if string is None:
        return None
    return base64.b64encode(bytes(string, 'utf-8')).decode('utf-8')

def base64_to_str(string: str) -> str:
    if string is None:
        return None
    return base64.b64decode(string).decode('utf-8')
