# -*- coding: UTF-8 -*-

import xml.etree.ElementTree


# Ritorno una lista da un file xml
def get_list_from_xml(xmlfile='./test1.xml', debug=False):
    """
    Ritorna una lista di managedObject trovati in un file xml.

    :param xmlfile: str (path of .xml file)
    :param debug: bool (to trigger debug mode)
    :return: list
    """

    objs_name = "{raml20.xsd}managedObject"
    node = xml.etree.ElementTree.parse(xmlfile).getroot()[0]  # node of xmlfile where
        # there are managed_objects

    objs_list = node.findall(objs_name)  # find all the managed_Object
    #  (it's list)

    if debug:
        print("Creata la lista id: {} con {}".format(id(objs_list), len(objs_list)))

    return objs_list


# Classe funzionante NON MODIFICARE
class ProcessXml:
    """
    ProcessXml() prende uno specifico xml file e lo processa.

    1- La classe legge un xml
    2- memorizza i managed_object in una lista[]
    3- formatta i singoli managed object in un dicionary {} ben formattato

    La classe è itarabile (può essere richiamata in un loop)
    """

    def __init__(self, xmlfile='./test1.xml', debug=False):

        self.DEBUG = debug  # Bool for trigger Debug mode
        self.xmlfile = xmlfile

        self.objs_list = []  # lista di obj che sono liste
        self.obj = []  # gli obj sono liste

        self.formatted_obj = {}

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

        KEYS = ("ID", "Sorgente", "Destinazione", "Classe", "LAC", "Target")

        for elem in self.get_obj_from_list():
            print("Processo l' elemento: {}\n".format(elem))

            name = elem.attrib['name']
            sorgente = name[:7]
            destinazione = name[11:]
            classe = elem.attrib['class']

            if self.DEBUG:
                print 'Sorgente: {}\nDestinazione: {}\nTipo: {}\n'.format(sorgente,
                                                                          destinazione,
                                                                          classe)

            self.formatted_obj = {KEYS[1]: sorgente,
                                  KEYS[2]: destinazione,
                                  KEYS[3]: classe}

            print("-> creato {}: {}".format(id(self.formatted_obj), self.formatted_obj))


if __name__ == '__main__':
    # a = ProcessXml(debug=True)


