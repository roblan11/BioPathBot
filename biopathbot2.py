
import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import math
import datetime
from geopy.geocoders import Nominatim

def degre_to_radiant(data):
    radiant=data*math.pi/180.0
    return radiant

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

#setup geolocator
geolocator = Nominatim()

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

        # get date if exist
        date = re.findall("((?<=\[\[)\d*(\.*\d*\.*\d*)*(?=\]\]))",line)
        date_convert = ""

        if len(date) != 0 :
            dateToAdd = date[0][0]

            if re.match("\d+\.\d+\.\d+", dateToAdd):
                the_date=datetime.datetime.strptime(dateToAdd, "%Y.%m.%d")
            elif re.match("\d+\.\d+", dateToAdd):
                the_date=datetime.datetime.strptime(dateToAdd, "%Y.%m")
            else:
                the_date=datetime.datetime.strptime(dateToAdd, "%Y")

            timestamp=(the_date-datetime.datetime(1970, 1, 1)).total_seconds()+36
            convert=int(1.0*timestamp/(24*3600))
            date_convert = str(convert)
            # print(str(date)+' => '+str(convert))
            print(date_convert)

        # get place if exist
        place = re.findall("(?<=\/\s\[\[)[A-zÀ-ÿ]*(?=\]\])",line)
        place_convert = ""
        if len(place) != 0:
             placeToAdd = place[0]

             location = geolocator.geocode(placeToAdd)

             pos_lieux = [[location.latitude, location.longitude,0]]
             print(pos_lieux)
"""
             pos_lieux_rad=[]
             for i in range(len(pos_lieux)):
                 temp=[]
                 temp.append(degre_to_radiant(pos_lieux[i][0]))
                 temp.append(degre_to_radiant(pos_lieux[i][1]))
                 temp.append(pos_lieux[i][2])
                 pos_lieux_rad.append(temp)

             pos_lieux_convert=[]

             LE_GEODESY_LMIN=-1.0*math.pi
             LE_GEODESY_LMAX=1.0*math.pi
             LE_GEODESY_AMIN=-1.0*math.pi/2.0
             LE_GEODESY_AMAX=1.0*math.pi/2.0
             LE_GEODESY_HMIN=-2*math.pi*6378137.0/1024.0
             LE_GEODESY_HMAX=2*math.pi*6378137.0/1024.0

             for i in range(len(pos_lieux)):
                 le_pose=pos_lieux_rad[i]
                 longeur_adress=20
                 le_address=longeur_adress*[0]

                 le_buffer=0
                 le_parse=0

                 le_pose[0]=(le_pose[0]-LE_GEODESY_LMIN)/(LE_GEODESY_LMAX-LE_GEODESY_LMIN)
                 le_pose[1]=(le_pose[1]-LE_GEODESY_AMIN)/(LE_GEODESY_AMAX-LE_GEODESY_AMIN)
                 le_pose[2]=(le_pose[2]-LE_GEODESY_HMIN)/(LE_GEODESY_HMAX-LE_GEODESY_HMIN)

                 for le_parse in range(longeur_adress):
                     if le_pose[0] >= 0.5:
                         le_buffer = 1
                     else:
                         le_buffer = 0
                     le_address[le_parse]=le_buffer
                     le_pose[0] = ( le_pose[0] * 2.0 ) - le_buffer

                     if le_parse >= 1:
                         if le_pose[1] >= 0.5:
                             le_buffer = 1
                         else:
                             le_buffer = 0
                         le_address[le_parse]=le_address[le_parse]+le_buffer*2
                         le_pose[1]=(le_pose[1]*2.0)-le_buffer

                         if(le_parse>=10):
                             if le_pose[2]>=0.5:
                                 le_buffer=1
                             else:
                                 le_buffer=0
                             le_address[le_parse]=le_address[le_parse]+le_buffer*4
                             le_pose[2]=(le_pose[2]*2.0)-le_buffer
                 for j in range(len(le_address)):
                     le_address[j]=str(le_address[j])
                 place_convert = ''.join([str(x) for x in le_address])

                 # print(placeToAdd + ' => '+place_convert)

        # if both the date and the location are available, create a new page
        # or append to an existing page
        if date_convert and place_convert:
            # TODO: add new spatiotemporal page
            print("create new page " + place_convert + ":" + date_convert)
            """
