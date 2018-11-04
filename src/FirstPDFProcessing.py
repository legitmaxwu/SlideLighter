

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from pdf2image import convert_from_path



paths = []



def CreateJPEGS(filename):
    global paths
    pages = convert_from_path('../samples/' + filename + '.pdf')
    pageNum = 1
    for page in pages:
        page.save("../samples/jpegs/" + filename + "_page" + str(pageNum) + ".jpeg")
        paths.append("../samples/jpegs/" + filename + "_page" + str(pageNum) + ".jpeg")
        pageNum += 1




