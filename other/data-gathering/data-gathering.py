import mysql.connector
import requests # to get image from the web
import shutil # to save it locally
import datetime
import os

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="historyguessr"
)

def download_image(url):
  ## Set up the image URL and filename
  script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
  storage_dir = "../../back/storage/app/public/img/"
  filename = str(datetime.datetime.now().timestamp()) + ".jpg"
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


def find_img_url(url):
    img_url = ""
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        #print(data)
        for key in data:
            if has_depiction(key):
                img_url = has_depiction(key)
                break
        return img_url

    else:
        print("Error in find_img_url")
        return False

def has_depiction(url:str):
    r = requests.get(url.replace("resource", "data") + ".json")
    if r.status_code == 200:
        data = r.json()
        try:
            data[url]['http://xmlns.com/foaf/0.1/depiction']
            print("Found image")
            return data[url]['http://xmlns.com/foaf/0.1/depiction'][0]['value']
        except Exception:
            print("Error in has_depiction")
            return ""
    
    else:
        print("Error in has_depiction")
        return False



mycursor = mydb.cursor()

for year in range(1950, 1955):
    img_url = find_img_url("http://dbpedia.org/data/Category:" + str(year) + "_deaths.json")
    filename = download_image(img_url)
    if filename:
        mycursor.execute("INSERT INTO images (year, path) VALUES (%s, %s)", (year, filename))
        mydb.commit()
    
    print("End of " + str(year))
