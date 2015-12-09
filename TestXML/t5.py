# -*- coding: UTF-8 -*-

import xml.etree.ElementTree
from UserDict import UserDict



class ManagedObjects(UserDict):
    # Classe conteiner #

    def __init__(self, filename = None):
        UserDict.__init__(self)
        self['name'] = filename  # -> chiamo self.__setitem__(self, name, filename)
        self['data'] = None

    def __str__(self):

        string = str(self['name'][2:]+' => ')
        return string

class ManagedObject(ManagedObjects):
    # Mappa (è un dictionary) di cosa chiamare:
    # tag : (funzione da chiamare, metodo, nome dell'attributo, inizio e fine dello slice
    xmlMap = {"Sorgente"    :   (getattr, 'attrib',  'name',    0,    7),
              "Destinazione":   (getattr, 'attrib',  'name',   11, None),
              "Classe"      :   (getattr, 'attrib', 'class', None, None)}

    objs_name = "{raml20.xsd}managedObject"

    def __parse(self, filename):

        self.clear()
        #root = xml.etree.ElementTree.parse(filename).getroot()[0]
        #for elem in root.findall(self.objs_name):

        for tag, (function, method, attrib, start, end) in self.xmlMap.items():

            # al primo ciclo vale: "Classe", (<function getattr>, 'class', None, None) -> elem.attrib['class']
            # self['Classe'] = getattr(elem, 'attrib')['class'][None, None]

            self[tag] = function(elem, method)[attrib][start:end]

            print(self[tag])

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
        # dopo aver impostato il nome torna quà
        # se key == 'name'
        if key == 'name' and item:
            self.__parse(item)

        # finito di fare i cambiamenti chiamo il set del padre
        ManagedObjects.__setitem__(self, key, item)

def test():

    data = []
    root = xml.etree.ElementTree.parse('./test1.xml').getroot()[0]
    for elem in root.findall("{raml20.xsd}managedObject"):
        data.append(elem)
        elem = ManagedObject()
        print elem

    print data

if __name__ == '__main__':

    #filename = './test1.xml'
    #print ManagedObject(filename)

    test()
