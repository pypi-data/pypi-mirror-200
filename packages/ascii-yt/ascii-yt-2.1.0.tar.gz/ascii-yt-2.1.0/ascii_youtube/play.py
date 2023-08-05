import os, sys
from time import sleep
from . import ascii_frames as af
from yt_dlp.utils import DownloadError
from urllib.parse import parse_qs, urlencode, urlparse
from cap_from_youtube import cap_from_youtube as youtube_cap

YT_HOSTNAMES = ['youtu.be', 'www.youtube.com']

def get_youtube_url(url: str):
    # Parse the URL to extract the query string
    parsed_url = urlparse(url)

    # check if it's a youtube URL
    if parsed_url.hostname not in YT_HOSTNAMES:
        af.raise_error((f"'{url}' is not a youtube URL."))

    # get the yt video ID
    query_params = parse_qs(parsed_url.query)
    if query_params.get('v'):
        video_id = query_params['v']
        query_params.clear()
        query_params['v'] = video_id

    # Reconstruct the URL with the modified query string
    encoded_query = urlencode(query_params, doseq=True)
    new_url = parsed_url._replace(query=encoded_query).geturl()

    return new_url

def get_video_capture(url: str):
    try:
        # extract the URL and download the video
        return youtube_cap(url)
    except DownloadError:
        sys.exit(1)
    

def play(url: str, size=None, chars="", colors=False):
    video_url = get_youtube_url(url)
    video_capture = get_video_capture(video_url)

    os.system("clear")
    DELAY = 0.01

    while True:
        success, frame = video_capture.read()
        if success:
            print('\x1b[H' + af.image2ascii(frame, size, chars, colors))
            sleep(DELAY)
        else: 
            return

