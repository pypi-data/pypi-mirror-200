"""
  Dave Skura
"""
from postgresdave_package.postgresdave import db 
from schemawizard_package.schemawizard import schemawiz

mydb = db()
csvfilename = 'sample.csv'
tblname = 'sample_csv'

print ("Processing " + csvfilename) # 

mydb.load_csv_to_table(csvfilename,tblname,False,schemawiz(csvfilename).delimiter)

print('Table now has ' + tblname + ' has ' + str(mydb.queryone('SELECT COUNT(*) FROM ' + tblname)) + ' rows.\n') 

mydb.close()


