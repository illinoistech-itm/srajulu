from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import findspark

spark = SparkSession.builder.appName("Assignment04").getOrCreate()
findspark.add_packages('mysql:mysql-connector-java:8.0.11')

# Read Option 1: Loading data from a JDBC source using load method
jdbcDF1 = (spark.read
.format("jdbc")
.option("url", "jdbs:sqlserver://localhost:;databaseName:employees")
.option("dbtable", "employees")
.option("user", "worker")
.option("password", "cluster")
.load())