from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import datetime

def plotPolygon(m,llx,lly,urx,ury,k,c='b'):
    lon = []
    lat = []
    for i in np.arange(llx,urx+k,k):
        lon.append(i)
        lat.append(lly)
    for i in np.arange(lly,ury+k,k):
        lon.append(urx)
        lat.append(i)
    for i in np.arange(urx,llx-k,-k):
        lon.append(i)
        lat.append(ury)
    for i in np.arange(ury,lly-k,-k):
        lon.append(llx)
        lat.append(i)
    m.plot(lon,lat,latlon=True,c=c,lw=2)

plt.figure(figsize=(10,7))
plt.subplots_adjust(left=0.05,right=0.98,bottom=0.05,top=0.95)
#m = Basemap(projection='ortho',lon_0=113.5,lat_0=23,resolution='l',\
#    llcrnrx=-700000.,llcrnry=-400000.,urcrnrx=700000.,urcrnry=400000)
m = Basemap(llcrnrlon=40,urcrnrlon=190,llcrnrlat=-40,urcrnrlat=60,resolution='l')
#m.drawcoastlines(linewidth=0.8)
m.fillcontinents(color='#CCCCCC')
m.drawmeridians(np.arange(0, 360, 10), linewidth=0.5, dashes=[1, 2],labels=[0,0,0,1])
m.drawparallels(np.arange(-90, 90, 10), linewidth=0.5, dashes=[1, 2],labels=[1,0,0,0])
#m.nightshade(datetime.datetime.now())
plotPolygon(m,120,-30,180,50,1)
plotPolygon(m,50,-30,120,20,1)
plotPolygon(m,80,0,120,20,1)
plotPolygon(m,80,20,120,50,1)
plotPolygon(m,107,26,120,50,1)
plotPolygon(m,107,20,120,26,1,c='r')
plt.plot([0,0],[0,0],c='b',label='Vapor Source Area',lw=2)
plt.plot([0,0],[0,0],c='r',label='Target Area',lw=2)
plt.text(113.5,22.5,"SC",zorder=10,ha='center',va='center',size=20)
plt.text(150,10,"WP",zorder=10,ha='center',va='center',size=20)
plt.text(113.5,38,"EC",zorder=10,ha='center',va='center',size=20)
plt.text(93.5,35,"IA",zorder=10,ha='center',va='center',size=20)
plt.text(100,10,"BSC",zorder=10,ha='center',va='center',size=20)
plt.text(85,-10,"IO",zorder=10,ha='center',va='center',size=20)
plt.title("Vapor Source Areas")
plt.legend(loc=1)
plt.text(45,55,"Target Area: Southern China (107°E~120°E, 20°N~26°N)",size=13,va='center')
plt.show()