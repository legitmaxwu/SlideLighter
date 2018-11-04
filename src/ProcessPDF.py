import argparse
import logging
import six
import sys
sys.path.insert(0,"/Users/adam/anaconda3/lib/python3.6/site-packages/pdfminer.six-20170720-py3.6.egg")
import pdfminer.settings
pdfminer.settings.STRICT = False
import pdfminer.high_level
import pdfminer.layout
from pdfminer.image import ImageWriter
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure

ofile = None
pdfsize = 0


def parse_layout(layout):
    """Function to recursively parse the layout tree."""

    for lt_obj in layout:
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            parsed = str(lt_obj.get_text())
            if parsed.count('\n-') > 1 or parsed.count('\n2'):
                splits = parsed.split('\n')
                splits.pop()
                length = len(splits)
                for i in range(length):
                    while (not splits[i][0].isalpha()):
                        splits[i] = splits[i][1:]
                x_coord_1, x_coord_2 = lt_obj.bbox[0]/pdfsize[2], lt_obj.bbox[2]/pdfsize[2]
                y_coord_1, y_coord_2 = lt_obj.bbox[1]/pdfsize[3], lt_obj.bbox[3]/pdfsize[3]
                y_coord_sectioned = (y_coord_2 - y_coord_1) / length
                for index in range(length):
                    ofile.write(str(lt_obj.__class__.__name__) + ": List - Element " + str(index + 1) + "\n")
                    adjusted_coords = (x_coord_1, y_coord_2 - (index + 1) * y_coord_sectioned, x_coord_2, y_coord_2 - index * y_coord_sectioned)
                    ofile.write(str(adjusted_coords) + "\n")
                    ofile.write(splits[index] + "\n")
            else:
                ofile.write(str(lt_obj.__class__.__name__) + "\n")
                adjusted_coords = (lt_obj.bbox[0]/pdfsize[2],lt_obj.bbox[1]/pdfsize[3],lt_obj.bbox[2]/pdfsize[2],lt_obj.bbox[3]/pdfsize[3])
                ofile.write(str(adjusted_coords) + "\n")
                ofile.write(parsed)
                
        elif isinstance(lt_obj, LTFigure):
            ofile.write(str(lt_obj.__class__.__name__) + "\n")
            adjusted_coords = (lt_obj.bbox[0]/pdfsize[2],lt_obj.bbox[1]/pdfsize[3],lt_obj.bbox[2]/pdfsize[2],lt_obj.bbox[3]/pdfsize[3])
            ofile.write(str(adjusted_coords) + "\n")
            parse_layout(lt_obj)  # Recursive

def parse_pdf(pdfFilePath):
    global ofile
    global pdfsize
    fp = open(pdfFilePath, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    pdfsize = PDFPage.create_pages(doc).__next__().mediabox
    rsrcmgr = PDFResourceManager()
    laparams = LAParams(line_margin=0.2,char_margin = 5)
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    pageNum = 1
    for page in PDFPage.create_pages(doc):
        ofile = open(pdfFilePath + "_page" + str(pageNum) + "_elements.txt","w+")
        interpreter.process_page(page)
        layout = device.get_result()
        parse_layout(layout)
        pageNum += 1
        ofile.close()