# -*- coding: UTF-8 -*-

"""Convert specific xml to xlsx.

"""

import xml.etree.ElementTree
import openpyxl


DEBUG = True

def get_managed_objects_list_from_xml(xml_filename='./test1.xml'):
    '''
    Set the xml file to parse and return a list of managed object or None

    :param xml_filename: the xml to parse
    :return: list of all object [<element>]
    '''

    # node of xmlfile where there are managed_objects
    node = xml.etree.ElementTree.parse(xml_filename).getroot()[0]
    # find all the managed_Object
    managed_objs = node.findall("{raml20.xsd}managedObject")

    # if exist
    if managed_objs:
        # print out for debug
        if DEBUG:
            for index, obj in enumerate(managed_objs):
                print("Trovato elemento {:-4}: {}".format(index, obj))

        # return the managed_object list []
        print("Creata la lista {} contenente {} oggetti".format('XX', len(managed_objs)))
        return managed_objects_list

    # se non trovo nulla
    else:
        print("Non sono stati trovati elementi.")
        return None

def get_object_from_list(self):
    print('ff')

    testlist = get_managed_objects_list_from_xml()
    print(testlist)

    for obj in testlist:
        print(obj)
        yield obj
        #next()

class ManObj:
    """
    Una lista [...] {}
    
    iterabile = può essere richiamata in un for loop
    """

    KEYS = ("ID", "Sorgente", "Destinazione", "Classe", "LAC", "Target")

    def __init__(self, debug=False):

        self.DEBUG = debug              # Bool for trigger Debug mode
        self.managed_objects_list = []  # list of all selected objects in the xml file

        # an empty template
        my_managed_object = dict((key, None) for key in self.KEYS)

        # for debug only
        if self.DEBUG:
            print("Debug mode is set to {}.".format(self.DEBUG))
            print("Inizializzo dictionary template:\n{}".format(my_managed_object))


    def format_object(self):
        '''
        format the managed object list into

        :return: a well formatted managed object dictionary
        '''

        self.get_object_from_list

        # per ogni oggetto in lista
        name = obj.attrib['name']
        self.sorgente = name[:7]
        self.destinazione = name[11:]

        self.classe = obj.attrib['class']

        print("Non posso formattare una lista vuota.")


if __name__ == '__main__':
    get_managed_objects_list_from_xml()
    get_object_from_list()
    a = ManObj(debug=True)
    # a.get_managed_objects_list_from_xml()
    # a.get_object_from_list()