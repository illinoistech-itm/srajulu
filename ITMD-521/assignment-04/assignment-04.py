from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark import *

spark = SparkSession\
.builder\
.master('local[*]')\
.appName('Assignment04')\
.config('spark.driver.extraClassPath', '/home/vagrant/spark/jars/mysql-connector-java-8.0.28.jar')\
.getOrCreate()

JDBC_DF = spark.read.format("jdbc").option("url","jdbc:mysql://localhost/employees").option("driver","com.mysql.jdbc.Driver").option("dbtable","employees").option("user","worker").option("password","cluster").load().show()