# necessary imports
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from colorsys import hsv_to_rgb
from matplotlib.colors import rgb2hex
import numpy as np
SEGMENTS = 100

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
def drawmap(pts, filename, export=False):
    n_pts = len(pts)
    corners = findCorners(pts)
    m = Basemap(llcrnrlon=corners[0]-1, llcrnrlat=corners[2]-1, urcrnrlon=corners[1]+1, urcrnrlat=corners[3]+1, resolution='i')
    m.drawmapboundary(fill_color='0.6')
    m.drawcountries(linewidth=1.0, color='0.6')
    m.fillcontinents(color='white', lake_color='white')
    for i in range(n_pts-1): # draw lines
        for j in range(SEGMENTS):
            start = pts[i] + (pts[i+1]-pts[i])*(j/SEGMENTS)
            end = pts[i] + (pts[i+1]-pts[i])*((j+1)/SEGMENTS)
            m.plot([start[0], end[0]], [start[1], end[1]], color=hsv_to_rgb((i+j/SEGMENTS)/n_pts, 1, 1))
    for i in range(n_pts): # draw points
        m.plot(pts[i][0], pts[i][1], marker='o', color=hsv_to_rgb(i/n_pts, 1, 1), fillstyle='full', markeredgewidth=0.0)
    if export:
        plt.savefig(filename, bbox_inches='tight')
    plt.show()

# points to test
points = [[1, 1], [1, 10], [2, 1], [2, 10], [3, 1], [3, 10], [4, 1], [4, 10], [5, 1], [5, 10], [6, 1], [6, 10], [7, 1], [7, 10], [8, 1], [8, 10], [9, 1], [9, 10], [10, 1], [10, 10]]
drawmap(np.array(points), "map1.png", True)
