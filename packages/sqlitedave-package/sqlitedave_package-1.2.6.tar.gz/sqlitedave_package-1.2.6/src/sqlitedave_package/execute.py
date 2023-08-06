"""
  Dave Skura
  
  File Description:
"""
import sys
from sqlitedave import sqlite_db

def main():
	mydb = sqlite_db()
	if len(sys.argv) == 1 or sys.argv[1] == 'execute.py': # no parameters
		print('')
		print('usage: ')
		print('py -m sqlitedave_package.execute [query] ') 
		print('-----------')
		mydb.connect()
		print(mydb.dbstr())
		mydb.close()

	else: 
		mydb.connect()
		print(mydb.dbstr())
		parameter = sys.argv[1]
		if check_isafile(parameter):
			#print('is a file')
			f = open(parameter,'r')
			query = f.read()
			f.close()
		else:
			#print('is not a file')
			query = parameter
		
		print(query)
		print('------ ------ ------\n')
		
		try:
			data = mydb.execute(query)
			print('Success')
		except Exception as e:
			print(str(e))
			
		mydb.close()
		
	sys.exit(0)

def check_isafile(possible_filename):
	try:
		f =open(possible_filename,'r')
		f.close()
		return True
	except:
		return False

if __name__ == '__main__':
	main()
