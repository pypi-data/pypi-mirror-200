"""
  Dave Skura
"""
from schemawizard_package.schemawizard import schemawiz
from postgresdave_package.postgresdave import db 

mydb = db()
mydb.connect()
print(mydb.dbstr())

csvfilename = 'tesla.csv'
tblname = 'tesla_csv'

obj = schemawiz(csvfilename)
print ("Processing " + csvfilename) # 

postgres_ddl = obj.guess_postgres_ddl(tblname)

if mydb.does_table_exist(obj.lastcall_tablename):
	print('table already exists')
	print('Table currenty has ' + obj.lastcall_tablename + ' has ' + str(mydb.queryone('SELECT COUNT(*) FROM ' + obj.lastcall_tablename)) + ' rows.') 
	print('dropping table ' + obj.lastcall_tablename)
	mydb.execute('DROP TABLE ' + obj.lastcall_tablename + ' CASCADE')


print('\nCreating ' + obj.lastcall_tablename)
mydb.execute(postgres_ddl)
print('Table created.')
mydb.load_csv_to_table(csvfilename,obj.lastcall_tablename,False,obj.delimiter)
print('Table loaded.')
print('Table now has ' + obj.lastcall_tablename + ' has ' + str(mydb.queryone('SELECT COUNT(*) FROM ' + obj.lastcall_tablename)) + ' rows.\n') 


