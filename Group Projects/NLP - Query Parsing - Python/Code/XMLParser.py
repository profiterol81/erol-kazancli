""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"      CorpusParser is a Class to read file xml(only QueryNo and Query information) and save the information in a list"
"      of XML objects       "
"                                                                                          "
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from XMLItem import XMLItem

class CorpusParser:

    """""""""  CONSTRUCTOR """""""""

    def __init__(self, File_name):
        if not "xml" in File_name:
            File_name = File_name + ".xml";
        self.filename = File_name;                       # filename contains the name of the file to be read.
                                                         # It is given when it's defined the object
        self.XMLItems   = [];

    """""""""   METHODS   """""""""

    def read(self):                                      # read() reads the file and save the information
                                                         # in the matrix "data".
        content = open(self.filename, "r");
        i = -1;

        self.XMLItems = []
        QueryNo = ""
        Query = ""
        ItemEnd = False
        for line in content:

            if "<QUERYNO>" in line:
                QueryNo = int(extractLine(line));

            if "<QUERY>" in line:
                Query = extractLine(line);
                ItemEnd = True

            if ItemEnd:
                newItem = XMLItem(QueryNo, Query, "", "", "", "", "", "")
                self.XMLItems.append(newItem)
                ItemEnd = False

        return self.XMLItems;

    def write(self, XMLItems, fileName):
        '''Save a structure(Rep_str) with some attributes, into a file(OutFile) with XML format.'''

        infile = open(fileName, 'w')
        infile.write('<OUTPUT-FILE>' + '\n')
        infile.close()

        infile = open(fileName, 'a')
        for x in XMLItems:
            infile.write('<QUERYNO>' + str(x.Qnumber) + '</QUERYNO>' + '\n')
            infile.write('<QUERY>' + x.Query + '</QUERY>' + '\n')
            infile.write('<LOCAL>' + x.Local + '</LOCAL>' + '\n')
            infile.write('<WHAT>' + x.What + '</WHAT>' + '\n')
            infile.write('<WHAT-TYPE>' + x.What_type + '</WHAT-TYPE>' + '\n')
            infile.write('<GEO-RELATION>' + x.Geo_relation + '</GEO-RELATION>' + '\n')
            infile.write('<WHERE>' + x.Where + '</WHERE>' + '\n')
            infile.write('<LAT-LONG>' + x.Lat_Long + '</LAT-LONG>' + '\n')

        infile.write('</OUTPUT-FILE>')
        infile.close()


def extractLine(line):               # extractLine() is out of the class. It just extract the information from a line.
    k = 0;
    element = "";
    for i in range(len(line)):
        if ( line[i]=="<" )and( element != "" ):
            break;
        if k==1:
            element = element + line[i];
        if line[i]==">":
            k = 1;
    return element;






