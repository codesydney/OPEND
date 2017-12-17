#########################################################################################################
#   Program Name : NSWBirthRateDatabasePrep.py                                                          #
#   Program Description:                                                                                #
#   This program prepares a SQLite table containing data about birth rates in NSW.                      #
#                                                                                                       #
#   Comment                                         Date                  Author                        #
#   ================================                ==========            ================              #
#   Initial Version                                 25/10/2017            Engramar Bollas               #
#   Prepared a blog                                 28/10/2017            Engramar Bollas   		#
#   testing new branch commit 			    30/10/2017	          Gerald Mills  	        #
#   testing new branch commit                       09/11/2017            about.me/kashif.islam         #
#########################################################################################################
import sqlite3
import sys

#######################################################################
### Create NSW_BIRTH_RATE Table                                     ### 
#######################################################################
conn = sqlite3.connect('NSW_POPULATION.sqlite')
cur = conn.cursor()

cur.executescript('''	
DROP TABLE IF EXISTS NSW_POPULATION;

CREATE TABLE NSW_POPULATION (
	YEAR              number(4),            
	CODE              varchar(10),
	SUBURB            varchar(100),  
	STATE             char(3), 
	POSTCODE          number(4),
	POPULATION        number(10)
);

''')

fname = 'NSWPopulation_001.csv'
fhand = open(fname)

#######################################################################
### Populate NSW_POPULATION Table                                   ### 
#######################################################################
for line in fhand:	
	fields = line.split(',')

	YEAR = '2011' 
	CODE = fields[0].strip()  
	SUBURB = fields[1].strip() 
	STATE = fields[9].strip() 
	POSTCODE = '' 
	POPULATION = fields[2].strip() 
	

	cur.execute('''INSERT INTO NSW_POPULATION
        (
		YEAR,
		CODE,
		SUBURB,
		STATE,
		POSTCODE,
		POPULATION
        )  
        VALUES ( ?, ?, ?, ?, ?, ?)''',   
		(
		YEAR,
		CODE,
		SUBURB,
		STATE,
		POSTCODE,
		POPULATION
		))
				
conn.commit()

print ('Done')
