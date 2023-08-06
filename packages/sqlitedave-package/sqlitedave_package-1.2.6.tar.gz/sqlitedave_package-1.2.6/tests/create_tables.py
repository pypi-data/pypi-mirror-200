"""
  Dave Skura
  
  File Description:
"""
import sqlite3

print (" create table Station,Calendar,Postal_Code_Segments ") # 
DB_NAME = 'local_sqlite_db'
dbconn = sqlite3.connect(DB_NAME)
sql = """
DROP TABLE IF EXISTS  Station;
"""
dbconn.execute(sql)

sql = """
CREATE TABLE Station (
	stationid	integer,
	stationname	text,
	province	text,
	latitude	real,
	longitude	real,
	start_dt	text,
	end_dt text
);
"""
dbconn.execute(sql)

sql = """
DROP TABLE IF EXISTS Calendar;
"""
dbconn.execute(sql)

sql = """
CREATE TABLE Calendar (
	year	integer,
	month	integer,
	day	integer,
	caldt text
);
"""

dbconn.execute(sql)

sql = """
DROP TABLE IF EXISTS Postal_Code_Segments;
"""
dbconn.execute(sql)

sql = """
CREATE TABLE Postal_Code_Segments (
	province	text,
	postalcode	text,
	fsa	text,
	latitude	real,
	longitude	real,
	rnk	integer,
	segment integer
);
"""

dbconn.execute(sql)

sql = """
CREATE INDEX Postal_Code_Segmentsidx ON Postal_Code_Segments(segment);
"""

dbconn.execute(sql)

dbconn.close()