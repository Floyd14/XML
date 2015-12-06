# -*- coding: UTF-8 -*-

''' XML Test exemple. 

For more info see: 
- https://docs.python.org/2/library/xml.etree.elementtree.html 
- http://www.diveintopython3.net/xml.html '''

import xml.etree.ElementTree as etree

tree = etree.parse('book.xml')
root = tree.getroot() # elements are like lists ...

# the name of root is 'catalog' ...
print '\nLa radice del file è: %s' %root.tag
print '\nIn questo catalogo ci sono %s elementi' %len(root)

#--- Loop tra figli
# printa tutto cio che è in root..
print 'Questi elementi sono:'
for child in root:
    print child.tag

print 'Posso selezionare uno specifico figlio \nES il terzo: %s' %root[2].tag
print '... e vederene gli attributi: %s (che sono dictionary)' %root[2].attrib

print '\nPosso vedere i figli dei figli:'
for child in root[2]:
    print child.tag
    
print '\nSelezionare uno specifico figlio: %s' %root[2][1].tag
print '... e vederne il valore (testo): %s' %root[2][1].text

#--- Ricerche 
print '\nPer le ricerche ho i metodi find() o findall() \nentrambi ricercano SOLO tra i figli diretti'
print '\nfind() ritorna il primo che trova: %s' %root.find('book').tag
print 'findall() ritorna una lista di quelli trovat:\n%s' %root.findall('book')


for book in root.findall('book'):
    title = book.find('title').text
    author = book.find('author').text
    author_attribute = book.get('author')
    
    print '%s, %s, %s' %(title, author, author_attribute)


