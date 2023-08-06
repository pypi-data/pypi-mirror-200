"""
  Dave Skura
  
  File Description:
"""
import sqlite3

print (" open local_sqlite_db ") # 
DB_NAME = 'local_sqlite_db'
dbconn = sqlite3.connect(DB_NAME)
print (" run SQL ") # 

sql = "SELECT * FROM Station"
cursor = dbconn.execute(sql)

for row in cursor:
	print(row)

dbconn.close()