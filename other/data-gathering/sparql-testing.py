import sparql
import string

q1 = (
'''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://dbpedia.org/ontology/>
PREFIX prop: <http://dbpedia.org/property/>

SELECT ?naturalevent, MIN(?date), ?depiction, (count(?link) as ?nlinks) WHERE {
?naturalevent rdf:type ?type .
?type rdfs:subClassOf* owl:NaturalEvent .
?naturalevent owl:wikiPageWikiLink ?link.
?naturalevent foaf:depiction ?depiction .
?naturalevent prop:date ?date .
} GROUP BY ?naturalevent ?depiction ORDER BY DESC(?nlinks) LIMIT 10
'''
)

result = sparql.query('http://dbpedia.org/sparql', q1)

for row in result:
    print(row)

print("")
print("")
print("")

q2 = (
'''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://dbpedia.org/ontology/>
PREFIX prop: <http://dbpedia.org/property/>

SELECT ?outbreak, MIN(?date), ?depiction, (count(?link) as ?nlinks) WHERE {
?outbreak a owl:Outbreak .
?outbreak owl:wikiPageWikiLink ?link.
?outbreak foaf:depiction ?depiction .
?outbreak prop:date ?date .
} GROUP BY ?outbreak ?depiction ORDER BY DESC(?nlinks) LIMIT 10
'''
)

result = sparql.query('http://dbpedia.org/sparql', q2)

for row in result:
    print(row)

print("")
print("")
print("")

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
    MINUS { ?societalevent a owl:SportsEvent . } .
    ?societalevent owl:wikiPageWikiLink ?link.
    ?societalevent foaf:depiction ?depiction .
    ?societalevent prop:date ?date .
    FILTER (datatype(?date) != xsd:gMonthDay) .
    OPTIONAL {?societalevent prop:year ?year .} .
    OPTIONAL {?societalevent prop:compyear ?compyear .} .
} GROUP BY ?societalevent ?depiction ORDER BY DESC(?nlinks) LIMIT 1000
'''
) #Excluding sports events because they are most of the time not relevant

result = sparql.query('http://dbpedia.org/sparql', q3)

i=0
for row in result:
    
    if row[1].n3().__contains__("http://www.w3.org/2001/XMLSchema#date") or row[1].n3().__contains__("http://www.w3.org/2001/XMLSchema#integer") or row[1].n3().__contains__("http://www.w3.org/2001/XMLSchema#decimal"):
        print(str(row[1])[:4])
    else:
        if row[2] != None:
            print(row[2].n3())
        elif row[3] != None:
            print(row[3].n3())
    print(str(row[4].n3())[1:-1])
    i+=1
    print(i)

print("")