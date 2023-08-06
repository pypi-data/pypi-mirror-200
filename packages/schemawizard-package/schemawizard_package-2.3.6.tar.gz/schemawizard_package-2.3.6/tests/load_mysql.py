"""
  Dave Skura
"""
from schemawizard_package.schemawizard import schemawiz

csvfilename = 'tesla.csv'
tablename = 'tesla2_csv'
withtruncate=False
r = schemawiz().justload_mysql_from_csv(csvfilename,tablename,withtruncate)

if r !='':
	print(r + ' loaded.')
