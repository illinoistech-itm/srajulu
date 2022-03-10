from select import select
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import expr
from pyspark.sql.functions import split, col

spark = SparkSession\
.builder\
.master('local[*]')\
.appName('Assignment05')\
.config('spark.driver.extraClassPath', '/home/vagrant/spark/mysql-connector-java-8.0.28.jar')\
.getOrCreate()


data_source = spark.read.format("jdbc")\
.option("url","jdbc:mysql://localhost/Assignment05")\
.option("driver","com.mysql.jdbc.Driver")\
.option("dbtable","temperatures")\
.option("user","worker")\
.option("password","cluster").load()
data_source.show()
data_source.printSchema()