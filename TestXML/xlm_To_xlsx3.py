# -*- coding: UTF-8 -*-

"""Convert specific xml to xlsx.



"""

import xml.etree.ElementTree
import openpyxl


class ManObj:
    """
    Una lista [...] 
    
    iterabile = può essere richiamata in un for loop
    """

    KEYS = ("ID", "Sorgente", "Destinazione", "Classe", "LAC", "Target")

    def __init__(self):

        for key in self.KEYS:
            self.KEYS = None

        self.has_lac = False

    def get_managed_object_from_xml(self, xml_filename = './test1.xml', DEBUG=False):
        '''
        Set the xml file to parse and return a list of managed object or None

        :param xml_filename: the xml to parse
        :return: list of all object [<element>]
        '''

        # node of xmlfile where there are managed_objects
        node = xml.etree.ElementTree.parse(xml_filename).getroot()[0]
        # find all the managed_Object
        managed_objs = node.findall("{raml20.xsd}managedObject")

        # se esiste
        if managed_objs:
            # print out for debug
            if DEBUG:
                for index, obj in enumerate(managed_objs):
                    print("Trovato elemento {:-4}: {}".format(index, obj))

            # ritorno la managed_object list []
            self.managed_object = managed_objs
            print("Creata la lista {} contenente {} oggetti".format('XX', len(managed_objs)))
            return self.managed_object

        # se non trovo nulla
        else:
            print("Non sono stati trovati elementi.")
            return None

    def format_object(self):
        '''
        format the managed object list

        :return: a well formatted managed object list
        '''

        # Controllo se esiste una lista di oggetti
        if self.managed_objs:
            for obj in self.managed_object:

                # per ogni oggetto in lista
                name = obj.attrib['name']
                self.sorgente = name[:7]
                self.destinazione = name[11:]

                self.classe = obj.attrib['class']

        else:
            print("Non posso formattare una lista vuota.")

    def get_manObj(self):
        manObj = {"Classe" : self.classe,
                  "Sorgente" : self.sorgente,
                  "Destinazione" : self.destinazione,
                  "LAC" : self.lac,
                  "Target" : self.target,
                  "??" : self.has_lac}

        return manObj

if __name__ == '__main__':
    a = ManObj().get_managed_object_from_xml(DEBUG=True)