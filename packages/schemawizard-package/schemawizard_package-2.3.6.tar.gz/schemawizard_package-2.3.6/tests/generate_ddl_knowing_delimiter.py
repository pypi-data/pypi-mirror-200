"""
	Dave Skura
"""

from schemawizard_package.schemawizard import schemawiz

myschema = schemawiz()

myschema.force_delimiter = ','

myschema.loadcsvfile('tesla.csv')

print(myschema.guess_postgres_ddl())