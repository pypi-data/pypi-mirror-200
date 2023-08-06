"""
  Dave Skura
"""

from schemawizard_package.schemawizard import schemawiz

BigQuery_ddl = schemawiz('tesla.csv').guess_BigQuery_ddl('mygcpproject-007','mydataset','mynormal_bqtable')
print(BigQuery_ddl)
