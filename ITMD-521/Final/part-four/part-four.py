from calendar import month
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import year
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import col
from pyspark.sql.functions import year
from pyspark.sql.functions import *
from pyspark.sql.functions import to_timestamp

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

    spark = SparkSession.builder.appName("suraj part three").config('spark.driver.host','192.168.172.45').config(conf=con).getOrCreate()

    parquet_file = "s3a://srajulu/80.parquet"
    spark.sql("set spark.sql.legacy.timeParserPolicy=LEGACY")

    parquet_df = spark.read.format("parquet").option("header", "true").option("inferSchema", "true").load(parquet_file)
    parquet_df.printSchema()
    
    #1. find all of the weather station ids that have registered days (count) of visibility (VisibilityDistance) less than 200 per year.
    query1 = parquet_file.withColumnRenamed("WeatherStationIds", "WeatherStation")
    query1_df = (query1.withColumn("NewObservationDate", to_timestamp(col("ObservationDate"), "MM/dd/yyyy")).drop("ObservationDate"))

    # query 1
    query1_df.filter(month("New-Observation-Date") == 2).groupBy(month('New-Observation-Date')).count().orderBy('count', ascending=False).show()
    
    
   
