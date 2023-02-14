# File Reading an Writing
import os
# XML Parser
import xml.etree.ElementTree as ET
# RegEx
import re
# Used to save dictionary to json file
import json

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
        # Extracts the complete comment of one party. 
        # If the comments of multiple parties are recorded in a single tag, then they are also captured
        # Only process comment if it is a party comment (excludes Beifälle, etc.)
        fraktion = re.findall(r"(\[(DIE LINKE|SPD|AfD|CDU\/CSU|FDP|BÜNDNIS 90\/DIE GRÜNEN)\]:.+?(–|\)))", text.text.replace("\xa0", " "))

        # Iterates over all found occurences of comments per <kommentar>-tag
        # Then saves the contents as party name and comment content
        # This is then appended to the list of comments 
        for kommentar in fraktion:
            kommentarfraktion = re.split(": ", kommentar[0])[0]
            kommentarinhalt = re.split(": ", kommentar[0])[1].replace(")", "").replace(" –", "")
            kommentarliste.append((kommentarfraktion, kommentarinhalt))

    # Saves the recorded contents of a single <rede> into a dictionary
    # the structure is described above (line 28-31)
    rededict[rede.attrib['id']] = (redefraktion, redeinhalt, kommentarliste)

#print(rededict['ID20100100'])
#print(rededict)
for key in rededict:
    print(key, '->', rededict[key])
    print('')

# Saves dictionary as json file
out_file = open("BundestagsRedenSample.json", "w", encoding='utf8')
json.dump(rededict, out_file, indent = 4, ensure_ascii=False)

###################################################################
###################################################################

# TODO:: iterate over all files, to generate complete dictionary

rededict = {}

# Initializes the content of one file (plenarliste[0]) as an ElementTree
# so that we can use the methods of the xml parser on it
for plenarsitzung in plenarliste:
    tree = ET.ElementTree(ET.fromstring(plenarsitzung))
    # sets the root of the xml file
    root = tree.getroot()
    print("noch alles ok")
    # Our central dictionary which contains an ID, the party from which the speech originates, speechcontent,  
    # Party from which a comment originates and the content of the comment itself
    # Struktur des rededict:
    # Struktur: {'id':[RedeFraktion,RedeInhalt,[Topics],[KommentarFraktion,KommentarInhalt,Sentiment,SentimentWert]]}

    #print("Inhalt aller Reden im Dokument:")
    # Iterates over the whole xml text and pulls the content from the <rede>-tags
    for rede in root.iter('rede'):
        print(rede.attrib)
        if rede.find("p/redner/name/fraktion") != None:
            redefraktion = rede.find("p/redner/name/fraktion").text.replace("\xa0", " ")
        else:
            redefraktion = rede.find("p/redner/name/nachname").text.replace("\xa0", " ")
        redeinhalt = ""
        # Saves the contents from the <p>-tags of a <rede> into one string (redeinhalt)
        for i, text in enumerate(rede.findall('p')):
            if i > 0:
                redeinhalt += text.text.replace("\xa0", " ")

        # List of all comments of one <rede>
        kommentarliste = []
        # Iterates over all comments <kommentare> of a <rede>
        for i, text in enumerate(rede.findall('kommentar')):
            # Extracts the complete comment of one party. 
            # If the comments of multiple parties are recorded in a single tag, then they are also captured
            # Only process comment if it is a party comment (excludes Beifälle, etc.)
            fraktion = re.findall(r"(\[(DIE LINKE|SPD|AfD|CDU\/CSU|FDP|BÜNDNIS 90\/DIE GRÜNEN)\]:.+?(–|\)))", text.text.replace("\xa0", " "))

            # Iterates over all found occurences of comments per <kommentar>-tag
            # Then saves the contents as party name and comment content
            # This is then appended to the list of comments 
            for kommentar in fraktion:
                kommentarfraktion = re.split(": ", kommentar[0])[0]
                kommentarinhalt = re.split(": ", kommentar[0])[1].replace(")", "").replace(" –", "")
                kommentarliste.append((kommentarfraktion, kommentarinhalt))

        # Saves the recorded contents of a single <rede> into a dictionary
        # the structure is described above (line 28-31)
        rededict[rede.attrib['id']] = (redefraktion, redeinhalt, kommentarliste)

#print(rededict['ID20100100'])
#print(rededict)
#for key in rededict:
#    print(key, '->', rededict[key])
#    print('')

# Saves dictionary as json file
out_file = open("BundestagsReden.json", "w", encoding='utf8')
json.dump(rededict, out_file, indent = 4, ensure_ascii=False)