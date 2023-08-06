def get_dbutils(spark):
	try:
		from pyspark.dbutils import DBUtils
		dbutils = DBUtils(spark)
	except ImportError:
		import IPython
		dbutils = IPython.get_ipython().user_ns["dbutils"]
	return dbutils

dbutils = get_dbutils(spark)
		
def test(path):
	dbutils.notebook.run(path,1200)