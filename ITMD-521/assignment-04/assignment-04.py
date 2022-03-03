from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("Assignment04").getOrCreate()

# Read Option 1: Loading data from a JDBC source using load method
jdbcDF1 = (spark.read
.format("jdbc")
.option("url", "jdbs:sqlserver://localhost:1433;databaseName:employees")
.option("dbtable", "dbo.employees")
.option("user", "worker")
.option("password", "")
.load())