# coding=utf-8

"""
Da Dive into Python

Esempio mostra come funzionano le classi
"""

# importo i moduli
import os
import sys
from UserDict import UserDict


def stripnulls(data):
    "strip .."
    return data.replace("\00", "").strip()

# Definisco una classe (che deriva da UserDict)
# è un Dictionary personalizzato
class FileInfo(UserDict):
    "store file metadata"

    def __init__(self, filename=None):
        UserDict.__init__(self)     # DEVO SEMPRE RICHIAMARE L'INIT DELLA CLASSE MADRE !
        self['name'] = filename     # adesso ho le proprietà della classe madre

class MP3FileInfo(FileInfo):
    "store tags"

    tagDataMap = {"titple"  :   (   3,  33, stripnulls)
                  "artist"  :   (  33,  63, stripnulls)
                  "album"   :   (  63,  93, stripnulls)
                  "year"    :   (  93,  97, stripnulls)
                  "comment" :   (  97, 126, stripnulls)
                  "genre"   :   ( 127, 128, ord)}


