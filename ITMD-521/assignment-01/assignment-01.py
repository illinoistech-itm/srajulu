from __future__ import_function
from optparse import Option
from os import truncate
import sys

from pyspark.sql import SparkSession
from pyspark.sql.function import count
from pyspark.sql.types import *

if __name__ == "__main__":
    if len(sys.argv)!=2:
        print("Usage: DivvyTrips <file>", file=sys.stderr)
        sys.exit(-1)

    spark = (SparkSession.builder.appName("Assignment 1").getOrCreate())
    Divvy_File = sys.argv[1]

    infer_divvy_df = (spark.read.format("csv").option("header","true").option("inferSchema","true").load(Divvy_File))
    infer_divvy_df.show(n=10, truncate=False)
    infer_divvy_df.printSchema()