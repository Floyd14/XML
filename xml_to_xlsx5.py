# -*- coding: UTF-8 -*-

import xml.etree.ElementTree


xmlfile='./test1.xml'

def get_list_from_xml(xmlfile):
    """
    :param xmlfile:
    :return: list
    """

    objs_name = "{raml20.xsd}managedObject"

    node = xml.etree.ElementTree.parse(xmlfile).getroot()[0]  # node of xmlfile where
    # there are managed_objects

    objs_list = node.findall(objs_name)  # find all the managed_Object
    #  (it's list)

    return objs_list


def get_element_from_list():
    """
    :return: list
    """
    data = get_list_from_xml(xmlfile)   # is a list
    for elem in data:
        yield elem


def create_managed_object_from_list():
    """
    :return:
    """
    for element in get_element_from_list():
        yield element


class ManagedObject:

    debug = True

    def __init__(self):
        self.sorgente = None
        self.destinazione = None
        self.classe = None
        self.target = None

    def __str__(self):

        stringa = "ManagedObject: {}".format(id(self))
        return stringa

    def get_managed_object(self):

        keys = ("ID", "Sorgente", "Destinazione", "Classe", "LAC", "Target")
        managed_object = {keys[1]: self.sorgente,
                          keys[2]: self.destinazione,
                          keys[3]: self.classe}

        if self.debug:
            print("-> get {}: {}".format(id(managed_object), managed_object))

        return managed_object

if __name__ == '__main__':

    a = ManagedObject()
    print a
    a.get_managed_object()
