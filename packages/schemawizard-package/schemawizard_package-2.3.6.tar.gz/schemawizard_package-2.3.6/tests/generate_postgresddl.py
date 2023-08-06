"""
  Dave Skura
"""

from schemawizard_package.schemawizard import schemawiz

obj = schemawiz()

obj.loadcsvfile('tesla.csv')

postgres_ddl = obj.guess_postgres_ddl()

print('Tablename used in CREATE TABLE statement: ' + obj.lastcall_tablename + '\n')

print(postgres_ddl)

