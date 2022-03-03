from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark import *

spark = SparkSession\
.builder\
.master('local[*]')\
.appName('Assignment04')\
.config('spark.driver.extraClassPath', '/home/vagrant/spark/jars/mysql-connector-java-8.0.28.jar')\
.getOrCreate()

JDBC_DF = spark.read.format("jdbc").option("url","jdbc:mysql://localhost/employees").option("driver","com.mysql.jdbc.Driver").option("dbtable","employees").option("user","worker").option("password","cluster").load().createOrReplaceTempView("Employees")

#Assignment Part 1
# Q1 - Display the count of the number of records in the DF
Q1_DF=spark.sql("Select count(*) from Employees")
Q1_DF.show()

# Display the schema of the Employees Table from the DF
# Q2 - Print Schema
Q1_DF.printSchema()