#from __future__ import function
#from optparse import Option
#from os import truncate
from os import truncate
from statistics import mode
import sys

from pyspark.sql import SparkSession
#from pyspark.sql.function import count
from pyspark.sql.types import *

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: DivvyTrips <file>", file=sys.stderr)
        sys.exit(-1)

    spark = (SparkSession.builder.appName("Assignment 1").getOrCreate())
    data_source = sys.argv[1]

## Inferring Schema

    infer_divvy_df = (spark.read.format("csv").option("header","true").option("inferSchema","true").load(data_source))
    infer_divvy_df.show(n=10, truncate=False)
    infer_divvy_df.printSchema()
    parquet_path = infer_divvy_df.write.format("parquet").save("/home/vagrant/srajulu/ITMD-521/assignment-01/example-data/divy-2015.parquet")
    parquet_file = spark.read.format("parquet").load("/home/vagrant/srajulu/ITMD-521/assignment-01/example-data/divy-2015")
    parquet_file.show(n=10, truncate=False)

## Programmatically creating and attaching a schema using StructFields

    struct_schema = StructType([StructField("trip_id", IntegerType()),
        StructField("starttime", StringType()),
        StructField("stoptime", StringType()),
        StructField("bikeid", IntegerType()),
        StructField("tripduration", IntegerType()),
        StructField("from_station_id", IntegerType()),
        StructField("from_station_name", StringType()),
        StructField("to_station_id", IntegerType()),
        StructField("to_station_name", StringType()),
        StructField("usertype", StringType()),
        StructField("gender", StringType()),
        StructField("birthyear", IntegerType())])

    struct_divvy_df = (spark.read.schema(struct_schema).format("csv")).option("header","true").option("structureSchema","true").load(data_source)
    struct_divvy_df.show()
    struct_divvy_df.printSchema()
    

## Attaching a schema via a DDL

    ddl_schema =  "trip_id INT,starttime STRING,stoptime STRING,bikeid INT,tripduration INT,from_station_id INT,from_station_name STRING,to_station_id INT,to_station_name STRING,usertype STRING,gender STRING,birthyear INT"
    ddl_df = (spark.read.schema(ddl_schema).format("csv")).option("header", "true").load(data_source)
    ddl_df.show()
    ddl_df.printSchema()

## Select

    select_gender_df = (infer_divvy_df.select("gender", "to_station_id", "to_station_name").where(infer_divvy_df.gender == 'Male').groupBy("to_station_id").count())
    select_gender_df.show(n=10, truncate=False)