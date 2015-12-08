# -*- coding: UTF-8 -*-

import xml.etree.ElementTree
from UserDict import UserDict

def attrib():
    pass


class ManagedObject(UserDict):

    xmlMap = {"Sorgente"    :   (attributes,  'name',    0,    7),
              "Destinazione":   (attributes,  'name',   11,    0),
              "Classe"      :   (attributes, 'class', None, None)}

    def __init__(self, filename):
        UserDict.__init__(self)
        self['name'] = filename
        self.__parse(filename)


    def __parse(self, filename):

        self.clear()

        objs_name = "{raml20.xsd}managedObject"

        try:
            # tree = xml.etree.ElementTree.parse(filename)  # node of xmlfile where
            #     # there are managed_objects
            # root = tree.getroot()[0]
            #
            # mylist = root.findall(objs_name)  # find all the managed_Object -> return list

            # for elem in mylist:
            #     name = elem.attrib['name']
            #     sorgente = name[:7]
            #     destinazione = name[11:]
            #     classe = elem.attrib['class']

            root = xml.etree.ElementTree.parse(filename).getroot()[0]
            for elem in root.findall(objs_name):
                for tag, (func, arg, start, end) in self.xmlMap.items():

                    # al primo ciclo vale: "Classe", (<function attrib>, 'class', None, None) -> elem.attrib['class']
                    # sorgente = attrib(
                    self[tag] = func(arg)


                    print(tag, func, arg, start, end)

        except IOError:
            pass


if __name__ == '__main__':

    filename = './test1.xml'
    ManagedObject(filename)
