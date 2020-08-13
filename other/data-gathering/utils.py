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

def database_clean_unique_years():
    db = database_connect()
    cursor = db.cursor()
    cursor.execute('SELECT year, COUNT(year) FROM images GROUP BY year')
    years = cursor.fetchall()
    for row in years:
        if row[1] < 2 or row[0] <= 31:
            cursor.execute('DELETE FROM images WHERE year = %(year_to_del)s', {'year_to_del': int(row[0])})
    db.commit()

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

import time
import pytrends
from pytrends.request import TrendReq
import pandas as pd

comp_number = 0

def merge(array, left_index, right_index, middle, pytrend):
    # Make copies of both arrays we're trying to merge

    # The second parameter is non-inclusive, so we have to increase by 1
    left_copy = array[left_index:middle + 1]
    right_copy = array[middle+1:right_index+1]

    # Initial values for variables that we use to keep
    # track of where we are in each array
    left_copy_index = 0
    right_copy_index = 0
    sorted_index = left_index

    sleep_time = 0.1
    global comp_number

    '''
    reset1 = False
    reset2 = False
    '''

    # Go through both copies until we run out of elements in one
    while left_copy_index < len(left_copy) and right_copy_index < len(right_copy):
        time.sleep(sleep_time)
        keywords = [left_copy[left_copy_index][1], right_copy[right_copy_index][1]]
        try:
            pytrend.build_payload(keywords, cat=0, timeframe='today 1-m', geo='', gprop='')
            values = pytrend.interest_over_time().cumsum()
        except (pytrends.exceptions.ResponseError, requests.exceptions.ReadTimeout):
            '''
            if sleep_time > 30 and not reset1:
                sleep_time = 1
                reset1 = True
            elif sleep_time > 45 and not reset2:
                sleep_time = 1
                reset2 = True
            else:
                sleep_time+=1
            '''
            if pytrend.proxy_index <= (len(pytrend.proxies) - 1):
                print(pytrend.proxies[pytrend.proxy_index])
            pytrend.GetNewProxy()
            continue
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ProxyError, requests.exceptions.ConnectionError):
            if pytrend.proxy_index <= (len(pytrend.proxies) - 1):
                print(pytrend.proxies[pytrend.proxy_index])
            pytrend.GetNewProxy()
            continue
        # If our left_copy has the smaller element, put it in the sorted
        # part and then move forward in left_copy (by increasing the pointer)

        try:
            comp_result = values.iloc[-1][keywords[0]] <= values.iloc[-1][keywords[1]]
        except IndexError:
            comp_result = True

        if comp_result:
            array[sorted_index] = left_copy[left_copy_index]
            left_copy_index = left_copy_index + 1
        # Opposite from above
        else:
            array[sorted_index] = right_copy[right_copy_index]
            right_copy_index = right_copy_index + 1

        # Regardless of where we got our element from
        # move forward in the sorted part
        sorted_index = sorted_index + 1

        if pytrend.proxy_index <= (len(pytrend.proxies) - 1):
            print(pytrend.proxies[pytrend.proxy_index])

        comp_number+=1
        print('Nombre de comparaisons : ', comp_number)

    # We ran out of elements either in left_copy or right_copy
    # so we will go through the remaining elements and add them
    while left_copy_index < len(left_copy):
        array[sorted_index] = left_copy[left_copy_index]
        left_copy_index = left_copy_index + 1
        sorted_index = sorted_index + 1

    while right_copy_index < len(right_copy):
        array[sorted_index] = right_copy[right_copy_index]
        right_copy_index = right_copy_index + 1
        sorted_index = sorted_index + 1

def trends_merge_sort(keywords, left_index, right_index, pytrends):
    if left_index >= right_index:
        return

    middle = (left_index + right_index)//2
    trends_merge_sort(keywords, left_index, middle, pytrends)
    trends_merge_sort(keywords, middle + 1, right_index, pytrends)
    merge(keywords, left_index, right_index, middle, pytrends)

def custom_merge_sort(keywords):
    proxies = []
    with open('./other/data-gathering/proxy_list.txt', 'r') as proxy_list:
        for cnt, line in enumerate(proxy_list):
            proxies.append(line.replace('\n', ''))
    while True:
        try:
            pytrends = TrendReq(proxies=proxies)
            break
        except:
            proxies.pop(0)
    print('dab')
    trends_merge_sort(keywords, 0, len(keywords)-1, pytrends)
