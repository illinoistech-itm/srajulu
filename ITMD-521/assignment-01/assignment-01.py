#from __future__ import function
#from optparse import Option
#from os import truncate
from os import truncate
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
    parquet_path = infer_divvy_df.write.format("parquet").save("/home/vagrant/srajulu/ITMD-521/assignment-01/example-data/divvy-2015-q1")
    parquet_file = spark.read.format("parquet").load("/home/vagrant/srajulu/ITMD-521/assignment-01/example-data/divvy-2015-q1")
    parquet_file.show(n=10, truncate=False)

## Programmatically creating and attaching a schema using StructFields