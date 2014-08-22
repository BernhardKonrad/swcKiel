# In this file we will read the data and plot
# oxygen level vs depth

import sys

filename = sys.argv[1]

f_input = open(filename, 'r')

doneWithHeader = False
depthList = []
oxList = []

for line in f_input:
    if doneWithHeader:
        # read and save the data
        dataList = line.split()
        depth = -float(dataList[1])
        ox = float(dataList[5])
        depthList.append(depth)
        oxList.append(ox)

    else:
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

f_input.close()    

#import matplotlib.pyplot as plt
#plt.plot(oxList, depthList)
#plt.title('oxygen level at different depths')
#plt.show()
print sum(oxList) / len(oxList)