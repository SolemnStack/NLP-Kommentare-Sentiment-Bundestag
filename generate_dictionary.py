# File Reading an Writing
import os
# XML Parser
import xml.etree.ElementTree as ET
# RegEx
import re

# Reads all files in BundestagOpenData and save Path into a list (path_to_files)
path_to_folder = 'BundestagOpenData/'
path_to_files=sorted([os.path.join(path_to_folder, f) for f in os.listdir(path_to_folder)])
#print(path_to_files)

# Iterates over all the xml files and saves the contents into a list (plenarliste)
# Every list element contains the content of one file
plenarliste = []
for my_file in path_to_files:
    with open(my_file, 'r', encoding='utf-8') as f:
        plenarliste.append(f.read())

#print(plenarliste[0])

# Initializes the content of one file (plenarliste[0]) as an ElementTree
# so that we can use the methods of the xml parser on it
tree = ET.ElementTree(ET.fromstring(plenarliste[0]))
# sets the root of the xml file
root = tree.getroot()

# Our central dictionary which contains an ID, the party from which the speech originates, speechcontent,  
# Party from which a comment originates and the content of the comment itself
# Struktur des rededict:
# Struktur: {'id':[RedeFraktion,RedeInhalt,[Topics],[KommentarFraktion,KommentarInhalt,Sentiment,SentimentWert]]}
rededict = {}

print("Inhalt aller Reden im Dokument:")
# Iterates over the whole xml text and pulls the content from the <rede>-tags
for rede in root.iter('rede'):
    redefraktion = rede.find("p/redner/name/fraktion").text.replace("\xa0", " ")
    redeinhalt = ""
    # Saves the contents from the <p>-tags of a <rede> into one string (redeinhalt)
    for i, text in enumerate(rede.findall('p')):
        if i > 0:
            redeinhalt += text.text.replace("\xa0", " ")

    # List of all comments of one <rede>
    kommentarliste = []
    # Iterates over all comments <kommentare> of a <rede>
    for i, text in enumerate(rede.findall('kommentar')):
        # Saves the party name of a comment
        # TODO:: RegEx needs to be refined
        fraktion = re.search(r"\[(DIE LINKE|SPD|AfD|CDU\/CSU|FDP|BÜNDNIS 90\/DIE GRÜNEN)\]:", text.text.replace("\xa0", " "))
        # Only process comment if it is a party comment (excludes Beifälle, etc.)
        if fraktion != None:
            start, end = fraktion.span()
            kommentarfraktion = text.text[start:end-1]
            kommentarinhalt = re.split(":" ,text.text)[1].replace("\xa0", " ")
            kommentarliste.append((kommentarfraktion, kommentarinhalt))

    rededict[rede.attrib['id']] = (redefraktion, redeinhalt, kommentarliste)

#print(rededict['ID20100100'])
#print(rededict)
for key in rededict:
    print(key, '->', rededict[key])
    print('')

##########################################################
############ Hier folgen meine Testversuche ##############
##########################################################

'''
import requests

plenarliste = []
wahlperiode = 20
protokollnummer = 1
listennummer = 0
while protokollnummer < 84:
    response = requests.get("https://search.dip.bundestag.de/api/v1/plenarprotokoll-text?f.dokumentnummer=" + str(wahlperiode) + "/" + str(protokollnummer) + "&apikey=GmEPb1B.bfqJLIhcGAsH9fTJevTglhFpCoZyAAAdhp")
    if protokollnummer % 5 == 0:
        response.json()
    plenarliste.append(response.json()['documents'][0]['text'])
    #plenarliste[listennummer] = response.json()['documents'][0]['text']
    protokollnummer += 1

print(plenarliste)
'''

'''
print("Root Tag: " + str(root.tag))
print("Root Attribute: " + str(root.attrib))
print('')
print("Children and Attributes of Root:")
for child in root:
    print(child.tag, child.attrib)

print('')
print(root[1][0][0].text)

# Printed die ID jeder Rede im XML-Dokument
print("IDs aller Reden im Dokument:")
for rede in root.iter('rede'):
    print(rede.attrib)

print('')

print("IDs aller Tagesordnungspunkte im Dokument:")
for tagesordnungspunkt in root.iter('tagesordnungspunkt'):
    print(tagesordnungspunkt.attrib)

print('')

print("Inhalt aller Tagesordnungspunkte im Dokument:")
for tagesordnungspunkt in root.iter('tagesordnungspunkt'):
    print(tagesordnungspunkt.findall('p'))
    print(type(tagesordnungspunkt.findall('p')))
    print('')

print('')

testliste = tagesordnungspunkt.findall('p')

for textl in testliste:
    print(textl.text)

print('')

print("Inhalt aller Reden im Dokument:")
for rede in root.iter('rede'):
    print(rede.findall('p'))
    print(type(rede.findall('p')))
    print('')

print('')
print("Redeinhalt")
print('')

testliste = rede.findall('p')

print(testliste)

for textl in testliste:
    print(textl.text)
'''

# Test um Redeinhalte in eine Liste zu speichern
#redeliste = list()
#for i, tagesordnung in enumerate(root.iter('tagesordnung')):
#    redeliste.append(i)
#    for rede in root.iter('rede'):
#        redeliste[i].append(rede.findall('p'))

# Speichert alle Beiträge in Reden in eine Redeliste
# Einzelne Reden danach erreichbar mit redeliste[x]

#print('Die gesamte Redeliste')
#print(redeliste)
#print('')
#print("Ausschnitt aus Redeliste")
#print(redeliste[0])
#print('')

# Iteriert durch alle Reden hindurch und printet den Inhalt
#for rede in redeliste:
#    #print(rede)
#    #print(rede.attrib)
#    #print('')
#    for text in rede:
#        print(text.text)
#        print('')

# TODO:: Dictionary anlegen mit RedeID : Redeinhalt

# Printed die ID jeder Rede im XML-Dokument
# print("IDs aller Reden im Dokument:")
# for rede in root.iter('rede'):
#     print(rede.attrib)

# TODO:: Kommentare extrahieren. Dictionary mit Person : Kommentarinhalt

# TODO:: Dictionary mit RedeID, Fraktion des Redners, Redeinhalt, und falls vorhanden Kommentare/Beifälle und deren Fraktionen