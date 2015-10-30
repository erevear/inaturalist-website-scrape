import json
import urllib2
import requests
import codecs
import MySQLdb

i = 0
j = 0;




#print len(data)


db = MySQLdb.connect("localhost","root","password" )


cursor = db.cursor()

#set encoding to include any utf8 character
cursor.execute("SET NAMES utf8mb4;") 

cursor.execute("SET CHARACTER SET utf8mb4;")

cursor.execute("SET character_set_connection=utf8mb4;")

#set database to iNat_Observations
cursor.execute('USE iNat_Observations')

#if the table already exists, drop it and create new one with given fields
cursor.execute('DROP TABLE IF EXISTS OBSERVATIONS')
create_table = """CREATE TABLE IF NOT EXISTS OBSERVATIONS (
         SPECIES  CHAR(200) NOT NULL,
         OBSERVER CHAR(200) NOT NULL,
         DATE CHAR(200) NULL,
         LOCATION CHAR(200) NULL)"""

cursor.execute(create_table)




#also write to cvs
file = codecs.open("inat2.csv", "wb", "utf-8")
file.write( "Species,Observer,Date,Location,,\n");

#for all first 100 pages take in the species, observer username, date and location
#write all to a database and a file and print to console
while j < 100:
	url = 'http://inaturalist.org/observations.json?page=%d'%j
	print url
	r = requests.get(url)
	response = urllib2.urlopen(url)
	data = json.load(response)
	
	print len(data)
	while i < len(data):
		location = 'NA'
    		print "Species: %s"  %data[i]['species_guess']
    		species=data[i]['species_guess']
		
		file.write("%s" %species)
    		
    		print "Observer user name: %s " %data[i]['user']['login']
		observer=data[i]['user']['login']
		
		file.write(",%s" %observer)
    		print "Date: %s" %data[i]['observed_on_string'] 
		date= data[i]['observed_on_string'] 
		
		file.write(",%s" %date)
    		if 'place_guess' in data[i]:
        		print "Location: %s" %data[i]['place_guess']
			location = data[i]['place_guess']
			file.write(",%s" %location)
		
		
		file.write(",,\n")
		insert_observation = "INSERT INTO OBSERVATIONS(SPECIES, \
       		OBSERVER, DATE, LOCATION) \
       		VALUES ('%s', '%s','%s', '%s' )" % \
       		(species, observer, date, location)
		try:		
			cursor.execute(insert_observation)
		except:
			db.rollback()

		db.commit()

		
    		i = i + 1
	i = 0
	j=j+1



file.close()
db.close()




#Several SQL statements to find the most frequently occurring:
#Species: SELECT SPECIES FROM OBSERVATIONS GROUP BY SPECIES ORDER BY COUNT(*) DESC LIMIT #1;
 
#Observer: SELECT OBSERVER FROM OBSERVATIONS GROUP BY OBSERVER ORDER BY COUNT(*) DESC #LIMIT 1;

#Location:SELECT LOCATION FROM OBSERVATIONS GROUP BY LOCATION ORDER BY COUNT(*) DESC LIMIT #1;

#Date: SELECT DATE FROM OBSERVATIONS GROUP BY DATE ORDER BY COUNT(*) DESC LIMIT 1;
#in the data