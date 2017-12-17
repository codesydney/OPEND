#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('NSW_POPULATION.sqlite')

print ("Opened database successfully")
conn.row_factory = sqlite3.Row
details_cur = conn.execute('select YEAR, CODE, SUBURB, STATE, POSTCODE, POPULATION from NSW_POPULATION')
details = details_cur.fetchall()
for detail in details:
    print (detail['YEAR'],detail['CODE'],detail['SUBURB'],detail['STATE'],detail['POSTCODE'],detail['POPULATION']);
    
