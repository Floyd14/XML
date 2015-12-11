# -*- coding: UTF-8 -*-

import xml.etree.ElementTree
import openpyxl
from UserDict import UserDict

import re

import Tkinter
import ttk


def get_raw_element_from_xml(filename='./test3.xml',
                             obj_name="{raml20.xsd}managedObject"):
    root = xml.etree.ElementTree.parse(filename).getroot()[0]
    for elem in root.findall(obj_name):
        x = ManagedObject(elem)
        print x


def create_xlsx(filename='./test3.xml',
                obj_name="{raml20.xsd}managedObject",
                dest_filename='xmlTest3.xlsx'):

    data = []

    workbook = openpyxl.Workbook()
    my_wb = workbook.active
    my_wb.title = filename[2:-4]

    param = ('Sorgente', 'SSubzona', 'SSiteCode', 'SSettore',
             'Destinazione', 'DSubzona', 'DSiteCode', 'DSettore',
             'Classe', 'Lac', 'Relazione', 'Protocollo')

    root = xml.etree.ElementTree.parse(filename).getroot()[0]
    for elem in root.findall(obj_name):
        x = ManagedObject(elem)
        print x
        raw = [x[par] for par in list(param)]
        data.append(raw)
        my_wb.append(raw)

    for raw in data:
        print raw

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
              "Target": ('get', 'distName', None, None)
              }

    # objs_name = "{raml20.xsd}managedObject"

    def __repr__(self):
        # for print the ManagedObject
        try:
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

        except KeyError:
            pass

    def __parse(self, item):
        # item è un raw_obj
        self.clear()

        # inizializzo le chuiavi
        keys = ('Sorgente', 'Destinazione', 'Classe', 'Lac', 'Target', 'RNC',
                'SSubzona', 'SSiteCode', 'SSettore',
                'DSubzona', 'DSiteCode', 'DSettore',
                'Relazione', 'Protocollo')

        for key in keys:
            self[key] = 0

        # Definisco Sorgente, Destinazione e Classe
        for tag, (method, attrib, start, end) in self.xmlMap.items():
            # al primo ciclo vale: "Classe", (<function getattr>, 'class', None, None) -> elem.attrib['class']
            # self['Classe'] = getattr(elem, 'attrib')['class'][None, None]
            self[tag] = getattr(item, method)(attrib)[start:end]
            # print(self[tag])

        self['SSubzona'] = self['Sorgente'][:2]
        self['SSiteCode'] = int(self['Sorgente'][2:-1])
        self['SSettore'] = int(self['Sorgente'][-1:])

        self['DSubzona'] = self['Destinazione'][:2]
        self['DSiteCode'] = int(self['Destinazione'][2:-1])
        self['DSettore'] = int(self['Destinazione'][-1:])

        # Prendo l'RNC
        pattern = re.compile(r"(D*)(RNC-)(\d{3}|\d{2})(D*)")
        rnc = re.search(pattern, str(self['Target']))
        self['RNC'] = rnc.group(3)

        # Prendo la LAC
        if self['Classe'] == 'ADJG':
            self['Lac'] = int([getattr(p, 'text') for p in list(item)
                               if getattr(p, 'get')('name') == 'AdjgLAC'][0])


        elif self['Classe'] == 'ADJI':

            self['Lac'] = '(RNC) {}'.format(self['RNC'])

        elif self['Classe'] == 'ADJL':
            self['Lac'] =  '(RNC) {}'.format(self['RNC'])

        else:
            self['Lac'] = '(RNC) {}'.format(self['RNC'])

        carrier1 = (1, 4, 7)
        carrier2 = (2, 5, 8)
        carrier3 = (3, 6, 9)

        gsm = (1, 2, 3)
        dcs = (7, 8, 9)

        rel1 = '3G <-> 3G (stessa carrier)'
        rel2 = '3G <-> 3G (diversa carrier)'
        rel3 = '3G -> 2G'

        # ADJS
        if self['Classe'] == 'ADJS':
            self['Relazione'] = rel1

            if self['SSettore'] and self['DSettore'] in (carrier1, carrier2):
                self['Protocollo'] = 'ADJS_OPI'

            else:
                self['Protocollo'] = 'ADJS_OPI_ F3'

        # ADJG
        elif self['Classe'] == 'ADJG':
            self['Relazione'] = rel3

            if self['DSettore'] in gsm:
                self['Relazione'] = rel3 + ' GSM'
                self['Protocollo'] = 'DEFAULT'

            elif self['DSettore'] in dcs:
                self['Relazione'] = rel3 + ' DCS'
                self['Protocollo'] = 'ADJG1900_OPI'

        # ADJI
        elif self['Classe'] == 'ADJI':
            self['Relazione'] = rel2

            if self['SSettore'] in carrier1:

                if self['DSettore'] in carrier2:
                    self['Protocollo'] = 'ADGJ_OPI_RC_F1_F2'
                elif self['DSettore'] in carrier3:
                    self['Protocollo'] = 'ADGJ_OPI_RC_F1_F3'

            elif self['SSettore'] in carrier2:

                if self['DSettore'] in carrier1:
                    self['Protocollo'] = 'ADGJ_OPI_RC_F2_F1'
                elif self['DSettore'] in carrier3:
                    self['Protocollo'] = 'ADGJ_OPI_RC_F2_F3'

            elif self['SSettore'] in carrier3:

                if self['DSettore'] in carrier1:
                    self['Protocollo'] = 'ADGJ_OPI_RC_F3_F1'
                elif self['DSettore'] in carrier2:
                    self['Protocollo'] = 'ADGJ_OPI_RC_F3_F2'

        # ADJL
        elif self['Classe'] == 'ADJL':
            self['Relazione'] = 'DA IMPLEMENTARE'

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


def create_gui():
    top = Tkinter.Tk()
    # Code to add widgets will go here...
    top.geometry("300x280+300+300")
    app = Example(top)

    top.mainloop()

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
    #get_raw_element_from_xml()
    create_xlsx()
    # create_gui()
