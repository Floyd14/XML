# -*- coding: UTF-8 -*-

''' xml_To_xlsx Test1. 

This program convert .xml file to .xlsx Excel file..

Dependency: 
    openpyxl
    xml.etree.ElementTree as etree
    
For more info see: 
    - https://docs.python.org/2/library/xml.etree.elementtree.html 
    - http://www.diveintopython3.net/xml.html 
    - https://openpyxl.readthedocs.org/en/default/ '''


import datetime
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
import xml.etree.ElementTree as etree


def createActiveWorkbook():
    active_workbook = Workbook().active
    return active_workbook


def getRootOfAnXml(name='book.xml'):
    root = etree.parse(name).getroot() 
    return root

def setUpHeader(root):
    header = [elem.tag for elem in root[0]]
    
    
    i = 0
    while i < len(root):
        row = [val.text for val in root[i]]
        # Rows can also be appended
        i = i + 1 
    
def setHeaderStyle(cell):
    cell.font = Font(name='Calibri',
                size=16,
                bold=True,
                italic=False,
                vertAlign='baseline',
                underline='none',
                strike=False,
                color='FF000000')
    
    cell.fill = PatternFill(fill_type=None,
                            start_color='FFFFFFFF',
                            end_color='FF000000')
    
    cell.border = Border(left=Side(border_style=None,
                                   color='FF000000'),
                    right=Side(border_style=None,
                               color='FF000000'),
                    top=Side(border_style=None,
                             color='FF000000'),
                    bottom=Side(border_style='double',
                                color='FF000000'),
                    diagonal=Side(border_style=None,
                                  color='FF000000'),
                    diagonal_direction=0,
                    outline=Side(border_style=None,
                                 color='FF000000'),
                    vertical=Side(border_style=None,
                                  color='FF000000'),
                    horizontal=Side(border_style=None,
                                    color='FF000000')
                    )
    cell.alignment=Alignment(horizontal="center",
                        vertical="center",
                        text_rotation=0,
                        wrap_text=True,
                        shrink_to_fit=True,
                        indent=0)
    cell.number_format = 'General'
    cell.protection = Protection(locked=True,
                            hidden=False)
    

def main(name='book.xml'):
    tree = etree.parse(name)    # object
    root = tree.getroot()       # like a list
    # Create a Workbook
    workbook = Workbook()
    active_workbook = workbook.active
    # Make title
    active_workbook.title = root.tag
    
    #--- Print Header
    header = [elem.tag for elem in root[0]]
    active_workbook.append(header)
    # set stiles for header
    for row in active_workbook.iter_rows(row_offset=0):
        for cell in row:
            setHeaderStyle(cell)
        
    
    #print header
    #--- Print Elements for Row
    i = 0
    while i < len(root):
        row = [val.text for val in root[i]]
        # Rows can also be appended
        active_workbook.append(row)
        #print row
        i = i + 1 
    # Save the file
    dest_filename = 'xmlTest.xlsx'
    workbook.save(filename = dest_filename)    
    
if __name__ == '__main__':
    print datetime.datetime.today()
    main()

