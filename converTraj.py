def read(year, month, day, hour, level):
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
    file = open("../traj/" + str(level) + "/1" + str(year)[2:4] + "0" + str(month) + day + hour, 'r', encoding='utf-8')
    lines = file.readlines()
    file.close()

    # read lines
    data = {}
    mode = 0
    for line in lines:
        l = line.split()
        if mode:
            if l[0] not in data:
                data[l[0]] = []
            data[l[0]].append(l)
        if l[1] == "PRESSURE":
            mode = 1
    return data

def fm(i,text):
    if len(text) <= i:
        return " "*(i-len(text))+text
    else:
        raise Exception("len of format")

def out_text(d):
    text = "     2     1\n"
    text += "    CDC1    50     3     1     0     0\n"
    text += "    CDC1    50     4     1     0     0\n"
    text += "     1 BACKWARD OMEGA\n"
    text += fm(6,d[0][2])+fm(6,d[0][3])+fm(6,d[0][4])+fm(6,d[0][5])+fm(9,d[0][9])+fm(9,d[0][10])+fm(8,d[0][11])+"\n"
    text += "     2 PRESSURE SPCHUMID\n"
    for i in range(len(d)):
        text += '     1     1'
        for j in range(2,8):
            text += fm(6,d[i][j])
        text += fm(8,d[i][8]) + fm(9,d[i][9]) + fm(9,d[i][10]) + fm(9,d[i][11]) + fm(8,d[i][12]) + fm(8,d[i][13]) + "\n"
    return text

def export_file(year,month,day,hour):
    data = []
    l = ["1000","1500","3000"]
    for level in [1000,1500,3000]:
        data.append(read(year,month,day,hour,level))

    for d in range(3):
        for i in data[d]:
            text = out_text(data[d][i])
            file = open("../traj/single/a"+str(year)+"_"+str(month)+"_"+str(day)+"_"+str(hour)+"_"+str(i)+"_"+l[d],"w+",encoding="ascii")
            file.write(text)
            file.close()

if __name__ ==  '__main__':
    export_file(1987,4,5,"02")