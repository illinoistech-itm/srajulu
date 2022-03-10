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

data_frame = spark.read.format("jdbc")\
.option("url","jdbc:mysql://localhost/Assignment05b")\
.option("driver","com.mysql.jdbc.Driver")\
.option("dbtable","temperatures")\
.option("user","worker")\
.option("password","cluster").load()
data_frame.show()

data_source.createOrReplaceTempView("Assignment_05_TempView")
data_frame.createOrReplaceTempView("Assignment_05_TempView_B")

# Unoin of Tables
DF_Union = data_source.union(data_frame)
DF_Union.show()
DF_Union.createOrReplaceTempView("Union_Data_Frame")
DF_Union_Query = DF_Union.select("ID",split(col("temperature"),",").alias("temperatures")).drop("temperature")
DF_Union_Query.printSchema()
DF_Union_Query.show()
DF_Union_Query.createOrReplaceTempView("Union_Data_Temp")

# Find all temperatures above 40 Celsius
spark.sql("""SELECT ID,temperatures, filter(temperatures, t -> t > 40) as high FROM Union_Data_Temp""").show()

# Assignment Part II
FilePath_TripDelay = "/home/vagrant/LearningSparkV2/databricks-datasets/learning-spark-v2/flights/departuredelays.csv"
FilePath_AirportCodes = "/home/vagrant/LearningSparkV2/databricks-datasets/learning-spark-v2/flights/airport-codes-na.txt"