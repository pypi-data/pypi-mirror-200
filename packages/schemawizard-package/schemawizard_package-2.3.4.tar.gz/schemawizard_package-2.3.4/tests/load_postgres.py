"""
  Dave Skura
"""
from schemawizard_package.schemawizard import schemawiz

csvfilename = 'tesla.csv'
tablename = 'tesla_csv'
withtruncate=False
r = schemawiz().justload_postgres_from_csv(csvfilename,tablename,withtruncate)

if r !='':
	print(r + ' loaded.')
