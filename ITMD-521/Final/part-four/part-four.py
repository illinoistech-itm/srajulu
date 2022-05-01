from calendar import month
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import year
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import col, mean, desc
from pyspark.sql.functions import year
from pyspark.sql.functions import *
from pyspark.sql.functions import to_timestamp
from pyspark.sql.functions import stddev
import pyspark.sql.functions as func

import os
import sys


if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usage: part-four.py <file> ", file=sys.stderr)
        sys.exit(-1)

    con = SparkConf()
    con.set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.2.0')
    con.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider')
    
    con.set('spark.hadoop.fs.s3a.access.key', os.getenv('SECRETKEY'))
    con.set('spark.hadoop.fs.s3a.secret.key', os.getenv('ACCESSKEY'))
    con.set("spark.hadoop.fs.s3a.endpoint", "http://192.168.172.50:9000")

    spark = SparkSession.builder.appName("suraj part four").config('spark.driver.host','192.168.172.45').config(conf=con).getOrCreate()

    parquet_file = "s3a://srajulu/80.parquet"
    spark.sql("set spark.sql.legacy.timeParserPolicy=LEGACY")

    parquetdatafrm = spark.read.format("parquet").option("header", "true").option("inferSchema", "true").load(parquet_file)
    parquetdatafrm.printSchema()

    # query 1
    #query_parquet_dataframe = (parquetdatafrm.withColumn("ForObsDate", to_timestamp(col("ObservationDate"), "MM/dd/yyyy")).drop("ObservationDate"))

    # query 1 - Count the number of records
    #query_parquet_dataframe.select("WeatherStation", "VisibilityDistance", "AirTemperature", month("ForObsDate"), year("ForObsDate")).where(month("ForObsDate") == 2).distinct().show(20)

    #Query 2
    #avg_new_parquet_dataframe = query_parquet_dataframe.filter(month("ForObsDate") == 2).groupBy("AirTemperature").count().orderBy(desc("count"))
    #avg_new_parquet_dataframe.select(mean("AirTemperature")).show(10)

    # query 3 - Median air temperature
    #query_parquet_dataframe.groupBy("WeatherStation").agg(func.percentile_approx("AirTemperature", 0.5).alias("MedianAirTemperature)")).show(10)
   
    # query 4 -Standard deviation air temperature
    #query_parquet_dataframe.select(stddev("AirTemperature")).show(10)

    #query 5
    #The weather station ID that has the lowest recorded temperature per year.
    lowest_dataframe_80 = spark.sql('select max(WeatherStation) as WeatherStation, YEAR(ObservationDate), min(AirTemperature) from parquet_dataframe_50_view GROUP BY YEAR(ObservationDate) ORDER BY min(AirTemperature)')
    lowest_dataframe_80.show()

    #query 6
    # The weather station ID that has the highest recorded temperature per year.
    highest_dataframe_80 = spark.sql('select max(WeatherStation) as WeatherStation, YEAR(ObservationDate), max(AirTemperature) from parquet_dataframe_50_view GROUP BY YEAR(ObservationDate) ORDER BY max(AirTemperature)')
    lowest_dataframe_80.show()