"""
  Dave Skura
  
  File Description:
"""
import sqlite3

print (" create tesla table ") # 
DB_NAME = 'local_sqlite_db'
dbconn = sqlite3.connect(DB_NAME)
sql = """
CREATE TABLE tesla (
	date text,
	close real,
	volume integer,
	open real,
	high real,
	low real
);
"""
dbconn.execute(sql)

dbconn.close()