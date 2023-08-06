# SQLiteDave - A wrapper for simplified sqlite usage using sqlite3.

## usage - load_csv_to_table
'''
	mydb = sqlite_db()
	mydb.connect()
	print(mydb.queryone('SELECT CURRENT_DATE'))
	mydb.close()

'''

## usage - load_csv_to_table
'''
	mydb = sqlite_db()
	mydb.connect()
	print(mydb.dbstr())
	csvfilename = 'Station.tsv'
	tblname = 'Station'	
	mydb.load_csv_to_table(csvfilename,tblname,True,'\t')
	mydb.close()
'''

## usage - export_table_to_csv
'''
	mydb = sqlite_db()
	mydb.connect()
	print(mydb.dbstr())
	csvfilename = 'Station.tsv'
	tblname = 'Station'
	mydb.export_table_to_csv(csvfilename,tblname)
	mydb.close()

'''