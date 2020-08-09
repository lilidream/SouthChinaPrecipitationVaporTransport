import numpy as np

class Vapo:
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
    days = {4: 30, 5: 31, 6: 30}
    epMonth = {
        1951: [8, 9, 10, 11, 12],
        1952: [1],
        1957: [4, 5, 6, 7, 8, 9, 10, 11, 12],
        1958: [1, 2, 3, 4, 5, 6, 7],
        1963: [7, 8, 9, 10, 11, 12],
        1964: [1],
        1965: [5, 6, 7, 8, 9, 10, 11, 12],
        1966: [1, 2, 3, 4, 5],
        1972: [5, 6, 7, 8, 9, 10, 11, 12],
        1973: [1, 2, 3],
        1976: [9, 10, 11, 12],
        1977: [1, 2],
        1979: [9, 10, 11, 12],
        1980: [1],
        1982: [4, 5, 6, 7, 8, 9, 10, 11, 12],
        1983: [1, 2, 3, 4, 5, 6],
        1986: [8, 9, 10, 11, 12],
        1987: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        1988: [1, 2],
        1991: [5, 6, 7, 8, 9, 10, 11, 12],
        1992: [1, 2, 3, 4, 5, 6],
        1997: [4, 5, 6, 7, 8, 9, 10, 11, 12],
        1998: [1, 2, 3, 4],
        2006: [8, 9, 10, 11, 12],
        2007: [1],
        2014: [10, 11, 12],
        2015: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        2016: [1, 2, 3, 4]
    }
    cpMonth = {
        1968: [10, 11, 12],
        1969: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        1970: [1, 2],
        1977: [9, 10, 11, 12],
        1978: [1, 2],
        1994: [9, 10, 11, 12],
        1995: [1, 2, 3],
        2002: [5, 6, 7, 8, 9, 10, 11, 12],
        2003: [1, 2, 3],
        2004: [7, 8, 9, 10, 11, 12],
        2005: [1],
        2009: [6, 7, 8, 9, 10, 11, 12],
        2010: [1, 2, 3, 4]
    }
    coldMonth = {
        1950: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        1951: [1, 2],
        1954: [7, 8, 9, 10, 11, 12],
        1955: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        1956: [1, 2, 3, 4],
        1964: [5, 6, 7, 8, 9, 10, 11, 12],
        1965: [1],
        1970: [7, 8, 9, 10, 11, 12],
        1971: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        1972: [1],
        1973: [6, 7, 8, 9, 10, 11, 12],
        1974: [1, 2, 3, 4, 5, 6],
        1975: [4, 5, 6, 7, 8, 9, 10, 11, 12],
        1976: [1, 2, 3, 4],
        1984: [10, 11, 12],
        1985: [1, 2, 3, 4, 5, 6],
        1988: [5, 6, 7, 8, 9, 10, 11, 12],
        1989: [1, 2, 3, 4, 5],
        1995: [9, 10, 11, 12],
        1996: [1, 2, 3],
        1998: [7, 8, 9, 10, 11, 12],
        1999: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        2000: [1, 2, 3, 4, 5, 6, 10, 11, 12],
        2001: [1, 2],
        2007: [8, 9, 10, 11, 12],
        2008: [1, 2, 3, 4, 5],
        2010: [6, 7, 8, 9, 10, 11, 12],
        2011: [1, 2, 3, 4, 5, 8, 9, 10, 11, 12],
        2012: [1, 2, 3]}

    def read(self, year, month, day, hour, level):
        '''
        Read Traj data into dict.
        Input BJT of datafile and only support for 0200 & 1400,
        function will convert to 1800Z & 0600Z.
        hour: "02" or "14"
        '''
        # convert BJT to UTC
        if hour == "02":
            hour = "18"
            if day > 1:
                day -= 1
            elif day == 1 and month == 4:
                month = 3;
                day = 31
            elif day == 1 and month == 5:
                month = 4;
                day = 30
            elif day == 1 and month == 6:
                month = 5;
                day = 31
        elif hour == "14":
            hour = "06"

        # Completing date
        if day < 10:
            day = "0" + str(day)
        else:
            day = str(day)

        # open file
        file = open("../traj/"+str(level)+"/1" + str(year)[2:4] + "0" + str(month) + day + hour, 'r', encoding='utf-8')
        lines = file.readlines()
        file.close()

        # read lines
        data = {}
        mode = 0
        for line in lines:
            l = line.split()
            if mode:
                if l[0] not in data:
                    data[l[0]] = {"lat": [], "lon": [], "p": [], "sh": []}
                data[l[0]]['lat'].append(float(l[9]))
                data[l[0]]['lon'].append(float(l[10]))
                data[l[0]]['p'].append(float(l[12]))
                data[l[0]]['sh'].append(float(l[13]))
            if l[1] == "PRESSURE":
                mode = 1
        return data

    def loadPrec(self):
        import json
        file = open("../prec.json", 'r', encoding='utf-8')
        data = json.loads(file.read())
        file.close()
        return data

    def analyzeSH(self, data, sh):
        anaData = {}
        for idd in data:
            sources = []
            indexNum = []
            contin = 0
            for i in range(len(data[idd]['sh']) - 1):
                if data[idd]['sh'][i + 1] - data[idd]['sh'][i] <= sh:
                    indexNum.append(i)
                    contin = 1
                else:
                    if contin:
                        indexNum.append(i)
                        sources.append(indexNum)
                        indexNum = []
                        contin = 0
                    else:
                        indexNum = []
            if sources != []:
                diff = [data[idd]['sh'][j[0]] - data[idd]['sh'][j[len(j) - 1]] for j in sources]
                lon = [data[idd]['lon'][j] for j in sources[diff.index(max(diff))]]
                lat = [data[idd]['lat'][j] for j in sources[diff.index(max(diff))]]
                p = [data[idd]['p'][j] for j in sources[diff.index(max(diff))]]
                shh = [data[idd]['sh'][j] for j in sources[diff.index(max(diff))]]
                anaData[idd] = {'lon': lon, 'lat': lat, 'p': p, 'sh': shh, 'pathLon': data[idd]['lon'],
                                'pathLat': data[idd]['lat'], 'pathSH': data[idd]['sh']}
            else:
                anaData[idd] = {'lon': [], 'lat': [], 'p': [], 'sh': []}

        return anaData

    def traj2json(self,level):
        import json
        anaData = {i: [] for i in self.sid}
        prec = self.loadPrec()
        for year in range(1960,2017):
            print(year)
            for month in range(4,7):
                for day in range(self.days[month]):
                    for hour in ['02','14']:
                        # analyze Traj
                        dayData = self.read(year, month, day + 1, hour, level)
                        dayData = self.analyzeSH(dayData, -0.083)
                        # find prec
                        for i in range(len(self.sid)):
                            for j in prec[str(self.sid[i])]:
                                if j['y'] == year and j['m'] == month and j['n'] != []:
                                    if hour == '02' and j['n'][day] > 0:
                                        anaData[self.sid[i]].append({
                                            "y": year, "m": month, "d": day + 1, "h": "02",
                                            "prec": j['n'][day],
                                            "lon": dayData[str(i + 1)]['lon'],
                                            "lat": dayData[str(i + 1)]['lat'],
                                            "p": dayData[str(i + 1)]['p'],
                                            "sh": dayData[str(i + 1)]['sh'],
                                            "pathLon": dayData[str(i + 1)]['pathLon'],
                                            "pathLat": dayData[str(i + 1)]['pathLat'],
                                            "pathSH": dayData[str(i + 1)]['pathSH']})
                                    elif hour == '14' and j['d'][day] > 0:
                                        anaData[self.sid[i]].append({
                                            "y": year, "m": month, "d": day + 1, "h": "14",
                                            "prec": j['d'][day],
                                            "lon": dayData[str(i + 1)]['lon'],
                                            "lat": dayData[str(i + 1)]['lat'],
                                            "p": dayData[str(i + 1)]['p'],
                                            "sh": dayData[str(i + 1)]['sh'],
                                            "pathLon": dayData[str(i + 1)]['pathLon'],
                                            "pathLat": dayData[str(i + 1)]['pathLat'],
                                            "pathSH": dayData[str(i + 1)]['pathSH']})
            file = open("../vaporSources/"+str(level)+"/"+str(year)+".json","w+",encoding='utf-8')
            file.write(json.dumps(anaData))
            file.close()
        print("Finish!")

    def traj2txt(self,level):
        prec = self.loadPrec()
        for year in range(1960,2017):
            anaData = {i: [] for i in self.sid}
            print(year)
            for month in range(4,7):
                for day in range(self.days[month]):
                    for hour in ['02','14']:
                        # analyze Traj
                        dayData = self.read(year, month, day + 1, hour, level)
                        # find prec
                        for i in range(len(self.sid)):
                            for j in prec[str(self.sid[i])]:
                                if j['y'] == year and j['m'] == month and j['n'] != []:
                                    if hour == '02' and j['n'][day] > 0:
                                        anaData[self.sid[i]].append({
                                            "y": year, "m": month, "d": day + 1, "h": "02",
                                            "prec": j['n'][day],
                                            "lon": dayData[str(i + 1)]['lon'],
                                            "lat": dayData[str(i + 1)]['lat'],
                                            "sh": dayData[str(i + 1)]['sh']})
                                    elif hour == '14' and j['d'][day] > 0:
                                        anaData[self.sid[i]].append({
                                            "y": year, "m": month, "d": day + 1, "h": "14",
                                            "prec": j['d'][day],
                                            "lon": dayData[str(i + 1)]['lon'],
                                            "lat": dayData[str(i + 1)]['lat'],
                                            "sh": dayData[str(i + 1)]['sh']})
            text = ""
            for id in anaData:
                for i in anaData[id]:
                    text += str(id) + " " +str(i['y'])+" "+str(i["m"])+" "+str(i["d"])+" "+str(i["h"])+" "+str(i["prec"])
                    for j in i['lon']:
                        text += " " + str(j)
                    for j in i['lat']:
                        text += " " + str(j)
                    for j in i['sh']:
                        text += " " + str(j)
                    text += "\n"
            file = open("../Share data/Traj/"+str(level)+"_"+str(year)+".txt",'w+',encoding='utf-8')
            file.write(text)
            file.close()
        print("Finish!")

    def load_prec_traj(self,level,year):
        file = open("../Share data/Traj/"+str(level)+ "_" + str(year)+ ".txt",'r')
        lines = file.readlines()
        file.close()
        data = []
        for line in lines:
            l = line.split()
            d = {
                "sid":int(l[0]),
                "y":int(l[1]),
                "m":int(l[2]),
                "d":int(l[3]),
                "h":l[4],
                "p":int(l[5]),
                "lon":[float(i) for i in l[6:247]],
                "lat":[float(i) for i in l[247:488]],
                "q":[float(i) for i in l[488:729]]
            }
            data.append(d)
        return data

    def SPVAR(self,lat,lon):
        s = 0
        for i in range(len(lat)):
            s += (lat[i]-lat[0])**2+(lon[i]-lon[0])**2
        return s/len(lat)

    # 聚类
    def cluster(self,level,year,n=1,draw=False):
        data = self.load_prec_traj(level,year)[0:10]
        path = data.copy()
        NumberOfClusters = len(data)
        while True:
            TSV = sum([self.SPVAR(i['lat'], i['lon']) for i in data])
            TSVadd = 99999
            indexOfTraj = [0,0]
            for i in range(NumberOfClusters-1):
                for j in range(i+1,NumberOfClusters):
                    if i != j:
                        lat = np.mean([data[i]['lat'],data[j]['lat']],axis=0)
                        lon = np.mean([data[i]['lon'],data[j]['lon']],axis=0)
                        svadd = self.SPVAR(lat,lon)/TSV
                        if svadd < TSVadd:
                            TSVadd = svadd
                            indexOfTraj = [i,j]
            print(indexOfTraj)
            if TSVadd >= 0.5:
                break

            data.append({'lon':np.mean([data[indexOfTraj[0]]['lon'],data[indexOfTraj[1]]['lon']],axis=0),
                         'lat':np.mean([data[indexOfTraj[0]]['lat'],data[indexOfTraj[1]]['lat']],axis=0)})
            if indexOfTraj != [0,0] or indexOfTraj != [1,1]:
                data.pop(indexOfTraj[0])
                data.pop(indexOfTraj[1])
            else:
                data.pop(indexOfTraj[0])

            NumberOfClusters = len(data)
            if NumberOfClusters <= n:
                break

        if draw:
            import matplotlib.pyplot as plt
            from mpl_toolkits.basemap import Basemap

            plt.figure(figsize=(9, 7))
            plt.subplots_adjust(left=0.06, right=0.98, bottom=0.06, top=0.97)
            m = Basemap(llcrnrlat=-10, llcrnrlon=80, urcrnrlat=50, urcrnrlon=150, resolution='l')
            m.drawcoastlines(linewidth=0.4)
            m.drawparallels(np.arange(-10, 90, 10), labels=[1, 0, 0, 0])
            m.drawmeridians(np.arange(80, 180, 10), labels=[0, 0, 0, 1])

            for i in range(len(path)):
                plt.plot(path[i]['lon'], path[i]['lat'], color='k', alpha=0.2)
                plt.text(path[i]['lon'][-1],path[i]['lat'][-1],str(i))

            for i in data:
                plt.plot(i['lon'], i['lat'])
            plt.show()

        return data

    def path_distance(self,t1,t2):
        dis = 0
        for i in range(len(t1['lon'])):
            dis += ((t1['lon'][i]-t2['lon'][i])**2+(t1['lat'][i]-t2['lat'][i])**2)**0.5
        return dis

    def cluster2(self,level,year,n=1,draw=False):
        data = self.load_prec_traj(level,year)[0:100]
        path = data.copy()
        numberOfCluster = len(data)
        while True:
            trajDis = 99999
            indexOfTraj = [0,0]
            for i in range(numberOfCluster-1):
                for j in range(i+1,numberOfCluster):
                    d = self.path_distance(data[i],data[j])
                    if d < trajDis:
                        trajDis = d
                        indexOfTraj = [i,j]
            data.append({"lon":np.mean([data[i]['lon'],data[j]['lon']],axis=0),
                         "lat":np.mean([data[i]['lat'],data[j]['lat']],axis=0)})
            if indexOfTraj != [0,0] or indexOfTraj != [1,1]:
                data.pop(indexOfTraj[0])
                data.pop(indexOfTraj[1])
            else:
                data.pop(indexOfTraj[0])

            numberOfCluster = len(data)
            if numberOfCluster <= n:
                break

        if draw:
            import matplotlib.pyplot as plt
            from mpl_toolkits.basemap import Basemap

            plt.figure(figsize=(9, 7))
            plt.subplots_adjust(left=0.06, right=0.98, bottom=0.06, top=0.97)
            m = Basemap(llcrnrlat=-10, llcrnrlon=80, urcrnrlat=50, urcrnrlon=150, resolution='l')
            m.drawcoastlines(linewidth=0.4)
            m.drawparallels(np.arange(-10, 90, 10), labels=[1, 0, 0, 0])
            m.drawmeridians(np.arange(80, 180, 10), labels=[0, 0, 0, 1])

            for i in range(len(path)):
                plt.plot(path[i]['lon'], path[i]['lat'], color='k', alpha=0.2)
                plt.text(path[i]['lon'][-1],path[i]['lat'][-1],str(i))

            for i in data:
                plt.plot(i['lon'], i['lat'])
            plt.show()

        return data

    def load_traj2Cluster(self,year,month,day,hour,level):
        # convert BJT to UTC
        if hour == "02":
            hour = "18"
            if day > 1:
                day -= 1
            elif day == 1 and month == 4:
                month = 3;
                day = 31
            elif day == 1 and month == 5:
                month = 4;
                day = 30
            elif day == 1 and month == 6:
                month = 5;
                day = 31
        elif hour == "14":
            hour = "06"

        # Completing date
        if day < 10:
            day = "0" + str(day)
        else:
            day = str(day)

        # open file
        file = open("../traj/" + str(level) + "/1" + str(year)[2:4] + "0" + str(month) + day + hour, 'r',
                    encoding='utf-8')
        lines = file.readlines()
        file.close()

        # read lines
        data = {}
        mode = 0
        for line in lines:
            l = line.split()
            if mode:
                if l[0] not in data:
                    data[l[0]] = {"lat": [], "lon": [], "p": [], "sh": [],"h":[]}
                data[l[0]]['lat'].append(float(l[9]))
                data[l[0]]['lon'].append(float(l[10]))
                data[l[0]]['p'].append(float(l[12]))
                data[l[0]]['h'].append(float(l[11]))
                data[l[0]]['sh'].append(float(l[13]))
            if l[1] == "PRESSURE":
                mode = 1

        for i in data:
            d = data[i]
            text = '''12     1
CDC1    14     3     1     0     0
CDC1    14     4     1     0     0
CDC1    14     5     1     0     0
CDC1    14     6     1     0     0
CDC1    15     3     1     0     0
CDC1    15     4     1     0     0
CDC1    15     5     1     0     0
CDC1    15     6     1     0     0
CDC1    16     3     1     0     0
CDC1    16     4     1     0     0
CDC1    16     5     1     0     0
CDC1    16     6     1     0     0
 1 BACKWARD OMEGA
'''
            text += "11 1 1 1 "+str(d['lat'][0])+ " "+ str(d['lon'][0]) + " " + str(d['h'][0])+"\n2 PRESSURE SPCHUMID\n"
            hour = 0
            for j in range(len(d['lon'])):
                text += "1 1 11 1 1 1 0 0 "+str(round(hour,1))+" "+str(d['lat'][j])+ " "+ str(d['lon'][j]) + " " + str(d['h'][j]) + " " +str(d['p'][j]) + " " + str(d['sh'][j]) + "\n"
                hour -= 1
            file = open("../traj/test/k"+i,'w+',encoding='utf-8')
            file.write(text)
            file.close()

    def load_SCSM(self):
        file = open("../Share data/SCS_summer_monsoon.txt")
        lines = file.readlines()
        file.close()
        data = {}
        for line in lines:
            l = line.split()
            data[l[0]] = [int(l[1]),int(l[2])]
        return data

    def mapper(self, x, x1, x2, X1, X2):
        '''
        一维线性映射函数，返回在x1-x2中的x，映射到X1-X2后的值。
        :return: float
        '''
        return ((X2 - X1) * (x - x1) / (x2 - x1)) + X1

    def spacial_freq(self, lon0, lat0, minX, maxX, minY, maxY, xSpace, ySpace, value=None, grid=False):
        '''
        计算散点在空间格点上的频率分布(格点左闭右开)
        :param x: list, 散点的x坐标
        :param y: list, 散点的y坐标
        :param minX: 空间范围的x的最小值
        :param maxX: 空间范围的x的最大值
        :param minY: 空间范围的y的最小值
        :param maxY: 空间范围的y的最大值
        :param xSpace: 空间范围的统计格点的x宽度的间隔
        :param ySpace: 空间范围的统计个点的y宽度的间隔
        :param grid: 返回对应格点的坐标，return 为 result,x,y
        :param value: list, 统计频率散点的加权值
        :return: numpy.array, 空间格点的频数矩阵，从(minX,maxY)至(maxX,minY)(认知排序)
        '''
        import numpy as np
        # 创建格点场
        xLength = int((maxX - minX) / xSpace)
        yLength = int((maxY - minY) / ySpace)
        spcaialFreq = np.zeros((yLength, xLength))
        lon = np.arange(minX, maxX, xSpace) + xSpace / 2
        lat = np.arange(maxY, minY, -ySpace) - ySpace / 2

        for j in range(len(lon0)):
            x = lon0[j]
            y = lat0[j]
            if len(x) == len(y):
                for i in range(len(x)):
                    if minX <= x[i] < maxX and minY < y[i] <= maxY:
                        gridX = int(self.mapper(x[i], minX, maxX, 0, xLength))
                        gridY = int(self.mapper(y[i], minY, maxY, yLength, 0))
                        if value != None:
                            spcaialFreq[gridY][gridX] += value[j][i]
                        else:
                            spcaialFreq[gridY][gridX] += 1
            if grid:
                return spcaialFreq, lon, lat
            else:
                return spcaialFreq

    def spacial_freq2(self,lon,lat,minX,maxX,minY,maxY,space):
        if len(lon) != len(lat):
            raise Exception("lon & lat Length not same")
        xd = maxX - minX
        yd = maxY - minY
        n = int((maxX-minX)/space)
        m = int((maxY-minY)/space)
        freq = np.zeros((m,n))
        for i in range(len(lon)):
            if len(lon[i]) == len(lat[i]):
                for j in range(len(lon[i])):
                    x = lon[i][j]
                    y = lat[i][j]
                    if minX <= x < maxX and minY <= y < maxY:
                        freq[int((y-minY)*m/yd)][int((x-minX)*n/xd)] += 1
        return freq

    def cal_traj_freq(self,level):
        # run_Once 分别计算每年季风爆发前后的降水轨迹频率
        deg = 1
        scsm = self.load_SCSM()
        for year in range(1960,2017):
            print("Calculating:",year)
            before = [[],[]]
            after = [[],[]]
            data = self.load_prec_traj(level,year)

            for l in data:
                # 爆发前
                if l['m'] <= scsm[str(year)][0] and l['d'] < scsm[str(year)][1]:
                    before[0].append(l['lon'])
                    before[1].append(l['lat'])
                else:
                    after[0].append(l['lon'])
                    after[1].append(l['lat'])
            bfreq = self.spacial_freq(before[0],before[1],60,150,-10,50,deg,deg)
            afreq = self.spacial_freq(after[0],after[1],60,150,-10,50,deg,deg)
            np.save("../Share data/Traj_freq/"+str(level)+"_"+str(year)+"b.npy",bfreq)
            np.save("../Share data/Traj_freq/"+str(level)+"_"+str(year)+"a.npy",afreq)

    # 计算降水轨迹的频率分布(修复了时间判断的bug)
    def cal_traj_freq2(self,level,mode):
        deg=1
        f1 = []
        f2 = []
        scsm = self.load_SCSM()
        for year in range(1960,2017):
            print(year)
            lons1 = []
            lats1 = []
            lons2 = []
            lats2 = []
            data = self.load_prec_traj(level,year)

            scsmt = scsm[str(year)][0] * 100 + scsm[str(year)][1]

            for l in data:
                time = l['m'] * 100 + l['d']
                if time < scsmt:
                    lons1.append(l['lon'])
                    lats1.append(l['lat'])
                else:
                    lons2.append(l['lon'])
                    lats2.append(l['lat'])

            freq1 = self.spacial_freq2(lons1,lats1,50,160,-10,60,1)
            freq2 = self.spacial_freq2(lons2,lats2,50,160,-10,60,1)
            f1.append(freq1)
            f2.append(freq2)
        np.save("../Share data/Traj_freq/"+str(level)+"_b_"+str(deg)+".npy",np.array(f1))
        np.save("../Share data/Traj_freq/"+str(level)+"_a_"+str(deg)+".npy",np.array(f2))


    def draw_single_year(self,year,level):
        from matplotlib import pyplot as plt
        from mpl_toolkits.basemap import Basemap

        scsm = self.load_SCSM()

        data = self.load_prec_traj(level,year)
        lon = []
        lat = []
        for l in data:
            if l['m'] <= scsm[str(year)][0] and l['d'] < scsm[str(year)][1]:
                None
            else:
                lon.append(l['lon'])
                lat.append(l['lat'])

        plt.figure(figsize=(10,7))
        plt.subplots_adjust(left=0.06,right=0.98,bottom=0.07,top=0.95)
        m = Basemap(llcrnrlon=60,llcrnrlat=-10,urcrnrlon=150,urcrnrlat=50)
        m.drawmeridians(np.arange(60,155,10),labels=[0,0,0,1],linewidth=0.5,dashes=[1,6])
        m.drawparallels(np.arange(-10,55,10),labels=[1,0,0,0],linewidth=0.5,dashes=[1,6])
        m.drawcoastlines(linewidth=0.8)

        for i in range(len(lon)):
            plt.plot(lon[i],lat[i])

        plt.show()

    def draw_single_year_freq(self,year,level):
        from matplotlib import pyplot as plt
        from mpl_toolkits.basemap import Basemap
        data = np.zeros((70, 100))
        mode = "a"
        data = np.load("../Share data/Traj_freq/"+str(level)+"_"+str(year)+mode+".npy")

        data = data * 100 / np.sum(data)

        X, Y = np.meshgrid(np.arange(50, 150, 1), np.arange(-10, 60, 1))

        plt.figure(figsize=(10, 6))
        plt.subplots_adjust(left=0.06, right=1.02, bottom=0.07, top=0.95)
        m = Basemap(llcrnrlon=50, llcrnrlat=-10, urcrnrlon=150, urcrnrlat=60)
        m.drawmeridians(np.arange(60, 155, 10), labels=[0, 0, 0, 1], linewidth=0.5, dashes=[1, 6])
        m.drawparallels(np.arange(-10, 55, 10), labels=[1, 0, 0, 0], linewidth=0.5, dashes=[1, 6])
        m.drawcoastlines(linewidth=0.8)
        plt.contourf(X, Y, data, np.linspace(0.005, np.max(data), 16), cmap="Oranges")
        plt.colorbar(pad=0.02)
        plt.contour(X, Y, data, np.linspace(0.005, np.max(data), 16), colors='k', linewidths=0.3)
        plt.show()


    def draw_traj_freq(self):
        from matplotlib import pyplot as plt
        from mpl_toolkits.basemap import Basemap
        data = np.zeros((70,110))
        mode = "b"
        for level in ["1000","1500","3000"]:
            d = np.load("../Share data/Traj_freq/"+level+"_"+mode+".npy")
            for year in range(len(d)):
                data += d[year]

        data = data*100000/np.sum(data)

        X,Y = np.meshgrid(np.arange(50,160,1),np.arange(-10,60,1))

        plt.figure(figsize=(12,7))
        plt.subplots_adjust(left=0.03,right=1.05,bottom=0.04,top=0.94)
        m = Basemap(llcrnrlon=50,llcrnrlat=-10,urcrnrlon=160,urcrnrlat=60)
        m.drawmeridians(np.arange(50,165,10),labels=[0,0,0,1],linewidth=0.5,dashes=[1,6])
        m.drawparallels(np.arange(-10,65,10),labels=[1,0,0,0],linewidth=0.5,dashes=[1,6])
        m.drawcoastlines(linewidth=0.8)
        plt.contourf(X,Y,data,np.linspace(1,np.max(data),16),cmap="Oranges")
        plt.colorbar(pad=0.02,ticks=np.linspace(1,np.max(data),16),label="($1\ /\ 10^5$)")
        plt.contour(X,Y,data,np.linspace(1,np.max(data),16),colors='k',linewidths=0.3)
        plt.title("Frequency of Precipitation Backward Trajectory Points (240h, at 1000m, 1500m & 3000m)\n before South China Sea Monsoon Onset during 1960-2016")
        plt.show()

    def draw_enso_traj_freq(self):
        from matplotlib import pyplot as plt
        from mpl_toolkits.basemap import Basemap
        edata = np.zeros((70, 110))
        ldata = np.zeros((70, 110))
        ndata = np.zeros((70, 110))
        mode = "a"
        time = "n"
        ept = self.epMonth
        cpt = self.cpMonth
        coldt = self.coldMonth

        for level in ["1000", "1500", "3000"]:
            d = np.load("../Share data/Traj_freq/" + level + "_" + mode + ".npy")
            for year in range(len(d)):
                y = year + 1960
                if y in ept:
                    if 4 in ept[y] and 5 in ept[y] and 6 in ept[y]:
                        edata += d[year]
                elif y in cpt:
                    if  4 in cpt[y] and 5 in cpt[y] and 6 in cpt[y]:
                        edata += d[year]
                elif y in coldt:
                    if 4 in coldt[y] and 5 in coldt[y] and 6 in coldt[y]:
                        ldata += d[year]
                else:
                    ndata += d[year]

        edata = edata * 100000 / np.sum(edata)
        ldata = ldata * 100000 / np.sum(ldata)
        ndata = ndata * 100000 / np.sum(ndata)

        if time == "e":
            data = edata
            name = "Frequency of Precipitation Backward Trajectory Points (240h, at 1000m, 1500m & 3000m)\n before South China Sea Monsoon Onset during 1960-2016 El Niño Event in Apr-Jun"
        elif time == "l":
            data = ldata
            name = "Frequency of Precipitation Backward Trajectory Points (240h, at 1000m, 1500m & 3000m)\n before South China Sea Monsoon Onset during 1960-2016 La Niña Event in Apr-Jun"
        else:
            data = ndata
            name = "Frequency of Precipitation Backward Trajectory Points (240h, at 1000m, 1500m & 3000m)\n before South China Sea Monsoon Onset during 1960-2016 in Apr-Jun"

        X, Y = np.meshgrid(np.arange(50, 160, 1), np.arange(-10, 60, 1))
        plt.figure(figsize=(12, 7))
        plt.subplots_adjust(left=0.03, right=1.05, bottom=0.04, top=0.94)
        m = Basemap(llcrnrlon=50, llcrnrlat=-10, urcrnrlon=160, urcrnrlat=60)
        m.drawmeridians(np.arange(50, 165, 10), labels=[0, 0, 0, 1], linewidth=0.5, dashes=[1, 6])
        m.drawparallels(np.arange(-10, 65, 10), labels=[1, 0, 0, 0], linewidth=0.5, dashes=[1, 6])
        m.drawcoastlines(linewidth=0.8)
        plt.contourf(X, Y, data, np.linspace(1, 300, 16), cmap="Oranges")
        plt.colorbar(pad=0.02, ticks=np.linspace(1, 300, 16), label="($1\ /\ 10^5$)")
        plt.contour(X, Y, data, np.linspace(1, 300, 16), colors='k', linewidths=0.3)
        plt.title(name)
        plt.show()

if __name__ == "__main__":
    v = Vapo()
    #d = v.cluster2(1000,1960,n=4,draw=True)
    #path = v.load_prec_traj(1000,1960)[0:10]
    #print(len(d))
    #v.cal_traj_freq(1500)
    v.draw_enso_traj_freq()
    #v.draw_single_year(1960,1000)
    #v.draw_single_year_freq(1960,1000)
    '''
    for i in [1000,1500,3000]:
        for m in ["a","b"]:
            print(i,m)
            v.cal_traj_freq2(i,m)
    '''