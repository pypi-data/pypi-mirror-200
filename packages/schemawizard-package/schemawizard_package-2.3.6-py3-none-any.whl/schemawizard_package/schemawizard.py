"""
  Dave Skura, 2023
"""
import datetime 
import os
import sys
from sqlitedave_package.sqlitedave import sqlite_db
from postgresdave_package.postgresdave import postgres_db 
from mysqldave_package.mysqldave import mysql_db 
from garbledave_package.garbledave import garbledave 

def main():
	obj = schemawiz()
	#obj.loadcsvfile('sample7.csv')
	#print(obj.guess_mysql_ddl('restored_sample177'))
	
	#tbl = obj.createload_mysql_from_csv('sample7.csv','restored_sample')

"""	
	csvfilename = 'a.csv'
	ddl = obj.guess_postgres_ddl(csvfilename.replace('.','_'))
	print(ddl)
	print('/* Tablename used : ' + obj.lastcall_tablename + ' */ \n')
	print('/* Postgres DDL - END   ----- ----- ----- ----- */ \n')
	
	print(obj.dbthings.postgres_db.does_table_exist('newtbl'))

	# add any specific known date formats
	#obj.dbthings.postgres_date_formats.append('Mon DD,YY')
	if csvfilename != '':
		obj.loadcsvfile(csvfilename)

	print('/* MySQL DDL - BEGIN ----- schemawiz().guess_mysql_ddl() ----- */ \n')
	print(obj.guess_mysql_ddl('sample_csv'))
	print('/* MySQL DDL - END   ----- ----- ----- ----- */ \n')


	print('/* Postgres DDL - BEGIN ----- schemawiz().guess_postgres_ddl() ----- */ \n')
	ddl = obj.guess_postgres_ddl(csvfilename.replace('.','_'))
	print('/* Tablename used : ' + obj.lastcall_tablename + ' */ \n')
	print(ddl)
	print('/* Postgres DDL - END   ----- ----- ----- ----- */ \n')



	print('/* BigQuery DDL - BEGIN ----- schemawiz().guess_BigQuery_ddl() ----- */ \n')
	print(obj.guess_BigQuery_ddl('watchful-lotus-364517','dave'))
	print('\n/* BigQuery DDL - END   ----- ----- ----- ----- */ \n')


	
	print('/* BigQuery External DDL - BEGIN ----- schemawiz().guess_BigQueryExternal_ddl() ----- */ \n')
	print(obj.guess_BigQueryExternal_ddl('watchful-lotus-364517','dave'))
	print('\n/* BigQuery External DDL - END   ----- ----- ----- ----- */ \n')

	print('/* BigQuery DDL - BEGIN ----- schemawiz().guess_BigQuery_ddl() ----- */ \n')
	print(obj.guess_BigQuery_ddl('watchful-lotus-364517','dave'))
	print('\n/* BigQuery DDL - END   ----- ----- ----- ----- */ \n')


	"""

class database_type:
	Postgres = 1
	MySQL = 2
	sqlite = 3
	BigQuery = 4


class dbthinger:
	def __init__(self,date_to_check=''):
		self.sqlite_db = sqlite_db()
		self.mysql_db = mysql_db()
		self.postgres_db = postgres_db()
		self.postgres_date_formats = ['YYYY/MM/DD','YYYY-MM-DD','YYYY-Mon-DD','MM/DD/YYYY','Mon-DD-YYYY','Mon-DD-YY','Month DD,YY','Month DD,YYYY','DD-Mon-YYYY','YY-Mon-DD','YYYYMMDD','YYMMDD','YYYY-DD-MM','Mon dd/YY']
		self.postgres_timestamp_formats = ['YYYY-MM-DD HH:MI:SS']

		self.mysql_date_formats = ['%b %d/%y','%m/%d/%Y','%Y/%m/%d']
		self.mysql_timestamp_formats = ['%Y/%m/%d %H:%i:%s','%d/%m/%Y %T']

		self.date_to_check = date_to_check 
		if date_to_check != '':
			self.chk_date(date_to_check)

	def ask_for_database_details(self,thisDatabaseType):
		configfilename = '.schemawiz_config' + str(thisDatabaseType)

		if thisDatabaseType == database_type.Postgres:
			DB_NAME = input('DB_NAME (postgres): ') or 'postgres'
		elif thisDatabaseType == database_type.MySQL:
			DB_NAME = input('DB_NAME : ') or 'atlas'
		elif thisDatabaseType == database_type.sqlite:
			DB_NAME = input('DB_NAME : (local_sqlite_db)') or 'local_sqlite_db'

		DB_HOST = ''
		if (thisDatabaseType == database_type.Postgres) or (thisDatabaseType == database_type.MySQL):
			DB_HOST = input('DB_HOST (localhost): ') or 'localhost'

		DB_PORT = ''
		if thisDatabaseType == database_type.Postgres:
			DB_PORT = input('DB_PORT (1532): ') or '1532'
		elif thisDatabaseType == database_type.MySQL:
			DB_PORT = input('DB_PORT (3306): ') or '3306'

		if thisDatabaseType == database_type.Postgres:
			DB_USERNAME = input('DB_USERNAME (postgres): ') or 'postgres'
		elif thisDatabaseType == database_type.MySQL:
			DB_USERNAME = input('DB_USERNAME: ') or 'dave'

		DB_SCHEMA = ''
		if thisDatabaseType == database_type.Postgres:
			DB_SCHEMA = input('DB_SCHEMA (public): ') or 'public'

		if thisDatabaseType == database_type.Postgres:
			DB_USERPWD = input('DB_USERPWD: ') or '4165605869'
		elif thisDatabaseType == database_type.MySQL:
			DB_USERPWD = input('DB_USERPWD: ') or 'dave'

		if thisDatabaseType == database_type.Postgres:
			self.postgres_db.useConnectionDetails(DB_USERNAME,DB_USERPWD,DB_HOST,DB_PORT,DB_NAME,DB_SCHEMA)
		elif thisDatabaseType == database_type.MySQL:
			self.mysql_db.useConnectionDetails(DB_USERNAME,DB_USERPWD,DB_HOST,DB_PORT,DB_NAME)
		elif thisDatabaseType == database_type.sqlite:
			self.sqlite_db.useConnectionDetails(DB_NAME)

		ans_save_connection_details = input('Save connection details? (y/n) :') or 'y'
		if ans_save_connection_details.upper() == 'Y':
			f = open(configfilename,'w')

			if thisDatabaseType == database_type.Postgres:
				f.write(garbledave().garbleit(DB_USERNAME + ' - ' + DB_USERPWD + ' - ' + DB_HOST + ' - ' + DB_PORT + ' - ' + DB_NAME + ' - ' + DB_SCHEMA))
			elif thisDatabaseType == database_type.MySQL:
				f.write(garbledave().garbleit(DB_USERNAME + ' - ' + DB_USERPWD + ' - ' + DB_HOST + ' - ' + DB_PORT + ' - ' + DB_NAME))
			elif thisDatabaseType == database_type.sqlite:
				f.write(garbledave().garbleit(DB_NAME + ' - '))

			f.close()

	def connect_local_db(self,thisDatabaseType):
		configfilename = '.schemawiz_config' + str(thisDatabaseType)
		if (((thisDatabaseType == database_type.sqlite) and (not self.sqlite_db.dbconn)) or (thisDatabaseType == database_type.Postgres) and (not self.postgres_db.dbconn))	or ((thisDatabaseType == database_type.MySQL) and (not self.mysql_db.dbconn)):
			try:
				f = open(configfilename,'r')
				config_line = garbledave().ungarbleit(f.readline())
				dbsettings = config_line.split(' - ')
				f.close()

				if thisDatabaseType == database_type.sqlite:
					DB_NAME = dbsettings[0]
					self.sqlite_db.useConnectionDetails(DB_NAME)

				else:
					DB_USERNAME = dbsettings[0]
					DB_USERPWD = dbsettings[1]
					DB_HOST = dbsettings[2]
					DB_PORT = dbsettings[3]
					DB_NAME = dbsettings[4]

					if thisDatabaseType == database_type.Postgres:
						DB_SCHEMA = dbsettings[5]
						self.postgres_db.useConnectionDetails(DB_USERNAME,DB_USERPWD,DB_HOST,DB_PORT,DB_NAME,DB_SCHEMA)
					elif thisDatabaseType == database_type.MySQL:
						self.mysql_db.useConnectionDetails(DB_USERNAME,DB_USERPWD,DB_HOST,DB_PORT,DB_NAME)

			except Exception as e:
				self.ask_for_database_details(thisDatabaseType)
		
	def chk_date(self,possible_date_str):
		print (" Checking date " + possible_date_str) # 
		self.date_type = self.match_date_type(possible_date_str)

		if self.date_type == -1:
			print('Not a date. date_type = ' + str(self.date_type))
		else:
			print('Is a date, and matchs date_type ' + str(self.date_type) + ', ' + self.postgres_date_formats[self.date_type])

		return self.date_type

	def chk_date_format_old(self,date_string,date_format):
		try:
			dateObject = datetime.datetime.strptime(date_string, date_format)
			return True
		except ValueError:
			return False

	def is_an_int(self,prm):
			try:
				if int(prm) == int(prm):
					return True
				else:
					return False
			except:
					return False

	def is_a_float(self,prm):
			try:
				if float(prm) == float(prm):
					return True
				else:
					return False
			except:
					return False

	def match_timestamp_type(self,timestamp_string,thisdatabase_type):	
		if thisdatabase_type == database_type.Postgres:
			for i in range(0,len(self.postgres_timestamp_formats)):
				fmt = self.postgres_timestamp_formats[i]
				if self.chk_postrgres_timestamp_format(timestamp_string,fmt):
					return i
				else:
					return -1
		elif thisdatabase_type == database_type.MySQL:
			for i in range(0,len(self.mysql_timestamp_formats)):
				fmt = self.mysql_timestamp_formats[i]
				if self.chk_mysql_timestamp_format(timestamp_string,fmt):
					return i
				else:
					return -1

	def chk_mysql_timestamp_format(self,timestamp_string,date_format):
		retval = False
		if len(timestamp_string) > 12:
			sql = "SELECT CASE WHEN STR_TO_DATE('" + timestamp_string + "','" + date_format + "') is not null THEN 'Good' ELSE 'Bad' END as date_reasonablness"
			try:
				#print(sql)
				#sys.exit(0)
				if self.mysql_db.queryone(sql) == 'Good':
					retval = True
			except:
				retval = False

		return retval


	def chk_postrgres_timestamp_format(self,timestamp_string,date_format):
		retval = False
		if len(timestamp_string) > 12:
			sql = "SELECT to_char('" + timestamp_string + "'::timestamp,'" + date_format + "')"
			try:
				#print(sql)
				return_fmt = self.postgres_db.queryone(sql)
				retval = True
			except Exception as e:
				retval = False

		return retval

	# -1 means no matching date format
	# > -1 means the date format matches self.postgres_date_formats[return_value]
	def match_date_type(self,date_string,thisdatabase_type):	
		
		fmtdict = {}
		dateformatscore = {}
		bestchoice = -1
		bestfmt = -1
		besthits = -1

		# might be a date
		if (((self.is_an_int(date_string) and len(date_string) == 8)) or ((not self.is_an_int(date_string)) and (len(date_string) > 5) and (len(date_string) < 12))): 
				# loadup with default date formats

			if thisdatabase_type == database_type.Postgres:
				for i in range(0,len(self.postgres_date_formats)):
					dateformatscore[self.postgres_date_formats[i]] = 0
					fmtdict[self.postgres_date_formats[i]] = i

			elif thisdatabase_type == database_type.MySQL:
				for i in range(0,len(self.mysql_date_formats)):
					dateformatscore[self.mysql_date_formats[i]] = 0
					fmtdict[self.mysql_date_formats[i]] = i
			
			for i in range(0,len(dateformatscore)):
				retval = False
				if thisdatabase_type == database_type.Postgres:
					retval = self.chk_postgres_date_format(date_string,self.postgres_date_formats[i])
					if retval:
						dateformatscore[self.postgres_date_formats[i]] += 1
				elif thisdatabase_type == database_type.MySQL:
					retval = self.chk_mysql_date_format(date_string,self.mysql_date_formats[i])
					if retval:
						dateformatscore[self.mysql_date_formats[i]] += 1

			for fmt in dateformatscore:
				if dateformatscore[fmt] > bestchoice:
					bestchoice = dateformatscore[fmt]
					bestfmt = fmt
		
		if bestchoice > 0:
			return fmtdict[bestfmt]
		else:
			return -1

	def match_float_type(self,floatvalue):
		return self.is_a_float(floatvalue)

	def match_integer_type(self,intvalue):
		return self.is_an_int(intvalue)

	def chk_mysql_date_format(self,date_string,date_format):
		
		sql = """

			SELECT CASE WHEN STR_TO_DATE('""" + date_string + """','""" + date_format + """') is null THEN 'bad'
			ELSE 'Good'
			END as date_reasonablness

		"""
		try:
			#print(sql)
			#sys.exit(0)
			return_fmt = self.mysql_db.queryone(sql)
			if return_fmt == 'Good':
				return True
			else:
				return False

		except Exception as e:
			return False

	def chk_postgres_date_format(self,date_string,date_format):
		
		sql = """

			SELECT CASE WHEN abs( to_date('""" + date_string + """','""" + date_format + """') - current_date) > 36500 THEN 'bad'
			ELSE 'Good'
			END as date_reasonablness

		"""
		try:

			return_fmt = self.postgres_db.queryone(sql)

			if return_fmt == 'Good':
				return True
			else:
				return False

		except Exception as e:
			return False
		
class schemawiz:	
	def __init__(self,csvfilename=''):
		self.version=2.0
		self.dbthings = dbthinger()
		self.force_delimiter = ''
		self.lastcall_tablename = ''
		self.delimiter = ''
		self.logging_on = False
		self.SomeFileContents = []
		self.column_names = []
		self.column_datatypes = []
		self.BigQuery_datatypes = []
		self.mysql_datatypes = []
		self.sqlite_datatypes = []
		self.column_sample = []
		self.column_dateformats = []
		self.analyzed	 = False
		self.IsaDateField = False
		self.DateField = ''
		self.clusterField1 = ''
		self.clusterField2 = ''
		self.clusterField3 = ''

		self.csvfilename = ''
		if csvfilename != '':
			self.loadcsvfile(csvfilename)
	
	def newpostgresconnection(self):
		os.remove('.schemawiz_config' + str(database_type.Postgres))

	def newmysqlconnection(self):
		os.remove('.schemawiz_config' + str(database_type.MySQL))

	def newsqliteconnection(self):
		os.remove('.schemawiz_config' + str(database_type.sqlite))

	def newconnections(self):
		self.newpostgresconnection()
		self.newmysqlconnection()
		self.newsqliteconnection()

	def justload_sqlite_from_csv(self,csvfilename,tablename,withtruncate=False):
		return_value = ''
		self.loadcsvfile(csvfilename)
		delimiter = self.lastcall_delimiter()

		if self.dbthings.sqlite_db.does_table_exist(tablename):
			self.dbthings.sqlite_db.load_csv_to_table(csvfilename,tablename,withtruncate,delimiter)
			rowcount = self.dbthings.sqlite_db.queryone('SELECT COUNT(*) FROM ' + tablename)
			print('Loaded table ' + tablename + ' with ' + str(rowcount) + ' rows.')
			return_value = tablename
		else:
			print('Table ' + tablename + ' does not exist.  Cannot load. \n alternatively try: createload_postgres_from_csv(csvfilename)')

		return return_value

	def createload_sqlite_from_csv(self,csvfilename,sztablename='',ddlfilename=''):
		return_value = ''

		self.loadcsvfile(csvfilename)
		ddl = self.guess_sqlite_ddl(sztablename)
		delimiter = self.lastcall_delimiter()
		if sztablename == '':
			tablename = self.lastcall_tablename
		else:
			tablename = sztablename

		if not self.dbthings.sqlite_db.does_table_exist(tablename):
			if ddlfilename != '':
				f = open(ddlfilename,'w')
				f.write(ddl)
				f.close()

			print(ddl)
			self.dbthings.sqlite_db.execute(ddl)

			self.dbthings.sqlite_db.load_csv_to_table(csvfilename,tablename,True,delimiter)

			rowcount = self.dbthings.sqlite_db.queryone('SELECT COUNT(*) FROM ' + tablename)
			print('Created/Loaded table ' + tablename + ' with ' + str(rowcount) + ' rows.')
			return_value = tablename
		else:
			print('Table ' + tablename + ' already exists.  Stopping Load.')

		return return_value

	def justload_postgres_from_csv(self,csvfilename,tablename,withtruncate=False):
		return_value = ''
		self.loadcsvfile(csvfilename)
		delimiter = self.lastcall_delimiter()

		if self.dbthings.postgres_db.does_table_exist(tablename):
			self.dbthings.postgres_db.load_csv_to_table(csvfilename,tablename,withtruncate,delimiter)
			rowcount = self.dbthings.postgres_db.queryone('SELECT COUNT(*) FROM ' + tablename)
			print('Loaded table ' + tablename + ' with ' + str(rowcount) + ' rows.')
			return_value = tablename
		else:
			print('Table ' + tablename + ' does not exist.  Cannot load. \n alternatively try: createload_postgres_from_csv(csvfilename)')

		return return_value

	def createload_postgres_from_csv(self,csvfilename,sztablename='',ddlfilename=''):
		return_value = ''

		self.loadcsvfile(csvfilename)
		ddl = self.guess_postgres_ddl(sztablename)
		delimiter = self.lastcall_delimiter()
		if sztablename == '':
			tablename = self.lastcall_tablename
		else:
			tablename = sztablename

		if not self.dbthings.postgres_db.does_table_exist(tablename):
			if ddlfilename != '':
				f = open(ddlfilename,'w')
				f.write(ddl)
				f.close()

			print(ddl)
			self.dbthings.postgres_db.execute(ddl)

			self.dbthings.postgres_db.load_csv_to_table(csvfilename,tablename,True,delimiter)

			rowcount = self.dbthings.postgres_db.queryone('SELECT COUNT(*) FROM ' + tablename)
			print('Created/Loaded table ' + tablename + ' with ' + str(rowcount) + ' rows.')
			return_value = tablename
		else:
			print('Table ' + tablename + ' already exists.  Stopping Load.')

		return return_value

	def justload_mysql_from_csv(self,csvfilename,tablename,withtruncate=False):
		return_value = ''
		self.loadcsvfile(csvfilename)
		delimiter = self.lastcall_delimiter()
		self.dbthings.mysql_db.connect()
		if self.dbthings.mysql_db.does_table_exist(tablename):
			self.dbthings.mysql_db.load_csv_to_table(csvfilename,tablename,withtruncate,delimiter)
			rowcount = self.dbthings.mysql_db.queryone('SELECT COUNT(*) FROM ' + tablename)
			print('Loaded table ' + tablename + ' with ' + str(rowcount) + ' rows.')
			return_value = tablename
		else:
			print('Table ' + tablename + ' does not exist.  Cannot load. \n alternatively try: createload_mysql_from_csv(csvfilename)')

		return return_value

	def createload_mysql_from_csv(self,csvfilename,sztablename='',ddlfilename=''):
		return_value = ''
		self.loadcsvfile(csvfilename)
		ddl = self.guess_mysql_ddl(sztablename)
		delimiter = self.lastcall_delimiter()
		if sztablename == '':
			tablename = self.lastcall_tablename
		else:
			tablename = sztablename

		if not self.dbthings.mysql_db.does_table_exist(tablename):
			if ddlfilename != '':
				f = open(ddlfilename,'w')
				f.write(ddl)
				f.close()
			print(ddl)
			self.dbthings.mysql_db.execute(ddl)
			self.dbthings.mysql_db.load_csv_to_table(csvfilename,tablename,True,delimiter)

			rowcount = self.dbthings.mysql_db.queryone('SELECT COUNT(*) FROM ' + tablename)
			print('Created/Loaded table ' + tablename + ' with ' + str(rowcount) + ' rows.')
			return_value = tablename
		else:
			print('Table ' + tablename + ' already exists.  Stopping Load.')

		return return_value

	def add_date_format(self,dt_fmt):
		self.dbthings.mysql_date_formats.append(dt_fmt)
		self.dbthings.postgres_date_formats.append(dt_fmt)

	def add_timestamp_format(self,tmsp_fmt):
		self.dbthings.mysql_timestamp_formats.append(tmsp_fmt)
		self.dbthings.postgres_timestamp_formats.append(tmsp_fmt)

	def lastcall_delimiter(self):
		return self.delimiter

	def utf8len(self,s):
			return len(s.encode('utf-8'))

	def logger(self,logline):
		if self.logging_on:
			print(logline)

	def loadcsvfile(self,csvfilename):
		if csvfilename != '':
			try:
				with open(csvfilename) as f:
					for csvline in f:
						self.csvfilename = csvfilename
						self.delimiter = self.GuessDelimiter(csvline)
						break

			except Exception as e:
				print('Cannot read file: ' + csvfilename)
				sys.exit(0)

		else:
				print('schemawiz.loadcsvfile(csvfilename) requires a valid csv file.')
				sys.exit(0)

	def analyze_csvfile(self,thisdatabase_type):
		self.analyzed = False

		if self.csvfilename == '':
			print('/* No csvfilename was provided to schemawiz.loadcsvfile().  Will use empty template */\n')
			self.SomeFileContents.append('field1,field2,field3,field4,field5')
			self.SomeFileContents.append('1999/02/18,0,0.001,textD,textE')
			self.get_column_names()
			self.get_column_types(thisdatabase_type)
			self.analyzed = True

		else:

			try:
				self.logger('Checking file size for ' + self.csvfilename + '\n')
				file_stats = os.stat(self.csvfilename)

				linecount = 0
				total_linesize = 0
				with open(self.csvfilename) as f:
					for line in f:
						linecount += 1
						if linecount != 1:
							total_linesize += self.utf8len(line)
						if linecount == 11:
							self.datalinesize = total_linesize/10

						self.SomeFileContents.append(line)
						if (linecount>100):
							break
				
				#self.logger('file has ' + str(len(self.SomeFileContents)) + ' lines')
				#self.logger('line size is ' + str(self.datalinesize) + ' ytes')
				#self.logger('file size is ' + str(file_stats.st_size) + ' bytes')


				self.get_column_names()
				self.get_column_types(thisdatabase_type)
				self.analyzed = True
			except Exception as e:
			
				print(str(e))
				sys.exit(0)

	def get_just_filename(self):
		justfilename=''
		if self.csvfilename.find('\\') > -1: # have a path and dirs
			fileparts = self.csvfilename.split('\\')
			justfilename = fileparts[len(fileparts)-1]
		else:
			if self.csvfilename != '':
				justfilename = self.csvfilename

		return justfilename

	def gettablename(self):

		now = (datetime.datetime.now())
		rando_tablename= 'tblcsv_' + str(now.year) + ('0' + str(now.month))[-2:] + str(now.day) + str(now.hour) + str(now.minute) 

		return rando_tablename

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

	def count_decimals(self,alphadict):
		count = 0
		for ch in alphadict:
			if '.'.find(ch) > -1:
				count += alphadict[ch]
		return count

	def get_datatype(self,datavalue,thisdatabase_type):
		chardict = {}
		data = ''
		if datavalue[0:1] == '"' and datavalue[-1:] == '"':
			#self.logger('enclosed in quotes ""')
			data = datavalue[1:-1]
			#self.logger('data: ' + data)
		else:
			data = datavalue.strip()

		chardict = self.count_chars(data)
		alphacount = self.count_alpha(chardict)
		nbrcount = self.count_nbr(chardict)
		deccount = self.count_decimals(chardict)

		lookslike = ''
		dtformat = ''
		timestamp_nbr = -1
		date_format_nbr = -1
		if thisdatabase_type != database_type.sqlite:
			timestamp_nbr = self.dbthings.match_timestamp_type(data,thisdatabase_type)
			date_format_nbr = self.dbthings.match_date_type(data,thisdatabase_type)


		if timestamp_nbr != -1:
			lookslike = 'timestamp' 
			if thisdatabase_type == database_type.Postgres:
				dtformat = self.dbthings.postgres_timestamp_formats[timestamp_nbr] 
			elif thisdatabase_type == database_type.MySQL:
				dtformat = self.dbthings.mysql_timestamp_formats[timestamp_nbr] 

		elif date_format_nbr != -1:
			lookslike = 'date' 
			if thisdatabase_type == database_type.Postgres:
				dtformat = self.dbthings.postgres_date_formats[date_format_nbr] 
			elif thisdatabase_type == database_type.MySQL:
				dtformat = self.dbthings.mysql_date_formats[date_format_nbr] 

		elif alphacount == 0 and deccount == 1:
			# 123.123232222
			if self.dbthings.match_float_type(data):
				lookslike = 'numeric'
			else:
				lookslike = 'text'


		elif self.dbthings.match_integer_type(data) :
			# 123
			lookslike = 'integer'

		else:
			lookslike = 'text'

		return lookslike,dtformat

	def get_column_types(self,thisdatabase_type):

		found_datatypes = {}
		found_datavalues = {}
		found_datefomat = {}
		for i in range(1,len(self.SomeFileContents)):
			dataline = self.SomeFileContents[i].strip().split(self.delimiter)
			#print(dataline)
			for j in range(0,len(dataline)):

				thisdatatype,dtformat = self.get_datatype(dataline[j],thisdatabase_type)
				#print(thisdatatype)
				if self.column_names[j] not in found_datatypes:
					found_datatypes[self.column_names[j]] = thisdatatype
					found_datavalues[self.column_names[j]] = dataline[j]
					found_datefomat[self.column_names[j]]	= dtformat
				else:
					if found_datatypes[self.column_names[j]] == 'date' and thisdatatype =='date' and found_datefomat[self.column_names[j]] != dtformat:
						found_datatypes[self.column_names[j]] == 'text'
					elif found_datatypes[self.column_names[j]] == 'timestamp' and thisdatatype =='timestamp' and found_datefomat[self.column_names[j]] != dtformat:
						found_datatypes[self.column_names[j]] == 'text'
					elif found_datatypes[self.column_names[j]] != thisdatatype:
						if found_datatypes[self.column_names[j]] == 'text' or thisdatatype == 'text':
							found_datatypes[self.column_names[j]] == 'text'
						elif found_datatypes[self.column_names[j]] == 'numeric' or thisdatatype == 'numeric':
							found_datatypes[self.column_names[j]] == 'numeric'
						elif found_datatypes[self.column_names[j]] == 'date' or thisdatatype == 'date':
							found_datatypes[self.column_names[j]] == 'text'

		for k in range(0,len(self.column_names)):
			self.column_sample.append(found_datavalues[self.column_names[k]].replace('"',''))
			self.column_dateformats.append(found_datefomat[self.column_names[k]])

			self.column_datatypes.append(found_datatypes[self.column_names[k]])
			self.mysql_datatypes.append(self.translate_dt(database_type.MySQL,found_datatypes[self.column_names[k]]))

			self.BigQuery_datatypes.append(self.translate_dt(database_type.BigQuery,found_datatypes[self.column_names[k]]))
			self.sqlite_datatypes.append(self.translate_dt(database_type.sqlite,found_datatypes[self.column_names[k]]))

			if not self.IsaDateField and self.translate_dt(database_type.BigQuery,found_datatypes[self.column_names[k]]) == 'DATE': 		
				self.IsaDateField = True
				self.DateField = self.column_names[k]
			elif self.translate_dt(database_type.BigQuery,found_datatypes[self.column_names[k]]) != 'FLOAT64':
				if self.clusterField1 == '':
					self.clusterField1 = self.column_names[k]
				elif self.clusterField2 == '':
					self.clusterField2 = self.column_names[k]
				elif self.clusterField3 == '':
					self.clusterField3 = self.column_names[k]

		for m in range(0,len(self.column_datatypes)):
			self.logger('column ' + str(self.column_names[m]) + ' has data type ' + str(self.column_datatypes[m]))


	def translate_dt(self,targettype,postgres_datatype):
		if targettype == database_type.BigQuery:
			if postgres_datatype.lower().strip() == 'text':
				return 'STRING'
			elif postgres_datatype.lower().strip() == 'date':
				return 'DATE'
			elif postgres_datatype.lower().strip() == 'timestamp':
				return 'TIMESTAMP'
			elif postgres_datatype.lower().strip() == 'integer':
				return 'INT64'
			elif postgres_datatype.lower().strip() == 'numeric':
				return 'FLOAT64'
			else:
				return 'UNKNOWN'
		elif targettype == database_type.MySQL:
			if postgres_datatype.lower().strip() == 'numeric':
				return 'float'
			else:
				return postgres_datatype
		elif targettype == database_type.sqlite:
			if postgres_datatype.lower().strip() == 'integer':
				return 'integer'
			elif postgres_datatype.lower().strip() == 'numeric':
				return 'real'
			else:
				return 'text'

		else:
			return postgres_datatype


	def clean_text(self,ptext): # remove optional double quotes
		text = ptext.strip()
		if (text[:1] == '"' and text[-1:] == '"'):
			return text[1:-1]
		else:
			return text

	def clean_column_name(self,col_name):

		new_column_name = col_name
		chardict = self.count_chars(col_name)
		alphacount = self.count_alpha(chardict)
		nbrcount = self.count_nbr(chardict)
		if ((len(col_name)-2) == (alphacount + nbrcount)) and '1234567890'.find(col_name[:1]) == -1:
			new_column_name = self.clean_text(col_name) # .replace('"','').strip()


		return new_column_name

	def get_column_names(self):
		self.delimiter = self.GuessDelimiter(self.SomeFileContents[0])
		self.logger('file delimiter is ' + self.delimiter)
		self.column_names = self.SomeFileContents[0].strip().split(self.delimiter)
		self.logger('Column Names are ' + str(self.column_names))

		for i in range(0,len(self.column_names)):
			self.column_names[i] = self.clean_column_name(self.column_names[i])

	def GuessDelimiter(self,first_row):
		if self.force_delimiter != '':
			delimiter_guess = self.force_delimiter
		else:
			if first_row.find('\t') > -1:
				delimiter_guess = '\t'
			elif first_row.find(',') > -1:
				delimiter_guess = ','
			else:
				delimiter_guess = '~'

		return delimiter_guess

	def guess_BigQueryExternal_ddl(self,useproject='',usedataset='',usetablename=''):
		self.dbthings.connect_local_db(database_type.MySQL)

		if useproject == '':
			project = 'schemawiz-123'
		else:
			project = useproject

		if usedataset == '':
			dataset = 'sampledataset'
		else:
			dataset = usedataset

		if usetablename == '':
			tablename = self.gettablename()
		else:
			tablename = usetablename

		self.lastcall_tablename = tablename

		project = project.replace(' ','').lower()
		dataset = dataset.replace(' ','').lower()
		tablename = tablename.replace(' ','').lower()
		
		if not self.analyzed:
			self.analyze_csvfile(database_type.MySQL) # database_type.BigQuery

		sql = 'CREATE EXTERNAL TABLE IF NOT EXISTS `' + project + '.' + dataset + '.' + tablename + '` (\n'
		for i in range(0,len(self.column_names)):
			sql += '\t' + self.column_names[i] + ' ' + self.BigQuery_datatypes[i] + ' \t\t/* eg. ' + self.column_sample[i] + ' */ ' 
			
			if self.BigQuery_datatypes[i].strip().lower() == 'date' or self.BigQuery_datatypes[i].strip().lower() == 'timestamp':
				sql += "OPTIONS (description='" + self.BigQuery_datatypes[i].strip().lower() + " format in csv [" + self.column_dateformats[i] + "]')"

			sql += ',\n'

		sql = sql[:-2] + '\n)'
		
		sql += " OPTIONS (\n    format = 'CSV',\n    Field_delimiter = '" + self.delimiter  + "',\n    uris = ['gs://bucket/" 
		sql += self.get_just_filename() + "*'],\n    skip_leading_rows = 1,\n    "
		sql += "description='" + "This externally stored, BigQuery table was defined by schemawiz for creating a BQ table to use csv files as source.'\n);"


		return sql

	def guess_BigQuery_ddl(self,useproject='',usedataset='',usetablename=''):
		self.dbthings.connect_local_db(database_type.MySQL)

		if useproject == '':
			project = 'schemawiz-123'
		else:
			project = useproject

		if usedataset == '':
			dataset = 'sampledataset'
		else:
			dataset = usedataset

		if usetablename == '':
			tablename = self.gettablename()
		else:
			tablename = usetablename

		self.lastcall_tablename = tablename

		project = project.replace(' ','').lower()
		dataset = dataset.replace(' ','').lower()
		tablename = tablename.replace(' ','').lower()
		
		if not self.analyzed:
			self.analyze_csvfile(database_type.MySQL) # database_type.BigQuery

		sql = 'CREATE TABLE IF NOT EXISTS `' + project + '.' + dataset + '.' + tablename + '` (\n'
		for i in range(0,len(self.column_names)):
			sql += '\t' + self.column_names[i] + ' ' + self.BigQuery_datatypes[i] + ' \t\t/* eg. ' + self.column_sample[i] + ' */ ' 
			
			if self.BigQuery_datatypes[i].strip().lower() == 'date' or self.BigQuery_datatypes[i].strip().lower() == 'timestamp':
				sql += "OPTIONS (description='" + self.BigQuery_datatypes[i].strip().lower() + " format in csv [" + self.column_dateformats[i] + "]')"

			sql += ',\n'


		sql = sql[:-2] + '\n)\n'
		
		if self.IsaDateField:
			sql += 'PARTITION BY ' + self.DateField + '\n'
		
		if self.clusterField1 != '':
			sql += 'CLUSTER BY \n    ' + self.clusterField1 + ',\n'

		if self.clusterField2 != '':
			sql += '    ' + self.clusterField2 + ',\n'

		if self.clusterField3 != '':
			sql += '    ' + self.clusterField3 + ',\n'

		sql = sql[:-2]

		sql += "\nOPTIONS (\n    require_partition_filter = False,\n    "
		sql += "description = 'This BigQuery table was defined by schemawiz for loading the csv file " + self.get_just_filename() + ", delimiter (" + self.delimiter + ")' \n);"
    
		return sql

	def guess_sqlite_ddl(self,usetablename=''):
		self.dbthings.connect_local_db(database_type.sqlite)
		if not self.analyzed:
			self.analyze_csvfile(database_type.sqlite)
		if usetablename == '':
			tablename = self.gettablename()
		else:
			tablename = usetablename

		self.lastcall_tablename = tablename

		fldcommentsql = '' 
		sql = '/* DROP TABLE IF EXISTS ' + tablename + '; */\n'

		sql += 'CREATE TABLE IF NOT EXISTS ' + tablename + '(\n'
		for i in range(0,len(self.column_names)):
			sql += '\t' + self.column_names[i] + ' ' + self.sqlite_datatypes[i] + ' \t\t/* eg. ' + self.column_sample[i] + ' */ ,\n'

		sql = sql[:-2] + '\n);\n\n'

		return sql

	def guess_postgres_ddl(self,usetablename=''):
		
		self.dbthings.connect_local_db(database_type.Postgres)

		if not self.analyzed:
			self.analyze_csvfile(database_type.Postgres)
		if usetablename == '':
			tablename = self.gettablename()
		else:
			tablename = usetablename

		self.lastcall_tablename = tablename

		fldcommentsql = '' 
		sql = 'DROP TABLE IF EXISTS ' + tablename + ';\n'

		sql += 'CREATE TABLE IF NOT EXISTS ' + tablename + '(\n'
		for i in range(0,len(self.column_names)):
			sql += '\t' + self.column_names[i] + ' ' + self.column_datatypes[i] + ' \t\t/* eg. ' + self.column_sample[i] + ' */ ,\n'
			if self.column_datatypes[i].strip().lower() == 'date' or self.column_datatypes[i].strip().lower() == 'timestamp':
				fldcommentsql += 'COMMENT ON COLUMN ' + tablename + '.' + self.column_names[i] + " IS '" + self.column_datatypes[i].strip().lower() + " format in csv [" + self.column_dateformats[i] + "]';\n"

		sql = sql[:-2] + '\n);\n\n'
		sql += 'COMMENT ON TABLE ' + tablename + " IS 'This Postgres table was defined by schemawiz for loading the csv file " + self.csvfilename + ", delimiter (" + self.delimiter + ")';\n"
		sql += fldcommentsql
		#print(sql)

		return sql

	def guess_mysql_ddl(self,usetablename=''):
		self.dbthings.connect_local_db(database_type.MySQL)

		if not self.analyzed:
			self.analyze_csvfile(database_type.MySQL)
		if usetablename == '':
			tablename = self.gettablename()
		else:
			tablename = usetablename
		self.lastcall_tablename = tablename

		sql = '/* DROP TABLE IF EXISTS ' + tablename + '; */\n'

		sql += ' CREATE TABLE IF NOT EXISTS ' + tablename + '(\n'
		for i in range(0,len(self.column_names)):
			sql += '\t' + self.column_names[i] + ' ' + str(self.mysql_datatypes[i]) + ' \t\t/* eg. ' + self.column_sample[i] + ' */ '
			if str(self.mysql_datatypes[i]).strip().lower() == 'date' or str(self.mysql_datatypes[i]).strip().lower() == 'timestamp':
				sql += 'COMMENT "' + str(self.mysql_datatypes[i]).strip().lower() + ' format in csv [' + self.column_dateformats[i] + ']" '
			sql += ' ,\n'

		sql = sql[:-2] + '\n) \n'
		
		sql += 'COMMENT="This MySQL table was defined by schemawiz for loading the csv file ' + self.csvfilename + ', delimiter (' + self.delimiter + ')"; \n'

		return sql


if __name__ == '__main__':
	main()
