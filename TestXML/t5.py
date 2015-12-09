# -*- coding: UTF-8 -*-

import xml.etree.ElementTree
from UserDict import UserDict

def get_raw_element_from_xml(filename='./test1.xml'):

    obj_name = "{raml20.xsd}managedObject"

    root = xml.etree.ElementTree.parse(filename).getroot()[0]
    for elem in root.findall(obj_name):

        x = ManagedObject(elem)
        print repr(x)

class ManagedObjects(UserDict):
    # Classe conteiner #
    # Quando inizializzo questa classe si inizializza anche la classe derivata!
    # (Prima questa e poi la derivata)

    def __init__(self, raw_obj=None):
        UserDict.__init__(self)
        self.name = id(raw_obj)  # -> chiamo self.__setitem__(self, name, id(raw_obj))
        #self.raw_obj = raw_obj # come lo gestisco ? sto chiamando __init??
        self['raw_obj'] = raw_obj # -> chamo self.__setitem__(self, 'raw_obj', raw_obj)

    def __str__(self):
        string = "Dictionary {} = {} {}\n"
        return string

class ManagedObject(ManagedObjects):
    # Mappa (è un dictionary) di cosa chiamare:
    # tag : (funzione da chiamare, metodo, nome dell'attributo, inizio e fine dello slice
    xmlMap = {"Sorgente"    :   (getattr, 'attrib',  'name',    0,    7),
              "Destinazione":   (getattr, 'attrib',  'name',   11, None),
              "Classe"      :   (getattr, 'attrib', 'class', None, None)}

    #objs_name = "{raml20.xsd}managedObject"

    def __parse(self, item):

        self.clear()
        #root = xml.etree.ElementTree.parse(filename).getroot()[0]
        #for elem in root.findall(self.objs_name):

        for tag, (function, method, attrib, start, end) in self.xmlMap.items():
            # al primo ciclo vale: "Classe", (<function getattr>, 'class', None, None) -> elem.attrib['class']
            # self['Classe'] = getattr(elem, 'attrib')['class'][None, None]

            self[tag] = function(item, method)[attrib][start:end]

            #print(self[tag])
            #print(elem)
            #print(ManagedObject())
            #print(ManagedObject)

    def __setitem__(self, key, item):
        # Quando istanzio la classe managedObject (quella derivata) chiamo,
        #  __init__ della classe padre:
        # che istanzia un UserDict (un dictionary) e
        # imposta un self['name'] = filename
        # -> (chiama ManagedObjects.__setitem__(self, key=name, filename) [quello della classe padre]
        #
        # dopo aver impostato il nome torna quà ??
        # se key == 'name'
        if key is 'raw_obj':  # ritorna idem?
            self.__parse(item)

        # finito di fare i cambiamenti chiamo il set del padre
        ManagedObjects.__setitem__(self, key, item)

if __name__ == '__main__':

    get_raw_element_from_xml()
