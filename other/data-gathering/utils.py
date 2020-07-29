import mysql.connector
import string
import requests # to get image from the web
import shutil # to save it locally
import datetime
import os


import string
from html.parser import HTMLParser


class WikiThumbailExtractor(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self._inbody = False
        self._ininfobox = False
        self._url = ""

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            _inbody = True

        if tag == "table":
            for attr in attrs:
                if attr[0] == "class" and str(attr[1]).__contains__("infobox"):
                    self._ininfobox = True
                    return

        if self._ininfobox and tag == "img":
            for attr in attrs:
                if attr[0] == "src":
                    self._url = attr[1]
                    self._inbody = False
                    self._ininfobox = False
                    return

    def handle_endtag(self, tag):
        pass

    def get_img_src(self):
        return self._url


def database_connect():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="historyguessr"
    )
    return mydb

def download_image(url):
    if url.__contains__(".svg"):
        return False

    ## Set up the image URL and filename
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    storage_dir = "../../back/storage/app/public/img/"
    filename = str(datetime.datetime.now().timestamp()) + "." + url.split('.')[-1]
    file_path = os.path.join(script_dir, storage_dir + filename)

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(url, stream = True)

    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        
        # Open a local file with wb ( write binary ) permission.
        with open(file_path,'wb') as f:
            shutil.copyfileobj(r.raw, f)
            
        return filename
    else:
        print("Error in download_image")
        return False


def try_parse_year(string, blank_space_only=False):
    blank_space = string.split(' ')
    for token in blank_space:
        try:
            return int(token)
        except Exception:
            ""

    if not blank_space_only:

        u_space = string.split('\u2013')
        for token in u_space:
            try:
                return int(token)
            except Exception:
                ""

        dash_space = string.split('-')
        for token in u_space:
            try:
                return int(token)
            except Exception:
                ""

    raise Exception("Can't parse")