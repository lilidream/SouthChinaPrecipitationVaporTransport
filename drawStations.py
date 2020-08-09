sid = [
    57947, 57957, 57965, 57972, 57993, 57996, 58715,
    58725, 58730, 58731, 58734, 58737, 58752, 58754, 58813,
    58820, 58834, 58846, 58847, 58911, 58918, 58921, 58926,
    58927, 58931, 58933, 58944, 59007, 59021, 59023, 59037,
    59046, 59058, 59065, 59072, 59082, 59087, 59096, 59102,
    59117, 59126, 59133, 59134, 59209, 59211, 59218, 59228,
    59242, 59254, 59265, 59271, 59278, 59287, 59293, 59294,
    59298, 59303, 59316, 59317, 59321, 59324, 59417, 59431,
    59446, 59453, 59456, 59462, 59478, 59493, 59501, 59626,
    59632, 59644, 59647, 59658, 59663, 59664, 59673, 59754
]
file = open("../data/station_location.txt")
lines = file.readlines()
file.close()

s = []
lat = []
lon = []

for line in lines:
    l = line.split()
    if int(l[0]) in sid:
       s.append(int(l[0]))
       lat.append(float(l[1]))
       lon.append(float(l[2]))
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(8,4.5))
plt.subplots_adjust(left=0.08,right=0.98,top=0.96,bottom=0.05)
m = Basemap(llcrnrlon=104,llcrnrlat=16,urcrnrlon=124,urcrnrlat=32,resolution='i')
m.drawcoastlines(linewidth=0.5)
m.readshapefile("shp/gadm36_CHN_1","China")
plt.scatter(lon,lat,color='r')
plt.plot([106,120,120,106,106],[28,28,18,18,28],c='b',lw=2)
#plt.xticks(np.arange(105,125,5),[str(i)+"°E" for i in np.arange(105,125,5)])
#plt.yticks(np.arange(20,32,3),[str(i)+"°N" for i in np.arange(20,32,3)])
m.drawmeridians(np.arange(50, 165, 2), labels=[0, 0, 0, 1], linewidth=0.5, dashes=[1, 6])
m.drawparallels(np.arange(-10, 65, 2), labels=[1, 0, 0, 0], linewidth=0.5, dashes=[1, 6])
plt.show()
print(len(sid))
