# -*- coding: utf-8 -*-

import urllib.request
import requests

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

# upload config
def uploadMap():
    upload_filename = "map1.png"

    # read local file
    upload_file = open(upload_filename,"rb")
    upload_contents = upload_file.read()
    upload_file.close()

    # setting parameters for upload
    # ref: https://www.mediawiki.org/wiki/API:Upload
    payload={'action':'upload','filename':upload_filename, 'ignorewarnings':1, 'token':edit_token}
    files={'file':upload_contents}

    # upload the image
    print("Uploading file to %s via API..." % (baseurl+"index.php/Fichier:"+upload_filename))
    r4=requests.post(baseurl+'api.php',data=payload,files=files,cookies=edit_cookie)

    # in case of error print the response
    #print(r4.text)

uploadMap()
