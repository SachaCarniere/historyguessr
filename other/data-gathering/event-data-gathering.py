import sparql
import string
import utils


mydb = utils.database_connect()
mycursor = mydb.cursor()

q3 = (
'''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://dbpedia.org/ontology/>
PREFIX prop: <http://dbpedia.org/property/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?societalevent, MIN(?date), MIN(?year), MIN(?compyear), MIN(?firstyear), MIN(?dbodate), ?depiction, GROUP_CONCAT(DISTINCT(?caption); separator=" "), (count(DISTINCT(?link)) as ?nlinks) WHERE {
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
    OPTIONAL {?societalevent prop:first ?firstyear .} .
    OPTIONAL {?societalevent owl:date ?dbodate .} .
    OPTIONAL {?societalevent prop:caption ?caption .} .
} GROUP BY ?societalevent ?depiction ORDER BY DESC(?nlinks) LIMIT 1500
'''
) #Excluding sports events because they are most of the time not relevant

j = 0
result = sparql.query('http://dbpedia.org/sparql', q3)

i = 0
for row in result:
    year = None
    try:
        year = utils.try_parse_year(str(row[0].n3())[1:-1].split('/')[-1].replace('_', ' '), True)
    except Exception:

        if row[5] != None:
            year = int(str(row[5])[:4])

        elif row[1].n3().__contains__("http://www.w3.org/2001/XMLSchema#date") or row[1].n3().__contains__("http://www.w3.org/2001/XMLSchema#integer") or row[1].n3().__contains__("http://www.w3.org/2001/XMLSchema#decimal"):
                year = int(str(row[1])[:4])

        elif row[2] != None:
            year = int(str(row[2]))

        elif row[3] != None:
                year = int(str(row[3]))

        else:
            if row[1].n3().__contains__("http://www.w3.org/1999/02/22-rdf-syntax-ns#langString"):
                try:
                    year = utils.try_parse_year(str(row[1]))
                except Exception:
                    print("Can't parse")
                    continue
            else:
                print(row)

        if row[4] != None:
            try:
                year = int(str(row[4]))
            except ValueError:
                pass

    if str(row[0].n3())[1:-1].__contains__("World_War_II") and (year>1945 or year<1939):
        continue

    if year == None:
        continue


    filename = utils.download_image(str(row[6].n3())[1:-1])
    if filename:
        mycursor.execute("INSERT INTO images (year, path, event_name, img_caption) VALUES (%s, %s, %s, %s)", (year, filename, str(row[0].n3())[1:-1].split('/')[-1].replace('_', ' '), str(row[7])))
        mydb.commit()
        ""

    '''
    print(str(row))
    print(str(row[0].n3())[1:-1].split('/')[-1].replace('_', ' '))
    print(year)
    print("#################")
    '''
    i += 1
    if i%100==0:
        print("###########")

