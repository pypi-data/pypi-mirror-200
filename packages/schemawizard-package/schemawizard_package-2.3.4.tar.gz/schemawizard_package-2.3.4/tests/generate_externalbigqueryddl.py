"""
  Dave Skura
"""

from schemawizard_package.schemawizard import schemawiz

BigQueryExternal_ddl = schemawiz('tesla.csv').guess_BigQueryExternal_ddl('mygcpproject-007','mydataset','mycsvbased_bqtable')
print(BigQueryExternal_ddl)

