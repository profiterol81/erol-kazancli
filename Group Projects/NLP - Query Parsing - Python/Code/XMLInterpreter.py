import dbpedia
import re
from XMLParser import CorpusParser


def Interpret (fileName):

    outputFileName = fileName.replace('.xml', '') + "_Output.xml"

    xml = CorpusParser(fileName)

    XMLItems = xml.read()

    for x in XMLItems:
        q = x.Query
        found, what, relation, where, country = findWhereWhatRelation(q)
        if what == '':
            what = 'None'
        if relation == '':
            relation = 'None'
        if where == '':
            where = 'None'

        if found:
            x.Local = 'YES'
            x.What = what
            if country <> '':
                x.Where = where + ', ' + country
            else:
                x.Where = where.strip()
            x.Geo_relation = relation
            x.What_type = findWhatType(what)
            lat, lon = dbpedia.getLattLong(where)
            if (lat <> "") and (lon <> ""):
                x.Lat_Long = str(round(float(lat), 2)) + ", " + str(round(float(lon), 2))
            else:
                x.Lat_Long = 'None'
        else:
            x.Local = 'NO'
            x.What = 'None'
            x.Where = 'None'
            x.Geo_relation = 'None'
            x.What_type = 'None'
            x.Lat_Long = 'None'

    xml.write(XMLItems, outputFileName)

# This method parses the query given using dbpedia search and regular expressions and returns found, what, relation, where, country
def findWhereWhatRelation(s):
    s = s.lower()
    found = False

    # find all the possible locations in the query
    listWords = dbpedia.isLocation(s, 'en')
    what = ''
    relation = ''
    where = ''
    country = ''

    if len(listWords) > 0:

        # iterate until finding the most probable location in the query
        # iteration is done from the longest to the shortest
        for word in listWords:

            where = word.strip().lower()

            reg = "(.*)(" + where + ")(.*)"
            p = re.compile(reg).findall(s)
            what = p[0][0].strip()
            # residue is the words coming after the location found
            residue = p[0][2].strip()
            a = re.compile(r"(.*)(\bin the\b|\bto the\b|\bfrom the\b|\bat the\b|\bon the\b|\bto\b|\bin\b|\bfrom\b|\bat\b|\bon\b|\bnear\b|\bnear to\b)(.*)").findall(residue)
            # if the residue does not contain a location keyword, the location found is a good candidate, stop iterating
            if not a:
                break

        country = dbpedia.getCountry(where)
        if what == '':
            what = residue
            found = True

        # if 'what' is not found
        if not found:
            p = re.compile(r"(.*)(\bsouth west\b|\bsouth east\b|\bnorth west\b|\bnorth east\b)(.*)").findall(what)
            if p:
                found = True
                what = p[0][0].strip()
                relation = p[0][1].strip().upper()
                x = p[0][2].strip()
                if ' ' in relation:
                    relation = relation.replace(' ', '_')
                else:
                    p2 = re.search(r"(south|north)(.*)", relation)
                    relation = p2(1) + '_' + p2(2)

                # search for the georelation checking the keywords in 'what'
                a = re.compile(r"(.*)(\bin the\b|\bto the\b|\bfrom the\b|\bat the\b|\bon the\b|\bto\b|\bin\b|\bfrom\b|\bat\b|\bon\b|\bnear\b|\bnear to\b)(.*)").findall(what)

                if a:
                    if a[0][2].strip() == '':
                        what = what.replace(a[0][1], '').strip()
                        if 'in' in a[0][1]:
                            relation = relation + '_of'
                        elif 'at' in a[0][1]:
                            relation = relation + '_at'
                        elif 'on' in a[0][1]:
                            relation = relation + '_on'
                        elif 'to' in a[0][1]:
                            relation = relation + '_to'
                        elif 'from' in a[0][1]:
                            relation = relation + '_from'

                relation = relation.upper()

            # if 'what' is still not found
            if not found:
                p = re.compile(r"(.*)(\bin\b|\bat\b|\bon\b|\bto\b|\bfrom\b|\bof\b|\bnear\b|\bnear to\b)(.*)").findall(what)
                if p:
                    if p[0][2].strip() == '':
                        found = True
                        what = p[0][0].strip()
                        relation = p[0][1].strip()
                        relation = relation.upper()
                    elif p[0][2].strip() == 'the':
                        found = True
                        what = p[0][0].strip()
                        relation = p[0][1].strip()
                        relation = relation.upper()
                        where = 'the ' + where
                    else:
                        where = p[0][2].strip() + ' ' + where
                        what = p[0][0].strip()
                        relation = p[0][1].strip().upper()

            found = True
            if residue <> '':
                where = where + ' ' + residue;

    # if location is not found through dbpedia search
    if not found:
        p = re.compile(r"(.*)(\bsouth west\b|\bsouth east\b|\bnorth west\b|\bnorth east\b|\bnorth\b|\bwest\b|\beast\b|\bsouth\b)(.*)").findall(s)
        if p:
            found = True
            what = p[0][0].strip()
            relation = p[0][1].strip().upper()
            where = p[0][2].strip()

    return found, what, relation, where, country

# This method parses 'what' found and gets the 'whatType' information using regular expressions
def findWhatType(what):
    whatType = ''
    a = re.compile(r"(.*)(\binfo|\bnews\b|\bfestival\b|\btrip|\bdiscount|\bincome|\bflight|\bto\b|\bblog\b|\bquestionnaire|\btour|\bweather|\bthing|\btip)(.*)").findall(what)
    if a:
        whatType = 'Information'

    a = re.compile(r"(.*)(\bhotel|\bbookshop|\bauto|\brent|\bcleaner|\bhostel|\bfood|\bhospital\b|\bpark|\bdoctor|\blaw|\bpolice|\bshop|\bcinema|\bhouse|\bbuy|\binn\b|\bmall|\brestaurant|\bcar|\bdealer|\bapartment|\bschool|\bplumber|\btraining|\bcafe|\bgym|\bairport|\bstore|\btheater|\bcenter|\bresort|\bnotary|\binsurance)(.*)").findall(what)
    if a:
        whatType = 'Yellow Page'

    if what == 'None':
        whatType = 'Map'

    if whatType == '':
        whatType = 'None'

    return whatType
