import sparql
import string


q1 = (
'''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://dbpedia.org/ontology/>
PREFIX prop: <http://dbpedia.org/property/>

SELECT ?societalevent, MIN(?date), MIN(?dbodate), ?depiction, (count(?link) as ?nlinks) WHERE {
    ?societalevent rdf:type ?type .
    ?type rdfs:subClassOf* owl:SocietalEvent .
    MINUS { ?societalevent rdf:type ?typee .
            ?typee rdfs:subClassOf* owl:SportsEvent . } .
    ?societalevent owl:wikiPageWikiLink ?link ;
            foaf:depiction ?depiction ;
            prop:date ?date .
    FILTER (datatype(?date) != xsd:gMonthDay) .
    OPTIONAL {
        ?societalevent owl:date ?dbodate .
    } .
} GROUP BY ?societalevent ?depiction ORDER BY DESC(?nlinks) LIMIT 15
'''
)

q2 = (
'''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://dbpedia.org/ontology/>
PREFIX prop: <http://dbpedia.org/property/>

SELECT ?dbodateprop WHERE {
        ?dbodateprop rdf:type owl:DataProperty .
        ?dbodateprop rdfs:label 'date' .
} LIMIT 15
'''
)


q3 = (
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
           prop:salesamount ?sales .
}GROUP BY ?album ?wikiPage ?sales ORDER BY DESC(?sales) LIMIT 10
'''
)


q4 = (
'''
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://dbpedia.org/ontology/>
PREFIX prop: <http://dbpedia.org/property/>
PREFIX datat: <http://dbpedia.org/datatype/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX schema: <http://schema.org/>

SELECT ?film, MIN(?releasedate), ?wikiPage, ?gross WHERE {
    ?film a owl:Film;
           owl:releaseDate ?releasedate ;
           foaf:isPrimaryTopicOf ?wikiPage ;
           owl:gross ?gross .
    ?gross a <http://dbpedia.org/> .
FILTER regex(?gross, "E")
}GROUP BY ?film ?wikiPage ?gross ORDER BY DESC(?gross) LIMIT 1000
'''
)

result = sparql.query('http://dbpedia.org/sparql', q4)

for row in result:
    print(row)
    