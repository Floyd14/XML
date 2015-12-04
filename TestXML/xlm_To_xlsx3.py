# -*- coding: UTF-8 -*-

"""

"""

import xml.etree.ElementTree
import openpyxl

class manObj():
    """
    Una lista [...] 
    
    iterabile = può essere richiamata in un for loop
    """
    
    def __init__ (self):
        self.manObj = {}
        
    def __iter__(self):
        
    
    def __init__(self, 
                 num = 0,
                 sorgente = "",
                 destinazione = "",
                 classe = "",
                 lac = "",
                 targhet = "",
                 has_lac = False):
        
        # identificativo lista
        self.num = num
        # param in list
        self.classe = classe
        self.sorgente = sorgente
        self.destinazione = destinazione
        self.has_lac = has_lac
        self.lac = lac
        self.target = targhet
        # Si crea
        self.create()

    def create(self, xmlfile = "./test1.xml"):
        # node of xmlfile where there are manageobjects
        node = xml.etree.ElementTree.parse(xmlfile).getroot()[0]
        managed_objs = node.findall('{raml20.xsd}managedObject') # to improve with namespace ...

        # per tutti gli oggetti
        for managed_obj in managed_objs:
            name = managed_obj.attrib['name']
            self.sorgente = name[:7]
            self.destinazione = name[11:]
            self.cls = managed_obj.attrib['class']
            return self



    def get_manObj(self):
        manObj = {"Classe" : self.cls,
                  "Sorgente" : self.sorgente,
                  "Destinazione" : self.destinazione,
                  "LAC" : self.lac,
                  "Target" : self.target,
                  "??" : self.has_lac}

        return manObj


