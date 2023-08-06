"""
  Dave Skura
"""

from schemawizard_package.schemawizard import schemawiz

mysql_ddl = schemawiz('tesla.csv').guess_mysql_ddl('my_myql_table1')
print(mysql_ddl)
