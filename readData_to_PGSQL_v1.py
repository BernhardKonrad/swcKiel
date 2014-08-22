# In this file we will read the data and plot
# oxygen level vs depth

import sys
import psycopg2 as pgsql
import pandas.io.sql as sql



mydb = pgsql.connect(database="survey", user="rkiko", password="rkiko")

cur = mydb.cursor()



cur.execute("""CREATE TABLE IF NOT EXISTS ctd_data
(Indx TEXT PRIMARY KEY,
Profile text,
Depth FLOAT8,
Oxygen_conc	 FLOAT8
)
""", mydb)

mydb.commit()


filename = sys.argv[1]

f_input = open(filename, 'r')

doneWithHeader = False
depthList = []
oxList = []

for line in f_input:
    if doneWithHeader == False:
        if "Profile" in line:
            profile = line.strip().split("=")[1]
            profile = int(profile)
        elif "Latitude" in line: 
            lat = line.strip().split("=")[1]
            lat = float(lat)
        elif "Longitude" in line: 
            lng = line.strip().split("=")[1]
            lng = float(lng)
        elif "Columns" in line:
            # order of columns is consistent
            doneWithHeader = True
            continue
    if doneWithHeader == True:
        # read and save the data
        dataList = line.split()
        depth = -float(dataList[1])
        ox = float(dataList[5])
        depthList.append(depth)
        oxList.append(ox)
        ###index not yet perfect
        indx = "'" + str(profile) + "_" + str(depth) + "'"
        print indx, profile, depth, ox
        cur.execute("""INSERT INTO ctd_data(indx, profile, depth, oxygen_conc) 
                     VALUES (%s, %s, %s, %s)"""
                     %(indx, profile, depth, ox), mydb)


mydb.commit()


df = sql.read_frame("""select profile, avg(oxygen_conc) as avg_ox 
                       from ctd_data
                       group by profile
                        """,  mydb)


f_input.close()    

#import matplotlib.pyplot as plt
#plt.plot(oxList, depthList)
#plt.title('oxygen level at different depths')
#plt.show()
print sum(oxList) / len(oxList)


cur.close()
mydb.close()