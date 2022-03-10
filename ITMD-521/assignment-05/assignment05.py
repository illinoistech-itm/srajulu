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

data_frame = (spark.read.format("csv").options(header="true", inferSchema="true", sep="\t").load(FilePath_AirportCodes))
data_frame.createOrReplaceTempView("Airports_NA")
data_frame.show()

# Read airport-codes-na.txt file

data_frame_1 = (spark.read
.format("csv")
.options(header="true")
.load(FilePath_TripDelay))

data_frame_1 = (data_frame_1
.withColumn("delay", expr("CAST(delay as INT) as delay"))
.withColumn("distance", expr("CAST(distance as INT) as distance")))
data_frame_1.createOrReplaceTempView("departureDelays")
data_frame_1.show()

# Table creation
foo = (data_frame_1.filter(expr("""origin == 'SEA' and destination == 'SFO' and date like '01010%' and delay > 0""")))
foo.createOrReplaceTempView("foo")
foo.show()

spark.sql("""
      SELECT a.City, a.State, f.date, f.delay, f.distance, f.destination
      FROM foo f 
      JOIN Airports_NA a ON a.IATA = f.origin """).show()

# Assignment Part III

# Adding new column
Column_1 = (foo.withColumn("status", expr("CASE WHEN delay <= 10 THEN 'On-time' ELSE 'Delayed' END")))
Column_1.show()

# Columnn Dropped
Column_Drop = Column_1.drop("delay")
Column_Drop.show()

# Column Renamed
Column_Rename = Column_Drop.withColumnRenamed("status", "flight_status")
Column_Rename.show()

# Pivot data population
spark.sql("""SELECT * FROM (
SELECT destination, CAST(SUBSTRING(date, 0, 2) AS int) AS month, delay
FROM departureDelays WHERE origin = 'SEA' ) 
PIVOT ( CAST(AVG(delay) AS DECIMAL(4, 2)) AS AvgDelay, MAX(delay) AS MaxDelay FOR month IN (1 JAN, 2 FEB))
ORDER BY destination""").show()