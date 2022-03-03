from pyspark.sql import SparkSession
from pyspark.sql.functions import *


spark = SparkSession.builder.appName("Assignment04").getOrCreate()


# Read Option 1: Loading data from a JDBC source using load method
jdbcDF1 = (spark.read.format("jdbc").option("url", "jdbc:mysql://localhost:3306;databaseName:employees").option("dbtable", "employees").option("user", "worker").option("password", "cluster").load())