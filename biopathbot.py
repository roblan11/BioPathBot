
import urllib.request
import requests
from bs4 import BeautifulSoup
import re

user='BioPathBot'
passw='chkiroju'
baseurl='http://wikipast.epfl.ch/wikipast/'
summary='Wikipastbot update'
names=['Henri Dunant']

# Login request
payload={'action':'query','format':'json','utf8':'','meta':'tokens','type':'login'}
r1=requests.post(baseurl + 'api.php', data=payload)

#login confirm
login_token=r1.json()['query']['tokens']['logintoken']
payload={'action':'login','format':'json','utf8':'','lgname':user,'lgpassword':passw,'lgtoken':login_token}
r2=requests.post(baseurl + 'api.php', data=payload, cookies=r1.cookies)

#get edit token2
params3='?format=json&action=query&meta=tokens&continue='
r3=requests.get(baseurl + 'api.php' + params3, cookies=r2.cookies)
edit_token=r3.json()['query']['tokens']['csrftoken']

edit_cookie=r2.cookies.copy()
edit_cookie.update(r3.cookies)


# BioPathBot : add line of databiographie to the right page (time and space)
for name in names:
    result=requests.post(baseurl+'api.php?action=query&titles='+name+'&export&exportnowrap')
    soup=BeautifulSoup(result.text, "lxml")
    #soup=BeautifulSoup(result.text)
    code=''
    for primitive in soup.findAll("text"):
        code+=primitive.string

    # split on list (*)
    lines = code.split("*")
    for line in lines :

        # add breaking lines (otherwise will be appened directly in one line)
        line = "\n\n"+line

        # get date if exist and append line to the page
        date = re.findall("((?<=\[\[)\d*(\.*\d*\.*\d*)*(?=\]\]))",line)
        if len(date) != 0 :
            dateToAdd = date[0][0]
            pageToChange = requests.post(baseurl+'api.php?action=query&titles='+dateToAdd+'&export&exportnowrap')
            payload={'action':'edit','assert':'user','format':'json','utf8':'','appendtext':line,'summary':summary,'title':dateToAdd,'token':edit_token}
            r4=requests.post(baseurl+'api.php',data=payload,cookies=edit_cookie)


        # get place if exist and append line to the page
        place = re.findall("(?<=\/\s\[\[)[A-zÀ-ÿ]*(?=\]\])",line)
        if len(place) != 0:
            placeToAdd = place[0]
            pageToChange = requests.post(baseurl+'api.php?action=query&titles='+placeToAdd+'&export&exportnowrap')
            payload={'action':'edit','assert':'user','format':'json','utf8':'','appendtext':line,'summary':summary,'title':placeToAdd,'token':edit_token}
            r4=requests.post(baseurl+'api.php',data=payload,cookies=edit_cookie)
