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


# classe Handler che sa derivare gli attributi, ecc e popolare il dictionary
class MP3FileInfo(FileInfo):
    "store tags"

    # Attributi di classe (per tutti gli oggetti di questa classe)
    # Non li metto in init perchè init è quando creo un istanza (oggetto) !!

    # Sono richiamabili con self.__class__.tagDataMap DOPO che è stata instanziata una classe!!
    # perchè __class__ è un attributo builtin di ongni istanza!!
    tagDataMap = {"titple"  :   (   3,  33, stripnulls),      # stripnulls è un puntatore alla funzione!
                  "artist"  :   (  33,  63, stripnulls),      # per chiamare una funzione devo scricere stripnulls()
                  "album"   :   (  63,  93, stripnulls),
                  "year"    :   (  93,  97, stripnulls),
                  "comment" :   (  97, 126, stripnulls),
                  "genre"   :   ( 127, 128, ord)}

    # METODO PRIVATO: inizia con __
    # Python non te li fa chiamare: a.__parse genera un eccezione !!
    def __parse(self, filename):
        "parse ID3v1.0 from MP3"
        self.clear()

        # Gestione delle eccezioni..
        try:
            # apertura file ( nome, modalità, buffer)
            fsock = open(filename, "rb", 0)
            try:
                fsock.seek(-128, 2)     # spostati a 128byte prima della fine del file (2 = fine del file)
                tagdata = fsock.read(128)   # leggi 128 byte (gli ultimi del file) -> è una lista

                # anche se qualcosa va storto prima vogliamo chiudere il file
                # finally viene sempre eseguito!
            finally:
                fsock.close()

            # Crea la tag
            # se gli ultimi 3 byte sono == TAG
            if tagdata[:3] == "TAG":

                # leggi da destra a sinistra
                # items() ritorna una lista dal dicionary di classe che ho definito prima
                # il dictionary di prima è composto da:
                # tag e una tuple (start, end, funzione)
                # ES: primo elemento ("title", (3, 33, <func stripnulls>)
                for tag, (start, end, parseFunc) in self.tagDataMap.items():

                    # creo l'attributo tag
                    # parse func è la funzione definita nel for
                    # che chiame quella definita in tagDataMap ma questa volta la esegue perchè ho le parentesi
                    # ES nel primo cilco viene eseguito stripnulls(XX)
                    # XX è un particolare pezzo di lista tagdata
                    self[tag] = parseFunc(tagdata[start:end])

        # vai avanti se trovi l'eccezione (NON USA raise IOError che avrebbe fermato tutto)
        except IOError:
            pass


    # Metodo che prede un elemento da un dizionario.
    # questo metodo viene chiamato da python tutte le volte che si accede al valore di una chiave di un
    # dicionary, ovvero se a è un dictionary, tutte le volte che:
    #
    # >>> a['name'] = 10 dove a è un dicionary
    # che quindi è uguale a:
    # >>> a.__setitem__('name', 10)
    #
    # key sta per la chiave del dictionary
    # idem sta per il valore della chiame

    def __setitem__(self, key, item):       # importante mantenere lo stesso numero di argomenti?

        # Se stiamo assegnando un valore alla key 'name' chiamiamo parse per fare una elaborazione aggiuntiva
        if key == "name" and item:
            self.__parse(item)

        # Richiamo il metodo dell'antenato che python da solo non chiama mai !!
        # richiamo __setitem della classe FileInfo che eredita da UserDict
        # in cui è definito __setitem__
        FileInfo.__setitem__(self, key, item)


# prende una directory e una lista di estensioni e ritorna una lista di istanze
def listDirectory(directory, fileExtList):
    "get list of file info objects for files of particular extensions"

    # os.listdir(directory) -> lista di tutti i file in directory
    # os.path.normcase(f) -> normalizza tutti i file nella lista (per sistemi case-INsensitive)

    fileList = [os.path.normcase(f) for f in os.listdir(directory)]      # è una lista NORMALIZZATA !

    # if os.path.splitext -> divide il file name in nome e estensione,
    # [1] guardo l'estensione
    # se è presente nella lista fileExtList
    # ricostruisco il percorso completo del file os.path.join(directory, f)
    fileList = [os.path.join(directory, f) for f in fileList \
                if os.path.splitext(f)[1] in fileExtList]


    # argomenti: nome file è richiesto, sys.module è opzionale
    # sys.module è un dictionary (con tutti i moduli di python)
    def getFileInfoClass(filename, module=sys.modules[FileInfo.__module__]):
        "get file info class from filename extension"

        # prende l'estensione del file,
        # upper() -> la forza in caratteri maiuscoli
        # [1:] -> affetta via il punto
        subclass = "%sFileInfo" % os.path.splitext(filename)[1].upper()[1:]  # subclass = 'MP3FileInfo'

        # se questo modulo contiene una classe con lo stesso nome di subclass
        # allora restituisci tale classe
        # altrimenti restituisci FileInfo
        return hasattr(module, subclass) and getattr(module, subclass) or FileInfo

    # se esiste ritorniamo la classe! (non una istanza)
    # per ogni file f in lista
    # chiamo getFileInfo(f) passandoglki il filename f -> ritorna una classe !
    #
    return [getFileInfoClass(f)(f) for f in fileList]

if __name__ == "__main__":
    for info in listDirectory("./testMusic", [".mp3"]):
        print "\n".join(["%s=%s" % (k, v) for k, v in info.items()])
        print


