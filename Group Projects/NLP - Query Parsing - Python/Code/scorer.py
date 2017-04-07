# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 19:18:10 2015

@author: Lukashi
"""

import xml.etree.ElementTree as et #Used ElementTree library
"""
score(yourFile, goldenSetFile)
yourFile - path to the file you want to score
goldenSetFile - path to the file with the "golden set"
Both files should be in .xml format with similar structure.
The score() function counts score for the file provided by yourFile path by comparing it with the file provided by goldenSetFile path.
It prints the score, then returns a tuple in a form (precisionScore, recallScore, f1-score).
"""
def score(yourFile, goldenSetFile):
    gold = et.parse(goldenSetFile)
    goldRoot = gold.getroot()
    test = et.parse(yourFile)
    testRoot = test.getroot()
    correct, tagged = 0, 0
    allLocal = len(goldRoot.findall("QUERYNO"))

    i = 0
    while i < len(testRoot):
        if testRoot[i].tag == "QUERYNO":
            j = 0
            f = False
            while j < len(goldRoot) and not f:
                if goldRoot[j].text == testRoot[i].text:
                    tagged += 1
                    f = True
                    if goldRoot[j+2].text == "NO":
                        if testRoot[i+2].text == "NO":
                            correct += 1
                    else:
                        if testRoot[i+2].text.lower() == goldRoot[j+2].text.lower()  and \
                        testRoot[i+3].text.lower()  == goldRoot[j+3].text.lower()  and \
                        testRoot[i+4].text.lower()  == goldRoot[j+4].text.lower()  and \
                        testRoot[i+5].text.lower()  == goldRoot[j+5].text.lower() :
                            if testRoot[i+6].text.lower().split(",")[0] == goldRoot[j+6].text.lower().split(",")[0]:
                                correct += 1
                j += 8
        i += 8

    precision, recall, f1 = 0, 0, 0
    if tagged != 0:
        precision = 1.0*correct/tagged
    if allLocal != 0:
        recall = 1.0*correct/allLocal
    if precision + recall != 0:
        f1 = 2.0*precision*recall/(precision + recall)

    print 'Precision: {0:.3f} Recall: {1:.3f} F1-score: {2:.3f}'.format(precision, recall, f1)

    return (precision, recall, f1)

#main
inputGolden = "../../laboCase/GC_Tr_100.xml"
inputUser = "../../laboCase/GC_Tr_100_User.xml"
