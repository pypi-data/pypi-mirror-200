# Methods 

## __init__(self,csvfilename='')
Optionally pass in a csv filename to the contructor.

>
> from schemawizard_package.schemawizard import schemawiz
>
> myschema = schemawiz('tesla.csv')
>
>

## def guess_postgres_ddl(self,usetablename='')
This will return a valid Postgres CREATE TABLE statement.  If you run this statement in Postgres, you will get a table which matches the schema of the csv file selected.  

If you pass a parameter of tablename to this method, it will be used, otherwise, a random tablename will be generated.
>
> from schemawizard_package.schemawizard import schemawiz
>
> myschema = schemawiz('tesla.csv')
>
> postgres_ddl = myschema.guess_postgres_ddl('my_new_csv_table')
>
> print(postgres_ddl)
>

## def guess_mysql_ddl(self,usetablename='')
This will return a valid MySQL CREATE TABLE statement.  If you run this statement in MySQL, you will get a table which matches the schema of the csv file selected.  

If you pass a parameter of tablename to this method, it will be used, otherwise, a random tablename will be generated.
>
> from schemawizard_package.schemawizard import schemawiz
>
> myschema = schemawiz('tesla.csv')
>
> mysql_ddl = myschema.guess_mysql_ddl('my_new_csv_table')
>
> print(mysql_ddl)
>

## def guess_BigQuery_ddl(self,useproject='',usedataset='',usetablename='')
This will return a valid BigQuery CREATE TABLE statement.  If you run this statement in BigQuery, you will get a table which matches the schema of the csv file selected.  

If you pass a parameter of project, dataset and tablename to this method, it will be used, otherwise, a random name values will be generated.
>
> from schemawizard_package.schemawizard import schemawiz
>
> myschema = schemawiz('tesla.csv')
>
> mybigquery_ddl = myschema.guess_BigQuery_ddl('mygcpproject-007','mydataset','mynormal_bqtable')
>
> print(mybigquery_ddl)
>


## def guess_BigQueryExternal_ddl(self,useproject='',usedataset='',usetablename='')
This will return a valid BigQuery CREATE EXTERNAL TABLE statement.  If you run this statement in BigQuery, you will get an EXTERNAL table in BigQuery which matches the schema of the csv file selected.  This table requires a gcp bucket, location and file pattern for where the data in the table will be stored.

If you pass a parameter of project, dataset and tablename to this method, it will be used, otherwise, a random name values will be generated.
>
> from schemawizard_package.schemawizard import schemawiz
>
> myschema = schemawiz('tesla.csv')
>
> mybigquery_external_ddl = myschema.guess_BigQueryExternal_ddl('mygcpproject-007','mydataset','my_csvexternal_bqtable')
>
> print(mybigquery_external_ddl)
>

## self.force_delimiter = ''
schemawiz will automatically select a field delimiter, however, you can override this by setting the force_delimiter property.
You can force schemawiz to use a delimiter instead of guessing one.
>
> from schemawizard_package.schemawizard import schemawiz
>
> myschema = schemawiz()
>
> myschema.force_delimiter = ','
>

## def loadcsvfile(self,csvfilename)
After setting the delimiter, you can call loadcsvfile() to prepare schemawiz for ddl output.
>
> from schemawizard_package.schemawizard import schemawiz
>
> myschema = schemawiz()
>
> myschema.force_delimiter = ','
>
> myschema.loadcsvfile('tesla.csv')
>
