# -*- coding: UTF-8 -*-

import xml.etree.ElementTree
import openpyxl
from UserDict import UserDict


def get_raw_element_from_xml(filename='./test3.xml',
                             obj_name="{raml20.xsd}managedObject"):
    root = xml.etree.ElementTree.parse(filename).getroot()[0]
    for elem in root.findall(obj_name):
        x = ManagedObject(elem)
        print x


def create_xlsx(filename='./test3.xml',
                obj_name="{raml20.xsd}managedObject",
                dest_filename='xmlTest3.xlsx'):
    workbook = openpyxl.Workbook()
    my_wb = workbook.active
    my_wb.title = filename[2:-4]

    param = ('Sorgente', 'Destinazione', 'Classe', 'Lac')

    root = xml.etree.ElementTree.parse(filename).getroot()[0]
    for elem in root.findall(obj_name):
        x = ManagedObject(elem)
        print x
        raw = [x[par] for par in list(param)]
        my_wb.append(raw)

    # Save the file
    workbook.save(filename=dest_filename)


class ManagedObjects(UserDict):
    # Classe conteiner #
    # Quando inizializzo questa classe si inizializza anche la classe derivata!
    # (Prima questa e poi la derivata)

    def __init__(self, raw_obj=None):
        UserDict.__init__(self)
        self.name = id(raw_obj)  # -> chiamo self.__setitem__(self, name, id(raw_obj))
        # self.raw_obj = raw_obj # come lo gestisco ? sto chiamando __init??
        self['raw_obj'] = raw_obj  # -> chamo self.__setitem__(self, 'raw_obj', raw_obj)


class ManagedObject(ManagedObjects):
    # Mappa (è un dictionary) di cosa chiamare:
    # tag : (funzione da chiamare, metodo, nome dell'attributo, inizio e fine dello slice
    xmlMap = {"Sorgente": ('get', 'name', 0, 7),
              "Destinazione": ('get', 'name', 11, None),
              "Classe": ('get', 'class', None, None),
              # "AdjgLac"     :   ('attrib',  'name', None, None),
              # "Target"      :   ('attrib',  'name', None, None)
              }

    # objs_name = "{raml20.xsd}managedObject"

    def __repr__(self):
        # for print the ManagedObject
        a = "Dictionary (id:{}) = ".format(self.name)
        b = "{} -> {}".format(self['Sorgente'], self['Destinazione'])
        c = "\n\tClasse: {}\n\tLac: {}".format(self['Classe'], self['Lac'])
        d = "\n\tSubzona:    {} -> {}" \
            "\n\tSettore:     {} -> {}" \
            "\n\tSiteCode: {} -> {}".format(self['SSubzona'], self['DSubzona'],
                                            self['SSettore'], self['DSettore'],
                                            self['SSiteCode'], self['DSiteCode'])
        e = "\n{}, Protocollo: {}\n".format(self['Relazione'], self['Protocollo'])

        return a + b + c + d + e

    def __parse(self, item):
        # item è un raw_obj
        self.clear()

        for tag, (method, attrib, start, end) in self.xmlMap.items():
            # al primo ciclo vale: "Classe", (<function getattr>, 'class', None, None) -> elem.attrib['class']
            # self['Classe'] = getattr(elem, 'attrib')['class'][None, None]

            self[tag] = getattr(item, method)(attrib)[start:end]
            # print(self[tag])

        # Prendo la LAC
        if self['Classe'] == 'ADJG':
            self['Lac'] = str([getattr(p, 'text') for p in list(item)
                               if getattr(p, 'get')('name') == 'AdjgLAC'])

        else:
            self['Target'] = str([getattr(p, 'text')[10:-21] for p in list(item)
                                  if getattr(p, 'get')('name') == 'TargetCellDN'])

            self['Lac'] = self['Target']

        self['SSubzona'] = self['Sorgente'][:2]
        self['SSiteCode'] = self['Sorgente'][2:-1]
        self['SSettore'] = self['Sorgente'][-1:]

        self['DSubzona'] = self['Destinazione'][:2]
        self['DSiteCode'] = self['Destinazione'][2:-1]
        self['DSettore'] = self['Destinazione'][-1:]

        carrier1 = ('1', '4', '7')
        carrier2 = ('2', '5', '8')
        carrier3 = ('3', '6', '9')

        rel1 = '3G <-> 3G (stessa carrier)'
        rel2 = '3G <-> 3G (diversa carrier)'
        rel3 = '3G -> 2G'

        if self['Classe'] == 'ADJS':
            self['Relazione'] = rel1

            if self['SSettore'] and self['DSettore'] in (carrier1, carrier2):
                self['Protocollo'] = 'ADJS_OPI'

            else:
                self['Protocollo'] = 'ADJS_OPI_ F3'

        if self['Classe'] == 'ADJG':
            self['Relazione'] = rel3
            self['Protocollo'] = '??'

        if self['Classe'] == 'ADJI':
            self['Relazione'] = rel2
            self['Protocollo'] = '??'

        else:
            self['Relazione'] = '?'
            self['Protocollo'] = '??'

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


import Tkinter
import ttk


def create_gui():
    top = Tkinter.Tk()
    # Code to add widgets will go here...
    top.geometry("300x280+300+300")
    app = Example(top)

    top.mainloop()


from PIL import Image, ImageTk
from Tkinter import Tk, Label, BOTH
from ttk import Frame, Style


class Example(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("XML To XLSX")
        self.pack(fill='both', expand=1)

        canvas = Tkinter.Canvas(self)
        canvas.create_text(20, 30, anchor=Tkinter.W, font="Purisa",
                           text="Drag and Drop your XML file here")

        canvas.pack(fill=Tkinter.BOTH, expand=1)


if __name__ == '__main__':
    # get_raw_element_from_xml()
    create_xlsx()
    # create_gui()
