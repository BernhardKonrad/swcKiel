# In this file we will read the data and plot
# oxygen level vs depth


import psycopg2 as pgsql
import pandas.io.sql as sql



mydb = pgsql.connect(database="survey", user="rkiko", password="rkiko")

cur = mydb.cursor()




df = sql.read_sql("""select profile, avg(oxygen_conc) as avg_ox 
                       from ctd_data
                       group by profile
                       ORDER BY profile
                        """,  mydb)
print df


cur.close()
mydb.close()