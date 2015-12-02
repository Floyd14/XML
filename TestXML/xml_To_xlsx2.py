# -*- coding: UTF-8 -*-
""" xml_To_xlsx Test1.
This program convert .xml file to .xlsx Excel file ...
Dependency:
    openpyxl
    xml.etree.ElementTree as etree
For more info see:
    - https://docs.python.org/2/library/xml.etree.elementtree.html
    - http://www.diveintopython3.net/xml.html
    - https://openpyxl.readthedocs.org/en/default/ """

import xml.etree.ElementTree as et

from openpyxl import Workbook



def main():
    """
    Main script (sostituito)
    """
    xml_filename = "./test1.xml"
    
    tree = et.parse(xml_filename)           # "importo" un file .xml 
    root = tree.getroot()                   # ottengo la root del file, root è come una lista multidim
    
    # trovo i manage object è una lista
    entry = root[0]
    managed_objects =  entry.findall('{raml20.xsd}managedObject')
    print managed_objects # for Debug
    
#     
#     def get_object(managed_objects):
#         for managed_object in managed_objects:
#             print managed_object
#             return managed_object
#         
#     get_object(managed_objects)
    # name of obj
    print [managed_object.attrib['name'] for managed_object in managed_objects]
    
    for managed_object in managed_objects:
        name = managed_object.attrib['name']
        sorgente = name[:7]
        destinazione = name[11:]
        
        tipo = managed_object.attrib['class']
        
        if managed_object[0].attrib['name']:
            lac = managed_object[0].attrib['name']
        else:
            lac = 0
        
        print 'Sorgente: %s, Destinazione: %s, Tipo: %s' %(sorgente, destinazione, classe)
    
    #def mg_get_class(managed_objects):
    #    [cls for managed_object. in managed_objects]
    #    return
        
        
#     # Create a Workbook per interfacciarmi al file Excel
#     workbook = Workbook() # � una lista?
#     
#     # prendo qoello appena creato
#     active_workbook = workbook.active
#     active_workbook.title = root.tag
#     # Creo l'header
#     
#     # root path where there are iterable object..
#      
#     user_root = root[0] 
#     
#     print root[0][1].attrib['name']
#     print root[0][1]
#     # and name to show in the header of excell Tablle ex: .attrib[name] 
#     # will crash if .attrib[] doesn't exist ...
#     header = [elem.attrib['name'] for elem in user_root] # [ root[0][i], .. ]  
#     active_workbook.append(header)
# 
#     # set stiles for header: prendo la prima riga
#     # active_workbook.iter_rows(row_offset=0) = <generator object get_squared_range at 0x01101B70>
#     for row in active_workbook.iter_rows(row_offset=0): # row = (<Cell catalog.A1>, <Cell catalog.B1>, <Cell catalog.C1>, <Cell catalog.D1>, <Cell catalog.E1>, <Cell catalog.F1>)
#         for cell in row:
#             set_cell_style(cell)
# 
#     # Print elements for Row
#     i = 1 #salto il primo elemento
#     while i < len(user_root):
#         row = [val.text for val in user_root[i]]
#         active_workbook.append(row)
#         i += 1
#         
#     # Save the file
#     dest_filename = 'xmlTest2.xlsx'
#     workbook.save(filename=dest_filename)

if __name__ == '__main__':
    main()
