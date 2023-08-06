"""
  Dave Skura
"""
from schemawizard_package.schemawizard import schemawiz
csvfilename = 'sample.csv'

#ddl = schemawiz(csvfilename).guess_postgres_ddl()
ddl = schemawiz(csvfilename).guess_mysql_ddl()
#ddl = schemawiz(csvfilename).guess_postgres_ddl(csvfilename.replace('.','_'))

print(ddl)



