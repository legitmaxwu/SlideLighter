import random
import sys
from ast import literal_eval as make_tuple

dic = {}

def calculateCoverPer(clickpoints, elementpoints):
    lx = min(max(clickpoints[0],clickpoints[2]), max(elementpoints[0],elementpoints[2])) - max(min(clickpoints[0],clickpoints[2]), min(elementpoints[0],elementpoints[2]))
    ly = min(max(clickpoints[1],clickpoints[3]), max(elementpoints[1],elementpoints[3])) - max(min(clickpoints[1],clickpoints[3]), min(elementpoints[1],elementpoints[3]))
    if (lx >= 0 and ly >= 0):
        return (lx * ly / ((elementpoints[2]-elementpoints[0]) * (elementpoints[3]-elementpoints[1])))
    return 0

def FindSelectedElements(clickpoints,page,filename):
    global dic
    #RETURNS BOX IN (x,y) COORDINATES, TOP LEFT THEN BOTTOM RIGHT
    elementFile = open(("../samples/" + filename + ".pdf_page" + str(page) + "_elements.txt") , "r")
    fLines = elementFile.readlines()
    coordLine,getText = False,False
    elementText = ""
    skip = 0
    for line in fLines:
        if skip:
            skip -= 1
            continue
        if getText:
            while (line[:2] != "LT" and (line[:1] != "(" and line[1:4].isdigit())):
                skip+=1
                elementText += line
            getText = not getText
            dic[elementText] = dic.get(elementText,0) + 1 
        elif line[:6] == "LTText":
            coordLine = not coordLine
        elif coordLine:
            if (calculateCoverPer(clickpoints,make_tuple(line)) > 0.75):
                getText = not getText
            coordLine = not coordLine

def GetDict():
    return dic
