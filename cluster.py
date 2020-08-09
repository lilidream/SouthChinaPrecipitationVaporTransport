import numpy as np
class cluster():

    def read(self, year, month, day, hour):
        '''
        Input BJT of datafile and only support for 0200 & 1400,
        function will convert to 1800Z & 0600Z.
        '''
        # convert BJT to UTC
        if hour == "02":
            hour = "18"
            if day > 1:
                day -= 1
            elif day == 1 and month == 4:
                month = 3
                day = 31
            elif day == 1 and month == 5:
                month = 4
                day = 30
            elif day == 1 and month == 6:
                month = 5
                day = 31
        elif hour == "14":
            hour = "06"

        # Completing date
        if day < 10:
            day = "0" + str(day)
        else:
            day = str(day)

        # open file
        file = open("../traj/1500/1" + str(year)[2:4] + "0" + str(month) + day + hour, 'r', encoding='utf-8')
        lines = file.readlines()
        file.close()

        # read lines
        data = {}
        mode = 0
        for line in lines:
            l = line.split()
            if mode:
                if l[0] not in data:
                    data[l[0]] = {"lat": [], "lon": [],"h":[], "p": [], "sh": []}
                data[l[0]]['lat'].append(float(l[9]))
                data[l[0]]['lon'].append(float(l[10]))
                data[l[0]]['h'].append(float(l[11]))
                data[l[0]]['p'].append(float(l[12]))
                data[l[0]]['sh'].append(float(l[13]))
            if l[1] == "PRESSURE":
                mode = 1
        d = []
        for i in data:
            d.append(data[i])
        return d

    def sv(self,d1,d2):
        # d1 = {"lon":[],"lat":[],"h":[]}...
        sv = 0
        if len(d1['lon']) == len(d2['lon']):
            for i in range(len(d1['lon'])):
                sv += (d1['lon'][i]-d2['lon'][i])**2 + (d1['lat'][i]-d2['lat'][i])**2 + (d1['h'][i]-d2['h'][i])**2
            return sv
        else:
            raise Exception("Different length of two path when computing SV")

    def cluster1(self,data,n=1):
        import numpy as np
        '''
        聚类
        :param data: list [{"lon":[...],"lat":[...],"h":[...]},...]
        :return:
        '''
        numberOfTraj = len(data)
        numberOfCluster = len(data)

        # 生成轨迹变量
        t = {}
        for i in range(numberOfTraj):
            ddata = data[i]
            t[i] = {"lon":ddata['lon'],"lat":ddata['lat'],"h":ddata['h']}

        # 生成簇变量
        c = []
        for i in t:
            c.append({"lon":t[i]['lon'],"lat":t[i]['lat'],"h":t[i]['h'],"t":[i]})


        while True:
            CSV = 99999999999
            cgroup = [0,0]
            newC = []
            TSV = 0

            for i in range(numberOfCluster - 1):
                for j in range(i + 1, numberOfCluster):
                    # 计算两个簇的平均路径
                    cmean = {"lon":np.mean([c[i]['lon'],c[j]['lon']],axis=0),
                             "lat":np.mean([c[i]['lat'],c[j]['lat']],axis=0),
                             "h":np.mean([c[i]['h'],c[j]['h']],axis=0)}
                    cTraj = np.hstack([c[i]['t'],c[j]['t']]) # 合并两个簇的轨迹编号数组

                    # 计算簇空间方差csv
                    csv = 0
                    for k in cTraj:
                        csv += self.sv(t[k],cmean)
                    TSV += csv

                    # 比较最小的簇空间方差
                    if csv < CSV:
                        CSV = csv
                        cgroup = [i,j]
                        newC = cmean

            # 更新簇
            newClusterTraj = np.hstack([c[cgroup[0]]['t'],c[cgroup[1]]['t']])
            c[cgroup[0]] = newC
            c[cgroup[0]]['t'] = newClusterTraj
            del c[cgroup[1]]

            TSV += CSV

            numberOfCluster = len(c)
            print(numberOfCluster,round(CSV/TSV,4))

            if numberOfCluster == n:
                break
        return c

    def dis(self,x1,y1,x2,y2):
        a = np.array([x1,y1])
        b = np.array([x2,y2])
        c = np.linalg.inv(np.cov([a,b]))
        d = (a-b)*c*(a-b).T

        return np.sqrt(d)

    def distance(self,a,b):
        # 输入两个轨迹，计算两个轨迹的相似距离
        lon = np.hstack([a['lon'],b['lon']])
        lat = np.hstack([a['lat'],b['lat']])
        hgt = np.hstack([a['h'],b['h']])
        cov = np.linalg.inv(np.cov([lon,lat,hgt]))
        ma = []
        for i in range(len(a['lon'])):
            mi = []
            for j in range(len(b['lon'])):
                vd = np.array([a['lon'][i]-b['lon'][i],a['lat'][i]-b['lat'][j],a['h'][i]-b['h'][j]])
                mi.append(np.dot(np.dot(vd,cov),vd)**0.5)
            ma.append(min(mi))
        Dab = max(ma)
        ma = []
        for i in range(len(b['lon'])):
            mi = []
            for j in range(len(a['lon'])):
                vd = np.array([b['lon'][i]-a['lon'][i],b['lat'][i]-a['lat'][j],b['h'][i]-a['h'][j]])
                mi.append(np.dot(np.dot(vd,cov),vd)**0.5)
            ma.append(min(mi))
        Dba = max(ma)
        d = min(Dba,Dab)

        return d

    def center_dis(self,lon1,lat1,lon2,lat2):
        import numpy as np
        return ((np.mean(lon1)-np.mean(lon2))**2+(np.mean(lat1)-np.mean(lat2))**2)**0.5

    def cluster2(self,data,n=3,sigma=10):
        import random
        numberOfTraj = len(data)
        cluster = []

        # 随机选择n个聚类中心，将轨迹序号添加到cluster
        for i in range(n):
            if cluster == []:
                cluster.append(random.randint(0,numberOfTraj))
            else:
                while True:
                    m = 0
                    r = random.randint(0,numberOfTraj-n-1)
                    for j in cluster:
                        d = self.center_dis(data[r]['lon'],data[r]['lat'],data[j]['lon'],data[j]['lat'])
                        if d <= sigma:
                            m = 1
                            break
                    if m == 0:
                        cluster.append(r)
                        break


        newCluster = []

        while True:
            # 轨迹分类
            c = [[] for i in range(n)]  # 创建聚类集合
            for i in range(numberOfTraj):
                if i not in cluster:
                    dis = []
                    for j in range(n):
                        print("fenlei",cluster,i,j)
                        dis.append(self.distance(data[i],data[cluster[j]]))
                    cindex = dis.index(min(dis))
                    c[cindex].append(i)
            for i in range(n):
                c[i].append(cluster[i])

            # 重新寻找轨迹中心
            newCluster = []
            for i in c:
                dInClass = []
                for j in i:
                    dsum = 0
                    for k in i:
                        if j != k:
                            print("xunzhao", newCluster, j, k)
                            dsum += self.distance(data[j],data[k])
                    dInClass.append(dsum)
                newCluster.append(i[dInClass.index(min(dInClass))])

            # 判断
            assess = 0
            for i in range(n):
                if newCluster[i] in cluster:
                    assess += 1
            if assess == n:
                break
            else:
                cluster = newCluster
        return newCluster,c

    def drawCluster(self,data):
        import matplotlib.pyplot as plt
        from mpl_toolkits.basemap import Basemap
        import numpy as np

        c = self.cluster1(data,n=3)

        plt.figure(figsize=(12,8))
        plt.subplots_adjust(left=0.05,right=0.98,top=0.98,bottom=0.05)
        m = Basemap(llcrnrlat=-30,llcrnrlon=30,urcrnrlat=60,urcrnrlon=160)
        m.drawcoastlines()
        m.drawparallels(np.arange(-10,70,10),labels=[1,0,0,0])
        m.drawmeridians(np.arange(30,170,10),labels=[0,0,0,1])

        for i in range(len(data)):
            plt.plot(data[i]['lon'],data[i]['lat'],c="k",alpha=0.2)

        for i in range(len(c)):
            plt.plot(c[i]['lon'],c[i]['lat'])
        plt.show()

    def drawCluster2(self,data):
        import matplotlib.pyplot as plt
        from mpl_toolkits.basemap import Basemap
        import numpy as np

        cluster,c = self.cluster2(data, n=3)

        plt.figure(figsize=(12, 8))
        plt.subplots_adjust(left=0.05, right=0.98, top=0.98, bottom=0.05)
        m = Basemap(llcrnrlat=-30, llcrnrlon=30, urcrnrlat=60, urcrnrlon=160)
        m.drawcoastlines()
        m.drawparallels(np.arange(-10, 70, 10), labels=[1, 0, 0, 0])
        m.drawmeridians(np.arange(30, 170, 10), labels=[0, 0, 0, 1])

        for i in range(len(data)):
            plt.plot(data[i]['lon'], data[i]['lat'], c="k", alpha=0.2)

        for i in cluster:
            plt.plot(data[i]['lon'],data[i]['lat'])
        plt.show()

    # 输出HYSPLI轨迹文件
    def export_HYSPLIT(self,data,name):
        for i in range(len(data)):
            text = ''' 10     1
CDC1    89     3     1     0     0
CDC1    89     4     1     0     0
CDC1    89     5     1     0     0
CDC1    89     6     1     0     0
CDC1    93     5     1     0     0
CDC1    93     6     1     0     0
CDC1     4     5     1     0     0
CDC1     4     6     1     0     0
CDC1     5     5     1     0     0
CDC1     5     6     1     0     0
 1 BACKWARD OMEGA\n'''
            text += "11 1 1 1 "+str(data[0]['lat'][0]) + " " + str(data[0]['lon'][0]) + " " + str(data[0]['h'][0])+ "\n0\n"
            t = 0
            for j in range(len(data[i]['lon'])):
                text += "1 1 11 1 1 1 0 0 "+str(t)+" "+str(data[i]['lat'][j]) + " " + str(data[i]['lon'][j]) + " " + str(data[i]['h'][j])+"\n"
                t -= 1

            file = open("../traj/test/"+name+str(i),"w+",encoding='utf-8')
            file.write(text)
            file.close()

    def load_single_traj(self,name):
        import os
        files = os.listdir("../traj/test")
        filenames = []
        for i in files:
            if i[0:len(name)] == name:
                filenames.append(i)
        d = []
        for file in filenames:
            f = open("../traj/test/"+file)
            lines = f.readlines()
            f.close()
            m = 0
            data = {"lon":[],"lat":[],"h":[]}
            for line in lines:
                l = line.split()
                if m == 1:
                    data['lat'].append(float(l[9]))
                    data['lon'].append(float(l[10]))
                    data['h'].append(float(l[11]))

                if l[1] == "PRESSURE":
                    m = 1
            d.append(data)
        return d

if __name__ == "__main__":
    obj = cluster()
    data = []
    #for i in range(1,21):
        #for j in ['02',"14"]:
            #d = obj.read(1987,4,i,j)[0]
            #data.append(d)
    data = obj.load_single_traj("tta")[:10]
    #obj.cluster1(data)
    #obj.drawCluster(data)
    #obj.export_HYSPLIT(data,"ca")
    #obj.cluster2(data)
    obj.drawCluster2(data)
