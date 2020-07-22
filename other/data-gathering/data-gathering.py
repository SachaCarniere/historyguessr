import mysql.connector
import sparql
import string
import requests # to get image from the web
import shutil # to save it locally
import datetime
import os

forbidden_links = ["http://commons.wikimedia.org/wiki/Special:FilePath/Blue_pog.svg"]

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="historyguessr"
)

def download_image(url):
    if url.__contains__(".svg") or url.__contains__(".JPEG"):
        return False

    ## Set up the image URL and filename
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    storage_dir = "../../back/storage/app/public/img/"
    filename = str(datetime.datetime.now().timestamp()) + url[-4:]
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

mycursor = mydb.cursor()

q3 = (
'''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://dbpedia.org/ontology/>
PREFIX prop: <http://dbpedia.org/property/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?societalevent, MIN(?date), MIN(?year), MIN(?compyear), ?depiction, (count(?link) as ?nlinks) WHERE {
    ?societalevent rdf:type ?type .
    ?type rdfs:subClassOf* owl:SocietalEvent .
    MINUS { ?societalevent rdf:type ?typee .
            ?typee rdfs:subClassOf* owl:SportsEvent . } .
    ?societalevent owl:wikiPageWikiLink ?link ;
            foaf:depiction ?depiction ;
            prop:date ?date .
    FILTER (datatype(?date) != xsd:gMonthDay) .
    OPTIONAL {?societalevent prop:year ?year .} .
    OPTIONAL {?societalevent prop:compyear ?compyear .} .
} GROUP BY ?societalevent ?depiction ORDER BY DESC(?nlinks) LIMIT 1500
'''
) #Excluding sports events because they are most of the time not relevant

j = 0
result = sparql.query('http://dbpedia.org/sparql', q3)

i = 0
for row in result:
    try:
        year = try_parse_year(str(row[0].n3())[1:-1].split('/')[-1].replace('_', ' '), True)
    except Exception:
        if row[1].n3().__contains__("http://www.w3.org/2001/XMLSchema#date") or row[1].n3().__contains__("http://www.w3.org/2001/XMLSchema#integer") or row[1].n3().__contains__("http://www.w3.org/2001/XMLSchema#decimal"):
                year = int(str(row[1])[:4])
        else:
            if row[2] != None:
                year = int(str(row[2]))
            elif row[3] != None:
                year = int(str(row[3]))
            elif row[1].n3().__contains__("http://www.w3.org/1999/02/22-rdf-syntax-ns#langString"):
                try:
                    year = try_parse_year(str(row[1]))
                except Exception:
                    print("Can't parse")
                    print(row)
            else:
                print(row)


    filename = download_image(str(row[4].n3())[1:-1])
    if filename:
        mycursor.execute("INSERT INTO images (year, path, event_name) VALUES (%s, %s, %s)", (year, filename, str(row[0].n3())[1:-1].split('/')[-1].replace('_', ' ')))
        mydb.commit()
        ""

    print(str(row[0].n3())[1:-1].split('/')[-1].replace('_', ' '))
    print(year)
    i += 1
    if i%100==0:
        print("###########")

