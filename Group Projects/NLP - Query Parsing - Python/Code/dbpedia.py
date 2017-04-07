
from SPARQLWrapper import SPARQLWrapper, JSON
import re


def isLocation (term, lang):

    global sparql
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    if lang == 'en':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://www.ontologydesignpatterns.org/ont/d0.owl#Location>}
                UNION
                { res:**1** rdf:type <http://dbpedia.org/ontology/Place>}
                UNION
                { res:**1** rdf:type <http://dbpedia.org/ontology/PopulatedPlace>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/PopulatedPlace>}
                UNION
                { res:**1** rdf:type <http://schema.org/Place>}
                UNION
                { res:**1** rdf:type <http://dbpedia.org/class/yago/YagoGeoEntity>} .
            }
        """

    wordGroups = splitText(term)
    tempQuery = query
    listWords = []
    for x in range(0, len(wordGroups)):
        word = wordGroups[x].replace(' ','_')
        query = query.replace('**1**', word)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query()
        rta = results.convert()
        result = rta['boolean']
        if result:
            listWords.append(wordGroups[x])
        query = tempQuery

    return listWords;


def isCity (term, lang):

    global sparql
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    if lang == 'en':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://dbpedia.org/ontology/Settlement>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/City>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/Village>} .
            }
        """

    wordGroups = splitText(term)
    tempQuery = query
    listWords = []
    for x in range(0, len(wordGroups)):
        word = wordGroups[x].replace(' ','_')
        query = query.replace('**1**', word)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query()
        rta = results.convert()
        result = rta['boolean']
        if result:
            listWords.append(wordGroups[x])
        query = tempQuery

    return listWords;


def isState (term, lang):

    global sparql
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    if lang == 'en':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://dbpedia.org/class/yago/StatesOfTheUnitedStates>}.
            }
        """

    wordGroups = splitText(term)
    tempQuery = query
    listWords = []
    for x in range(0, len(wordGroups)):
        word = wordGroups[x].replace(' ','_')
        query = query.replace('**1**', word)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query()
        rta = results.convert()
        result = rta['boolean']
        if result:
            listWords.append(wordGroups[x])
        query = tempQuery

    return listWords;

def isCountry (term, lang):

    global sparql
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    if lang == 'en':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://dbpedia.org/ontology/Country>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/Country>}
            }
        """

    wordGroups = splitText(term)
    tempQuery = query
    listWords = []
    for x in range(0, len(wordGroups)):
        word = wordGroups[x].replace(' ','_')
        query = query.replace('**1**', word)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query()
        rta = results.convert()
        result = rta['boolean']
        if result:
            listWords.append(wordGroups[x])
        query = tempQuery

    return listWords;

def isRegion (term, lang):

    global sparql
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    if lang == 'en':
        query ="""
            PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX res: <http://dbpedia.org/resource/>
            ASK  WHERE {
                { res:**1** rdf:type <http://dbpedia.org/ontology/Region>}
                UNION
                { res:**1** rdf:type <http://umbel.org/umbel/rc/GeographicalRegion>}
            }
        """

    wordGroups = splitText(term)
    tempQuery = query
    listWords = []
    for x in range(0, len(wordGroups)):
        word = wordGroups[x].replace(' ','_')
        query = query.replace('**1**', word)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query()
        rta = results.convert()
        result = rta['boolean']
        if result:
            listWords.append(wordGroups[x])
        query = tempQuery

    return listWords;


def splitText(text):

    text = re.sub(r'[,\s]+', '_', text)
    listWords = []
    if text <> '' and text <> '_':
        words = text.split('_')
        temp = len(words)
        remaining = ''
        if temp <> 0:
            for x in range(0, len(words)):
                word = ''
                for y in range(0, temp):
                    word = word + words[y]
                    if y <> temp - 1:
                        word = word + ' '
                listWords.append(word.title())
                temp = temp - 1
                if x <> 0:
                    remaining = remaining + words[x] + ' '
            listWords = listWords + splitText(remaining.strip())

    return listWords;

# gets lattitude and longitude information
def getLattLong (term):

    global sparql
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    query ="""
    PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX res: <http://dbpedia.org/resource/>
    SELECT * WHERE {
        res:**1** a dbo:Place .
        res:**1** geo:lat ?lat .
        res:**1** geo:long ?long .
    }
    """
    term = term.title()
    term = term.strip().replace(' ','_')

    tempQuery = query
    query = query.replace('**1**', term)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query()
    rta = results.convert()
    query = tempQuery
    lat = ""
    lon = ""

    if rta:
        if rta['results']['bindings']:
            lat = rta['results']['bindings'][0]['lat']['value']
            lon = rta['results']['bindings'][0]['long']['value']
    return lat, lon

# gets country information
def getCountry (term):

    global sparql
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    query ="""
    PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX res: <http://dbpedia.org/resource/>
    SELECT * WHERE {
        res:**1** a dbo:Place .
        res:**1** dbo:country ?country .
    }
    """
    term = term.title()
    term = term.strip().replace(' ','_')

    query = query.replace('**1**', term)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query()
    rta = results.convert()
    country = ""

    if rta:
        if rta['results']['bindings']:
            country = rta['results']['bindings'][0]['country']['value']
    country = country.replace('http://dbpedia.org/resource/', '')

    # if country not found check if it is a country itself
    if country == '':

        list = isCountry(term, 'en')

        if len(list) > 0:
            country = term

    return country



