# -*- coding: UTF-8 -*-

import xml.etree.ElementTree
from UserDict import UserDict

filename = './test1.xml'


class ManagedObject(UserDict):
    xmlMap = {"Sorgente": None,
              "Destinazione": None,
              "Classe": None}

    def __init__(self, filename=None):
        UserDict.__init__(self)
        self['name'] = filename
        self.__parse(filename)

    def __parse(self, filename):

        self.clear()
        objs_name = "{raml20.xsd}managedObject"

        try:
            the_file = xml.etree.ElementTree.parse(filename)  # node of xmlfile where
            # there are managed_objects
            root = the_file.getroot()[0]
            list_ = root.findall(objs_name)  # find all the managed_Object -> return list

            for elem in list_:
                name = elem.attrib['name']
                sorgente = name[:7]
                destinazione = name[11:]
                classe = elem.attrib['class']

                print "Sorgente: {}\nDestinazione: {}\nClasse: {}".format(sorgente,
                                                                          destinazione,
                                                                          classe)
        except IOError:
            pass


if __name__ == '__main__':
    print ManagedObject(filename)
