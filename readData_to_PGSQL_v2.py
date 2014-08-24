"""
In this file we will read the data and load it into pgsql
Version 2 improved by R.Kiko in order to contain a proper indx (cruise, ctd, pressure) and to read in further data (lat, long, date, time, ctd_filenam).
Depth is in m, Pressure in dbar
Date and Time data types are DATE and TIME (use these, pgsql is date and time aware)
-9.99 is the badvalue indicator, it is replaced with NULL to allow input into sql as missing data
This code could be improved by defining the Primary key not as a special column termed indx,
but by defining it at the end of the table definition as PRIMARY KEY (Cruise, Profile, Pressure) that is made up of three columns.

The appropriate code would be:

CREATE TABLE IF NOT EXISTS ctd_data
(Cruise TEXT,
CTD_filename TEXT,
Latitude FLOAT8,
Longitude FLOAT8,
Date DATE,
Time Time,
Profile text,
Pressure FLOAT8,
Depth FLOAT8,
Salinity  FLOAT8,
Oxygen_conc	 FLOAT8,
PRIMARY KEY (Cruise, Profile, Pressure))

Then the you need to delete the indx input in the for loop (Delete indx, %s and indx).


"""


import sys
import psycopg2 as pgsql
import pandas.io.sql as sql



mydb = pgsql.connect(database="survey", user="rkiko", password="rkiko")

cur = mydb.cursor()


#use below line, if you want to develop the code further in order to recreate the table each time the script is run
cur.execute("""DROP TABLE IF EXISTS ctd_data""", mydb) 



cur.execute("""CREATE TABLE IF NOT EXISTS ctd_data
(Indx TEXT PRIMARY KEY,
Cruise TEXT,
CTD_filename TEXT,
Latitude FLOAT8,
Longitude FLOAT8,
Date DATE,
Time Time,
Profile text,
Pressure FLOAT8,
Depth FLOAT8,
Salinity  FLOAT8,
Oxygen_conc	 FLOAT8
)
""", mydb)

mydb.commit()


filename = sys.argv[1]

f_input = open(filename, 'r')


###using info from the filename to generate a filename that it is useful for input into sql (getting rid of .ctd)
filename_to_pgsql = "'" + filename.split(".")[0] + "'"

###using info from the filename to generate a cruise abbreviation useful for input
cruise = "'" + "M" + str(filename.split("_")[1]) + "'"

doneWithHeader = False
depthList = []
oxList = []

for line in f_input:
    if doneWithHeader == False: ###added further elif's here to catch date and time
        if "Profile" in line:
            profile = line.strip().split("=")[1]
            profile = profile.strip() #getting rid of the space
            profile = str(profile).zfill(3) #using zfill to generate a profile index with 3 digits, it fills zeros into the string
            profile = "'" + profile + "'"
        elif "Latitude" in line: 
            lat = line.strip().split("=")[1]
            lat = float(lat)
        elif "Longitude" in line: 
            lng = line.strip().split("=")[1]
            lng = float(lng)
        elif "Date" in line: 
            date = line.strip().split("=")[1]
            date = date.replace("/","") #replacing / with nothing to get the proper input format for pgsql
            date = "'" + date + "'" #adding single ' at start and end to allow insert into pgsql
        elif "Time" in line: 
            time = line.strip().split("=")[1]
            time = time.replace(":","")
            time = "'" + time + "'"
        elif "Columns" in line:
            # order of columns is consistent
            doneWithHeader = True
            continue
    if doneWithHeader == True:
        # read and save the data
        line = line.replace("-9.99","NULL")
        dataList = line.split()
        pressure = dataList[1] #column 2 is now defined as pressure, not depth, pressure is taken for the primary indx
        depth = dataList[2] #deleted the - again, as depth is normally reported this way, changed depth to column 3 and pressure to column 2
        ox = dataList[5] #removed the conversion to float, as this will be done by sql anyhow. It would not work with the NULL (which is a string) that -9.99 was changed to before
        sal = dataList[4]
        ###index not yet perfect
        indx = cruise + "_" + str(profile) + "_" + str(int(float(pressure)))
        indx = indx.replace("'", "")  #need to get rid of the ' that were added to cruise and profile before
        indx = "'" + indx + "'" #need to add ' at the ends of the string
        cur.execute("""INSERT INTO ctd_data(indx, cruise, profile, ctd_filename, latitude, longitude, date, time, pressure, depth, salinity, oxygen_conc) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                     %(indx, cruise, profile, filename_to_pgsql, lat, lng, date, time, pressure, depth, sal, ox), mydb)


mydb.commit()



f_input.close()    


cur.close()
mydb.close()


print "Profile input to pgsql:    " + filename_to_pgsql