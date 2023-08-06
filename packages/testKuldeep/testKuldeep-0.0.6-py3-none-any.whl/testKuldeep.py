from pyspark.sql import SparkSession
from concurrent.futures import ThreadPoolExecutor
spark = SparkSession.builder.getOrCreate()
def get_dbutils(spark):
	try:
		from pyspark.dbutils import DBUtils
		dbutils = DBUtils(spark)
	except ImportError:
		import IPython
		dbutils = IPython.get_ipython().user_ns["dbutils"]
	return dbutils

dbutils = get_dbutils(spark)
		
dicct = {}
countt = 0
def upda(path):
    for j in path.split(","):
        dicct[j.split("/")[-1]] = 0
    global countt
    countt = 1
    
def sequence_run(path):

    if countt == 0:
        upda(path)
        for i in path.split(","):
            if dicct[i.split("/")[-1]] == 0:
                print("Running notebook %s" % i.split("/")[-1])
                try:
                    dbutils.notebook.run(i,1200)
                    dicct[i.split("/")[-1]] = 1
                except:
                    print(i.split("/")[-1],"failed")
                    dicct[i.split("/")[-1]] = 0
                    break
            else:
                pass
    else:
        for i in path.split(","):
            if dicct[i.split("/")[-1]] == 0:
                print("Running notebook %s" % i.split("/")[-1])
                try:
                    dbutils.notebook.run(i,1200)
                    dicct[i.split("/")[-1]] = 1
                except:
                    print(i.split("/")[-1],"failed")
                    dicct[i.split("/")[-1]] = 0
                    break
            else:
                pass
	
def parallel_run(filepath):
    class NotebookData:
        def __init__(self, path, timeout, parameters=None, retry=0):
            self.path = path
            self.timeout = timeout
            self.parameters = parameters
            self.retry = retry

        def submitNotebook(notebook):
            print("Running notebook %s" % str(notebook.path).split("/")[-1])
            try:
                if (notebook.parameters):
                    return dbutils.notebook.run(notebook.path, notebook.timeout, notebook.parameters)
                else:
                    try:
                        return dbutils.notebook.run(notebook.path, notebook.timeout)
                    except:
                        print(str(notebook.path).split("/")[-1], 'failed')
            except Exception:
                if notebook.retry < 1:
                    raise
                print("Retrying notebook %s" % notebook.path)
                notebook.retry = notebook.retry - 1
                submitNotebook(notebook)

    def parallelNotebooks(notebooks, numInParallel):
        with ThreadPoolExecutor(max_workers=numInParallel) as ec:
            return [ec.submit(NotebookData.submitNotebook, notebook) for notebook in notebooks]

    notebooks = []
    for path in filepath.split(','):
        notebooks.append(NotebookData(path, 1200))

    res = parallelNotebooks(notebooks, 10)
    result = [i.result(timeout=3600) for i in res] # This is a blocking call.