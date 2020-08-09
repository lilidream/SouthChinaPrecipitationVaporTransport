import numpy as np
def t2orderSST(year,month):
    return (year-1891)*12+month-1

def calIOD():
    from netCDF4 import Dataset
    a = Dataset("../data/sst.mon.mean.nc")
    w = a.variables['sst'][:,80:100,50:70]
    e = a.variables['sst'][:,90:100,90:110]

    data = []

    wbg = [[],[],[]]
    ebg = [[],[],[]]

    for year in range(1960,2017):
        wbg[0].append(w[t2orderSST(year,9)])
        wbg[1].append(w[t2orderSST(year,10)])
        wbg[2].append(w[t2orderSST(year,11)])
        ebg[0].append(e[t2orderSST(year,9)])
        ebg[1].append(e[t2orderSST(year,10)])
        ebg[2].append(e[t2orderSST(year,11)])

    for i in range(3):
        wbg[i] = np.mean(wbg[i],axis=0)
        ebg[i] = np.mean(ebg[i],axis=0)

    for year in range(1960,2017):
        wmean = 0
        for month in [9,10,11]:
            wmean += np.mean(w[t2orderSST(year,month)]-wbg[month-9])
        wmean = wmean/3
        emean = 0
        for month in [9,10,11]:
            emean += np.mean(e[t2orderSST(year,month)]-ebg[month-9])
        emean = emean/3

        dmi = round(wmean-emean,3)
        data.append(dmi)

    std = np.std(data)*0.5

    p = []
    n = []
    for i in range(len(data)):
        if data[i] > std:
            p.append(i+1960)
        elif data[i] < -std:
            n.append(i+1960)

    '''
    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(np.arange(1960,2017,1),data)
    plt.hlines(0,1960,2016)
    plt.hlines(std,1960,2016)
    plt.hlines(-std,1960,2016)
    plt.show()
    '''

    return p,n

def calenso():
    file = open("../data/ONI.TXT")
    lines = file.readlines()
    file.close()

    data = {}

    for line in lines:
        l = line.split()
        if int(l[0]) not in data and 1960 <= int(l[0]) <= 2016:
            data[int(l[0])] = []
        if int(l[0]) in data:
            data[int(l[0])].append(float(l[4]))

    d1 = []
    d2 = []
    sprp = []
    sprn = []
    sump = []
    sumn = []

    p = []
    n = []

    for i in data:
        for j in range(10):
            if data[i][j] > 0.5:
                if data[i][j+1] > 0.5 and data[i][j+2] > 0.5:
                    p.append(i)
                    break
            elif data[i][j] < -0.5:
                if data[i][j+1] < -0.5 and data[i][j+2] < -0.5:
                    n.append(i)
                    break

    '''
    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(np.arange(1960, 2017, 1), d)
    plt.hlines(0, 1960, 2016)
    plt.hlines(0.5, 1960, 2016)
    plt.hlines(-0.5, 1960, 2016)

    plt.show()
    '''



    return p,n

if __name__ == "__main__":
    p1,n1 = calIOD()
    p2,n2 = calenso()

    pp = []
    pn = []
    np = []
    nn = []

    for i in p1:
        if i in p2:
            pp.append(i)
        if i in n2:
            pn.append(i)
    for i in n1:
        if i in p2:
            np.append(i)
        if i in n2:
            nn.append(i)

    print("IOD ENSO")
    print(" +    + ",pp)
    print(" +    - ",pn)
    print(" -    + ",np)
    print(" -    - ",nn)
