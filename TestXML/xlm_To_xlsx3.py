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


class MyClass:
    """
    MyClass() è Una lista [...] {}.

    1- La classe legge un xml
    2- memorizza i managed_object in una lista[]
    3- formatta i singoli managed object in un dicionary {} ben formattato

    La classe è itarabile (può essere richiamata in un loop)
    """

    KEYS = ("ID", "Sorgente", "Destinazione", "Classe", "LAC", "Target")

    def __init__(self, xmlfile='./test1.xml', debug=False):

        self.DEBUG = debug  # Bool for trigger Debug mode
        self.xmlfile = xmlfile

        self.objs_list = []     # lista di obj che sono liste
        self.obj = []   # gli obj sono liste

        # self.sorgente = None
        # self.destinazione = None
        # self.classe = None

        self.formatted_obj = dict((key, None) for key in self.KEYS)  # an empty {} template

        # for debug only
        if self.DEBUG:
            print("Debug mode is set to {}.".format(self.DEBUG))
            print(self.__doc__)
            print("Inizializzo dictionary template:\n{}".format(self.formatted_obj))

        # Richiamo i metodi ...
        self.get_obj_list_from_xml()
        self.format_obj()

    def get_obj_list_from_xml(self):
        """ Set the xml file to parse and return a list of managed object or None.

        open xml file and parse it (setto il node e il tree) then find all th object that i need .

        :return: list (of all object [<element>])

        Dependency: xml.etree.ElementTree"""

        node = xml.etree.ElementTree.parse(self.xmlfile).getroot()[0]  # node of xmlfile where
        # there are managed_objects

        objs_name = "{raml20.xsd}managedObject"
        objs_list = node.findall(objs_name)  # find all the managed_Object
        # (it's list)

        if objs_list:
            if self.DEBUG:
                print(self.get_obj_list_from_xml.__doc__)
                # con enumerate posso gestire l'indice
                for index, my_obj in enumerate(objs_list):
                    print("Trovato elemento {:-4}: {}".format(index, my_obj))

            # return the managed_object list []
            print("Creata la lista id: {} contenente {} oggetti".format(id(objs_list), len(objs_list)))
            self.objs_list = objs_list
            return objs_list
        else:
            print("Non sono stati trovati elementi.")
            return None

    def get_obj_from_list(self):
        """ Take managed object list and yield an element

        It's a generator (can be used in a for loop)
        :return: list (yeld managed_object of the list at time)
        """

        print('\nInside get_obj_generator\n')
        for elem in self.objs_list:

            if self.DEBUG:
                print(self.get_obj_from_list.__doc__)
                print("Yelding {} ...".format(elem))
            self.obj = elem
            yield self.obj

    def format_obj(self):
        """ format the managed object into a well formatted Dictionary.

        :return: dictionary (of the managed object)
        """

        for elem in self.get_obj_from_list():
            print("Processo l' elemento: {}\n".format(elem))

            name = elem.attrib['name']
            sorgente = name[:7]
            destinazione = name[11:]
            classe = obj.attrib['class']

            print 'Sorgente: {}\nDestinazione: {}\nTipo: {}\n'.format(sorgente,
                                                                      destinazione,
                                                                      classe)

if __name__ == '__main__':

    my_list = get_managed_objects_list_from_xml()
    for obj in get_object_from_list(my_list):
        print('yelding..')
        format_a_managed_gbject(obj)

    a = MyClass(debug=True)
