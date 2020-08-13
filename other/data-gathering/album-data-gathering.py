import sparql
import string
import utils
import requests

mydb = utils.database_connect()
mycursor = mydb.cursor()

album_query = (
'''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://dbpedia.org/ontology/>
PREFIX prop: <http://dbpedia.org/property/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX schema: <http://schema.org/>

SELECT ?album, MIN(?releasedate), ?wikiPage, MAX(?sales) WHERE {
    ?album a owl:MusicalWork ;
           rdf:type schema:MusicAlbum ;
           owl:releaseDate ?releasedate ;
           foaf:isPrimaryTopicOf ?wikiPage ;
           prop:salesamount ?sales ;
           prop:award ?award .
FILTER (?award = "Platinum"^^<http://www.w3.org/1999/02/22-rdf-syntax-ns#langString>) .
}GROUP BY ?album ?wikiPage ?sales ORDER BY DESC(?sales) LIMIT 200
'''
)
result = sparql.query('http://dbpedia.org/sparql', album_query)

for row in result:

    raw_wiki_url = str(row[2].n3())[1:-1]
    r = requests.get(raw_wiki_url)
    extractor = utils.WikiThumbailExtractor()
    extractor.feed(str(r.content))

    year = str(row[1])[:4]

    event_name = str(row[0].n3())[1:-1].split('/')[-1].replace('_', ' ')
    mycursor.execute("SELECT * FROM images WHERE event_name=%s", (event_name,))

    if len(mycursor.fetchall()) == 0:
        try:
            filename = utils.download_image("http:" + extractor.get_img_src())
            if filename:
                mycursor.execute("INSERT INTO images (year, path, event_name, img_caption, category) VALUES (%s, %s, %s, %s, %s)", (year, filename, event_name, "", "Album"))
                mydb.commit()
        except requests.exceptions.InvalidURL:
            pass
