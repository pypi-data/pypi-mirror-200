"""
  Dave Skura
"""

from schemawizard_package.schemawizard import schemawiz

mysql_ddl = schemawiz('').guess_mysql_ddl('my_myql_table1')
print(mysql_ddl)

postgres_ddl = schemawiz('tesla.csv').guess_postgres_ddl('my_postgres_table1')
print(postgres_ddl)


BigQuery_ddl = schemawiz('tesla.csv').guess_BigQuery_ddl('mygcpproject-007','mydataset','mynormal_bqtable')
print(BigQuery_ddl)


BigQueryExternal_ddl = schemawiz('tesla.csv').guess_BigQueryExternal_ddl('mygcpproject-007','mydataset','mycsvbased_bqtable')
print(BigQueryExternal_ddl)

