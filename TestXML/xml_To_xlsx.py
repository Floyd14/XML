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


import datetime
import os
import xml.etree.ElementTree

from types import StringType

from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font


class Myxml:
    def __init__(self, path="./", xmlfile=None):
        """
        Myxml class
        
        :type xmlfile: str
        """
        assert type(xmlfile) is StringType, "xmlfile is not a string: xmlfile is %r" % xmlfile

        #self.name = xmlfile
        self.absolute_path = os.path.join(path, xmlfile)
        self.workbook = Workbook()
        self.active_workbook = self.workbook.active

        # assert isinstance(xml.etree.ElementTree.parse(self.location).getroot, object)
        self.tree = xml.etree.ElementTree.parse(self.absolute_path)
        self.root = self.tree.getroot()
        self.first_row = None
        self.rows = None

    def __str__(self):
        pass

    def len_of_first_row_in_root(self):
        return len(self.get_first_row_in_root())

    def get_first_row_in_root(self):
        if self.root is not None:
            first_row = [elem.tag for elem in self.root[0]]
            # print(first_row)  # Uncomment for debug
            return first_row

    def get_rows(self):
        # rows = [val.text for i in range(0, len(self.root)) for val in self.root[i]]
        # row = []
        # for i in range(0, len(self.root)):
        #    for val in root[i]:
        #        row.append(val.text)

        # print(rows)    # Uncomment for debug
        # --- Print Elements for Row
        rows = []
        i = 0
        while i < len(self.root):
            row = [val.text for val in self.root[i]]
            i += 1
            rows.append(row)

        #print rows viene chiamato un botto di volte
        return rows


def create_xlsx_from_xlm(Myxml):
    _path = Myxml.absolute_path[-4]  # senza l'estensione...
    _filename = './a.xlsx'

    # imposto il nome del foglio
    Myxml.active_workbook.title = Myxml.root.tag

    # creo l'header ..
    Myxml.active_workbook.append(Myxml.get_first_row_in_root())
    # creo le altre rows ..
    i = 0
    while i < len(Myxml.get_rows()):
        Myxml.active_workbook.append(Myxml.get_rows()[i]) # non va..
        i += 1


    Myxml.workbook.save(filename=_filename)

def get_header_cell():
    pass

def set_header_style(cell):
    """
Set Style for header's cell
    :param cell: an XLSX cell
    """
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
    cell.alignment = Alignment(horizontal="center",
                               vertical="center",
                               text_rotation=0,
                               wrap_text=True,
                               shrink_to_fit=True,
                               indent=0)
    cell.number_format = 'General'
    cell.protection = Protection(locked=True,
                                 hidden=False)


def main(name='book.xml'):
    tree = xml.etree.ElementTree.parse(name)  # object rifai!
    root = tree.getroot()  # like a list
    # Create a Workbook
    workbook = Workbook()
    active_workbook = workbook.active
    # Make title
    active_workbook.title = root.tag

    # --- Print Header
    header = [elem.tag for elem in root[0]]
    active_workbook.append(header)

    # set stiles for header
    for row in active_workbook.iter_rows(row_offset=0):
        for cell in row:
            set_header_style(cell)

    # print header
    # --- Print Elements for Row
    i = 0
    while i < len(root):
        row = [val.text for val in root[i]]
        # Rows can also be appended
        active_workbook.append(row)
        # print row
        i += 1
        # Save the file
    dest_filename = 'xmlTest.xlsx'
    workbook.save(filename=dest_filename)


if __name__ == '__main__':
    print datetime.datetime.today()
    a = Myxml(xmlfile='book.xml')

    print a.absolute_path[:-4]
    #a.get_first_row_in_root()
    #a.get_rows()

    create_xlsx_from_xlm(a)

    main()
