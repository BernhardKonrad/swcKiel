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



### use show_plot = 0 and safe_plot = 1 if you want to use the code in a for-loop in the shell, then you get a plot of each profile
### you can add code to both show and safe the plot, but I would not recommend to do so

import matplotlib.pyplot as plt

show_plot = 0
safe_plot = 1


plt.plot(oxList, depthList)
plt.title('oxygen level at different depths')

if show_plot == 1 and safe_plot == 0:
    plt.show()
elif show_plot == 0 and safe_plot == 1:
    fig_name = filename.replace(".ctd",".pdf") #you could also add .jpg to create a jpg, but pdf's are to be prefferred for scientific publications, as these are vectorgrafics
    plt.savefig(fig_name)
    print fig_name + " plotted."
else:
    print "Better safe the plot if you are using a for - loop in the shell ..."   

