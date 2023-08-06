"""
  Dave Skura
"""
from schemawizard_package.schemawizard import schemawiz

csvfilename = 'sample.csv'

r = schemawiz().createload_mysql_from_csv(csvfilename,'sample2_csv')

print(r + ' created.')

