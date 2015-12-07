# -*- coding: UTF-8 -*-

"""Convert specific xml to xlsx.

"""

import xml.etree.ElementTree
import openpyxl

DEBUG = True


def get_managed_objects_list_from_xml(xml_filename='./test1.xml'):
    """ Set the xml file to parse and return a list of managed object or None.

    open xml file and parse it (setto il node e il tree) then find all th object that i need .

    :param xml_filename: the xml to parse
    :return: list of all object [<element>]

    Dependency: xml.etree.ElementTree
    """

    node = xml.etree.ElementTree.parse(xml_filename).getroot()[0]  # node of xmlfile where
    # there are managed_objects
    managed_objs = node.findall("{raml20.xsd}managedObject")  # find all the managed_Object
    # (it's list)

    if managed_objs:
        if DEBUG:
            # con enumerate posso gestire l'indice
            for index, my_obj in enumerate(managed_objs):
                print("Trovato elemento {:-4}: {}".format(index, my_obj))

        # return the managed_object list []
        print("Creata la lista {} contenente {} oggetti".format('XX', len(managed_objs)))
        return managed_objs
    else:
        print("Non sono stati trovati elementi.")
        return None


def get_object_from_list(alist):
    """ Take managed object list and yield an element

    It's a generator (can be used in a for loop)

    :param alist: of managed_objects
    :return: a managed_object (that is another list) of the list at time
    """

    print('\nInside get_obj_generator\n')
    for my_obj in alist:
        print(my_obj)
        yield my_obj


KEYS = ("ID", "Sorgente", "Destinazione", "Classe", "LAC", "Target")


def format_a_managed_gbject(obj):
    """ Richiamo il metodo get_object_from_list that yeld object and

    :param obj:
    :return:
    """

    # an empty template
    my_managed_object = dict((key, None) for key in KEYS)
    print("Empty template:\n{}".format(my_managed_object))

    print("\nInside the formatting func.\n")
    print("Make the element {} biutifull!!".format(obj))

    # per ogni oggetto in lista
    name = obj.attrib['name']
    sorgente = name[:7]
    destinazione = name[11:]
    classe = obj.attrib['class']

    print 'Sorgente: {}\nDestinazione: {}\nTipo: {}\n'.format(sorgente, destinazione, classe)

    my_managed_object['a'] = name
    print("Dictionary:\n{}".format(my_managed_object))


if __name__ == '__main__':

    my_list = get_managed_objects_list_from_xml()
    for obj in get_object_from_list(my_list):
        print('yelding..')
        format_a_managed_gbject(obj)

