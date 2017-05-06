# necessary imports
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

# draw plots inline rather than in a seperate window
%matplotlib inline
# draw plots bigger
plt.rcParams["figure.figsize"] = [20.0, 10.0]

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
def drawmap(pts, export=False):
    corners = findCorners(pts)
    m = Basemap(llcrnrlon=corners[0]-1, llcrnrlat=corners[2]-1, urcrnrlon=corners[1]+1, urcrnrlat=corners[3]+1, resolution='i')
    m.drawmapboundary(fill_color='0.6')
    m.drawcountries(linewidth=1.0, color='0.6')
    m.fillcontinents(color='white', lake_color='white')
    for p in pts: # draw points
        x, y = m(p[0], p[1])
        m.plot(x, y, 'bo')
    for i in range(len(pts)-1): # draw lines
        m.plot([pts[i][0], pts[i+1][0]], [pts[i][1], pts[i+1][1]], color='blue');
    if export:
        plt.savefig('map1.png');
    plt.show()

points = [[6, 46.5], [7, 47], [6, 47], [9, 46], [10, 48], [30, 80]]
drawmap(points, lines=False)
