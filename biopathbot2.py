import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import math
import datetime
from geopy.geocoders import Nominatim
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

# draw plots inline rather than in a seperate window
#%matplotlib inline
# draw plots bigger
plt.rcParams["figure.figsize"] = [20.0, 10.0]

user='BioPathBot'
passw='chkiroju'
baseurl='http://wikipast.epfl.ch/wikipast/'
summary='Wikipastbot update'
protected_logins=["Frederickaplan","Maud","Vbuntinx","Testbot","IB","SourceBot","PageUpdaterBot","Orthobot","BioPathBot","ChronoBOT","Amonbaro","AntoineL","AntoniasBanderos","Arnau","Arnaudpannatier","Aureliver","Brunowicht","Burgerpop","Cedricviaccoz","Christophe","Claudioloureiro","Ghislain","Gregoire3245","Hirtg","Houssm","Icebaker","JenniCin","JiggyQ","JulienB","Kl","Kperrard","Leandro Kieliger","Marcus","Martin","MatteoGiorla","Mireille","Mj2905","Musluoglucem","Nacho","Nameless","Nawel","O'showa","PA","Qantik","QuentinB","Raphael.barman","Roblan11","Romain Fournier","Sbaaa","Snus","Sonia","Tboyer","Thierry","Titi","Vlaedr","Wanda"]
depuis_date='2017-05-02T16:00:00Z'
liste_pages=[]
for user in protected_logins:
    result=requests.post(baseurl+'api.php?action=query&list=usercontribs&ucuser='+user+'&format=xml&ucend='+depuis_date)
    soup=BeautifulSoup(result.content,'lxml')
    for primitive in soup.usercontribs.findAll('item'):
        liste_pages.append(primitive['title'])

names=list(set(liste_pages))
for title in names:
    print(title)

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

#setup geolocator
geolocator = Nominatim(timeout=10)


# upload config
def uploadMap(filename):

    # read local file
    upload_file = open(filename,"rb")
    upload_contents = upload_file.read()
    upload_file.close()

    # setting parameters for upload
    # ref: https://www.mediawiki.org/wiki/API:Upload
    payload={'action':'upload','filename':filename, 'ignorewarnings':1, 'token':edit_token}
    files={'file':upload_contents}

    # upload the image
    print("Uploading file to %s via API..." % (baseurl+"index.php/Fichier:"+filename))
    r4=requests.post(baseurl+'api.php',data=payload,files=files,cookies=edit_cookie)

    # in case of error print the response
    #print(r4.text)


def addToPage(name, img):
    title = name + " BioPathBot"
    content = "[[Fichier: "+ img +"]]"
    pageToChange = requests.post(baseurl+'api.php?action=query&titles='+title+'&export&exportnowrap')
    payload={'action':'edit','assert':'user','format':'json','utf8':'','text':content,'summary':summary,'title':title,'token':edit_token}
    r4=requests.post(baseurl+'api.php',data=payload,cookies=edit_cookie)

# @TODO not get post-mortem data -> check Décès 
# BioPathBot : add line of databiographie to the right page (time and space)
def getDataFromPage(name):
    data = []
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

        # get date if exist
        date = re.findall("((?<=\[\[)\d*(\.*\d*\.*\d*)*(?=\]\]))",line)
        dateToAdd = ""

        if len(date) != 0 :
            dateToAdd = date[0][0]

        # get place if exist
        place = re.findall("(?<=\/\s\[\[)[A-zÀ-ÿ]*(?=\]\])",line)
        location = ""
        if len(place) != 0:
             placeToAdd = place[0]
             location = geolocator.geocode(placeToAdd)

        # if both the date and the location are available, append in data array
        if dateToAdd and location:
            dataToAdd = [location.longitude,location.latitude];
            data.append(dataToAdd);
    return data


# finds the minimal and maximal longitude and latitude
def findCorners(pts):
    minlon = maxlon = pts[0][0]
    minlat = maxlat = pts[0][1]
    for p in pts:
        currlon = p[0]
        if currlon<minlon:
            minlon = currlon
        elif currlon>maxlon:
            maxlon = currlon

        currlat = p[1]
        if currlat<minlat:
            minlat = currlat
        elif currlat>maxlat:
            maxlat = currlat

    return [minlon, maxlon, minlat, maxlat]

# draws the map, some points and the lines
def drawmap(pts, filename, export=False):
    if pts.amount() != 0:
        corners = findCorners(pts)
        m1 = Basemap(llcrnrlon=corners[0]-1, llcrnrlat=corners[2]-1, urcrnrlon=corners[1]+1, urcrnrlat=corners[3]+1, resolution='i')
        m1.drawcountries(linewidth=1.0, color='red')
        for p in pts: # draw points
            x, y = m1(p[0], p[1])
            m1.plot(x, y, 'bo')
        for i in range(len(pts)-1): # draw lines
            m1.plot([pts[i][0], pts[i+1][0]], [pts[i][1], pts[i+1][1]], color='blue');
        if export:
            plt.savefig(filename);
        plt.show()
        return true
    else:
        return false


for name in names:
    image_filename = (name + "_biopath.png").replace(" ","_")
    data = getDataFromPage(name)
    if drawmap(data, image_filename, True):
        uploadMap(image_filename)
        addToPage(name, image_filename)
