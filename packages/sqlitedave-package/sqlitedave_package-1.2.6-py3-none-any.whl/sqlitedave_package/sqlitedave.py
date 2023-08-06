"""
  Dave Skura
  
  File Description:
"""

import os
import sys
from datetime import *
import time
import sqlite3
from garbledave_package.garbledave import garbledave 

def splitTupleandGroup(k, inputTuple):
		args = [iter(inputTuple)] * k
		return zip(*args)

def main():
	print('usage: ')
	print('py -m sqlitedave_package.sqlitedave') 
	print('-- ')
	print('py -m sqlitedave_package.query [query or filename] ') 
	print('-- ')
	print('py -m sqlitedave_package.execute [query or filename] ') 
	print('-- ')

	mydb = sqlite_db()
	mydb.connect()
	print(mydb.dbstr())
	mydb.load_csv_to_table('postgres_data.tsv','tablec',True,'~')

	#print(mydb.export_query_to_str('SELECT CURRENT_DATE as d1,CURRENT_DATE as d2'))

	#csvfilename = 'Station.tsv'
	#tblname = 'Station'
	
	#mydb.load_csv_to_table('a.csv','tablea',True,',')
	#mydb.export_table_to_csv(csvfilename,tblname)

class disconnected_cursor:
	def __init__(self,datacursor):
		self.data = []
		inputTuple = ()
		for k in (i[0] for i in datacursor.description):
			col = (k,None,None,None,None,None,None)
			inputTuple += col

		self.description = tuple(splitTupleandGroup(7, inputTuple))
		self.rowcount = 0
		self.colcount = 0
		for row in datacursor:
			self.data.append(row)
			self.rowcount += 1
			self.colcount = len(row)

	def __iter__(self):
		self.iteration_nbr = 0
		return self

	def __next__(self):
		if self.iteration_nbr >= self.rowcount:
			raise StopIteration
		else:
			thisrow = self.data[self.iteration_nbr]
			self.iteration_nbr += 1
			return thisrow


class dbconnection_details: 
	def __init__(self,DB_NAME=''): 
		self.DatabaseType='SQLite' 
		self.updated='Mar 23/2023' 

		self.settings_loaded_from_file = False

		self.DB_NAME=DB_NAME
		if DB_NAME == '':
			self.loadSettingsFromFile()

	def loadSettingsFromFile(self):
		try:
			f = open('.schemawiz_config3','r')
			connectionstrlines = f.read()
			connectionstr = garbledave().ungarbleit(connectionstrlines.splitlines()[0])
			f.close()
			connarr = connectionstr.split(' - ')

			self.DB_NAME			= connarr[0]

			self.settings_loaded_from_file = True

		except:
			#saved connection details not found. using defaults
			self.DB_NAME='' 

	def dbconnectionstr(self):
		return 'Database=' + self.DB_NAME + ';'

	def saveConnectionDefaults(self,DB_NAME=''):

		f = open('.schemawiz_config3','w')
		f.write(garbledave().garbleit(DB_NAME + ' - ' ))
		f.close()

		self.loadSettingsFromFile()

class tfield:
	def __init__(self):
		self.table_name = ''
		self.column_name = ''
		self.data_type = ''
		self.Need_Quotes = ''
		self.ordinal_position = -1
		self.comment = '' # dateformat in csv [%Y/%m/%d]

class sqlite_db:
	def __init__(self,DB_NAME=''):
		self.enable_logging = False
		self.max_loglines = 500
		self.db_conn_dets = dbconnection_details(DB_NAME)
		self.dbconn = None
		self.cur = None

	def getbetween(self,srch_str,chr_strt,chr_end,srch_position=0):
		foundit = 0
		string_of_interest = ''
		for i in range(srch_position,len(srch_str)):
			if (srch_str[i] == chr_strt ):
				foundit += 1

			if (srch_str[i] == chr_end ):
				foundit -= 1
			if (len(string_of_interest) > 0 and (foundit == 0)):
				break
			if (foundit > 0):
				string_of_interest += srch_str[i]
			
		return string_of_interest[1:]

	def getfielddefs(self,tablename):
		tablefields = []
		#)cid	name	type	notnull	dflt_value	pk
		sql = "pragma table_info('" + tablename + "')"

		data = self.query(sql)
		for row in data:
			fld = tfield()
			fld.table_name = tablename
			fld.ordinal_position = row[0]
			fld.column_name = row[1]
			fld.data_type = row[2]
			if (fld.data_type.lower() == 'text' or fld.data_type.lower() == 'blob'):
				fld.Need_Quotes = 'QUOTE'
			else:
				fld.Need_Quotes = 'NO QUOTE'

			tablefields.append(fld)

		return tablefields

	def dbstr(self):
		return 'Database=' + self.db_conn_dets.DB_NAME + '; version ' + self.dbversion()

	def dbversion(self):
		return self.queryone('select sqlite_version();')

	def clean_column_name(self,col_name):

		new_column_name = col_name
		chardict = self.count_chars(col_name)
		alphacount = self.count_alpha(chardict)
		nbrcount = self.count_nbr(chardict)
		if ((len(col_name)-2) == (alphacount + nbrcount)) and '1234567890'.find(col_name[:1]) == -1:
			new_column_name = self.clean_text(col_name) # .replace('"','').strip()

		return new_column_name

	def clean_text(self,ptext): # remove optional double quotes
		text = ptext.strip()
		if (text[:1] == '"' and text[-1:] == '"'):
			return text[1:-1]
		else:
			return text

	def count_chars(self,data,exceptchars=''):
		chars_in_hdr = {}
		for i in range(0,len(data)):
			if data[i] != '\n' and exceptchars.find(data[i]) == -1:
				if data[i] in chars_in_hdr:
					chars_in_hdr[data[i]] += 1
				else:
					chars_in_hdr[data[i]] = 1
		return chars_in_hdr

	def count_alpha(self,alphadict):
		count = 0
		for ch in alphadict:
			if 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.find(ch) > -1:
				count += alphadict[ch]
		return count

	def count_nbr(self,alphadict):
		count = 0
		for ch in alphadict:
			if '0123456789'.find(ch) > -1:
				count += alphadict[ch]
		return count

	def logquery(self,logline,duration=0.0):
		if self.enable_logging:
			startat = (datetime.now())
			startdy = str(startat.year) + '-' + ('0' + str(startat.month))[-2:] + '-' + str(startat.day)
			starttm = str(startat.hour) + ':' + ('0' + str(startat.minute))[-2:] + ':' + ('0' + str(startat.second))[-2:]
			start_dtm = startdy + ' ' + starttm
			preline = start_dtm + '\nduration=' + str(duration) + '\n'

			log_contents=''
			try:
				f = open('.querylog','r')
				log_contents = f.read()
				f.close()
			except:
				pass

			logs = log_contents.splitlines()
			
			logs.insert(0,preline + logline + '\n ------------ ')
			f = open('.querylog','w+')
			numlines = 0
			for line in logs:
				numlines += 1
				f.write(line + '\n')
				if numlines > self.max_loglines:
					break

			f.close()


	def saveConnectionDefaults(self,DB_NAME):
		self.db_conn_dets.saveConnectionDefaults(DB_NAME)

	def useConnectionDetails(self,DB_NAME):

		self.db_conn_dets.DB_NAME = DB_NAME					
		self.connect()

	def is_an_int(self,prm):
			try:
				if int(prm) == int(prm):
					return True
				else:
					return False
			except:
					return False

	def export_query_to_str(self,qry,szdelimiter=','):
		data = self.query(qry)
		f = ''
		sz = ''
		for k in [i[0] for i in data.description]:
			sz += k + szdelimiter
		f += sz[:-1] + '\n'

		for row in data:
			sz = ''
			for i in range(0,len(data.description)):
				sz += str(row[i])+ szdelimiter

			f += sz[:-1] + '\n'

		return f

	def export_query_to_csv(self,qry,csv_filename,szdelimiter=','):
		data = self.query(qry)
		#print(data.description)
		#sys.exit(0)
		f = open(csv_filename,'w')
		sz = ''
		for k in [i[0] for i in data.description]:
			sz += k + szdelimiter
		f.write(sz[:-1] + '\n')

		for row in data:
			sz = ''
			for i in range(0,len(data.description)):
				sz += str(row[i])+ szdelimiter

			f.write(sz[:-1] + '\n')
				

	def export_table_to_csv(self,csvfile,tblname,szdelimiter=','):
		if not self.does_table_exist(tblname):
			raise Exception('Table does not exist.  Create table first')

		self.export_query_to_csv('SELECT * FROM ' + tblname,csvfile,szdelimiter)

	def load_csv_to_table(self,csvfile,tblname,withtruncate=True,szdelimiter=',',fields='',withextrafields={}):
		table_fields = self.getfielddefs(tblname)

		if not self.does_table_exist(tblname):
			raise Exception('Table does not exist.  Create table first')

		if withtruncate:
			self.execute('DELETE FROM ' + tblname)

		f = open(csvfile,'r')
		lines = f.readlines()

		hdrs = lines[0].split(szdelimiter)
		f.close()		

		isqlhdr = 'INSERT INTO ' + tblname + '('

		if fields != '':
			isqlhdr += fields	+ ') VALUES '	
		else:
			for i in range(0,len(hdrs)):
				isqlhdr += self.clean_column_name(hdrs[i]) + ','
			isqlhdr = isqlhdr[:-1] + ') VALUES '

		skiprow1 = 0
		batchcount = 0
		ilines = ''

		with open(csvfile) as myfile:
			for line in myfile:
				if line.strip()!='':
					if skiprow1 == 0:
						skiprow1 = 1
					else:
						batchcount += 1
						row = line.rstrip("\n").split(szdelimiter)
						newline = "("
						for var in withextrafields:
							newline += "'" + withextrafields[var]  + "',"

						for j in range(0,len(row)):

							if row[j].lower() == 'none' or row[j].lower() == 'null':
								newline += "NULL,"
							else:
								if table_fields[j].data_type.strip().lower() == 'date':
									dt_fmt = self.getbetween(table_fields[j].comment,'[',']')
									if dt_fmt.strip() != '':
										newline += "str_to_date('" + self.clean_text(row[j]) + "','" + dt_fmt + "'),"
									else:
										newline += "'" + self.clean_text(row[j]) + "',"

								elif table_fields[j].data_type.strip().lower() == 'timestamp':
									dt_fmt = self.getbetween(table_fields[j].comment,'[',']')
									if dt_fmt.strip() != '':
										newline += "str_to_date('" + self.clean_text(row[j]) + "','" + dt_fmt + "'),"
									else:
										newline += "'" + self.clean_text(row[j]) + "',"

								elif table_fields[j].Need_Quotes == 'QUOTE':
									newline += "'" + self.clean_text(row[j]).replace(',','').replace("'",'').replace('"','') + "',"
								else:
									val = self.clean_text(row[j]).replace(',','').replace("'",'').replace('"','')
									if val == '':
										newline += "NULL,"
									else:
										newline += val + ","

							
						ilines += newline[:-1] + '),'
						
						if batchcount > 500:
							qry = isqlhdr + ilines[:-1]
							#print(qry)
							#sys.exit()
							batchcount = 0
							ilines = ''
							self.execute(qry)

		if batchcount > 0:
			qry = isqlhdr + ilines[:-1]
			batchcount = 0
			ilines = ''
			print(qry)
			self.execute(qry)

	def does_table_exist(self,tblname):
		self.connect()

		sql = """
		SELECT count(*)
		FROM sqlite_master AS m
		WHERE lower(m.name) = lower('""" + tblname + "')"
		
		if self.queryone(sql) == 0:
			return False
		else:
			return True

	def close(self):
		if self.dbconn:
			self.dbconn.close()

	def ask_for_database_details(self):
		self.db_conn_dets.DB_NAME = input('DB_NAME (local_sqlite_db): ') or 'local_sqlite_db'

	def chk_conn(self):
		try:
			self.dbconn.cursor()
			return True
		except Exception as ex:
			return False

	def connect(self):
		connects_entered = False

		if self.db_conn_dets.DB_NAME == '':
			self.ask_for_database_details()
			connects_entered = True

		try:

			if not self.chk_conn():
				self.dbconn = sqlite3.connect(self.db_conn_dets.DB_NAME)

				if connects_entered:
					user_response_to_save = input('Save this connection locally? (y/n) :')
					# only if successful connect after user prompted and got Y do we save pwd
					if user_response_to_save.upper()[:1] == 'Y':
						self.saveConnectionDefaults(self.db_conn_dets.DB_NAME)

		except Exception as e:
			if self.db_conn_dets.settings_loaded_from_file:
				os.remove('.schemawiz_config3')

			raise Exception(str(e))

	def query(self,qry):
		if not self.chk_conn():
			self.connect()

		all_rows_of_data = disconnected_cursor(self.dbconn.execute(qry))
		self.close()
		return all_rows_of_data

	def commit(self):
		if self.chk_conn():
			self.dbconn.commit()

	def execute(self,qry):
		try:
			begin_at = time.time() * 1000
			if not self.chk_conn():
				self.connect()
			
			self.dbconn.execute(qry)
			self.commit()
			self.close()
			end_at = time.time() * 1000
			duration = end_at - begin_at
			self.logquery(qry,duration)
		except Exception as e:
			raise Exception("SQL ERROR:\n\n" + str(e))

	def queryone(self,select_one_fld):
		try:
			data = self.query(select_one_fld)
			for row in data:
				return row[0]

		except Exception as e:
			raise Exception("SQL ERROR:\n\n" + str(e))

if __name__ == '__main__':
	
	main()

