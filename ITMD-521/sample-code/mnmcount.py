from os import truncate
import sys


import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import count

if __name__ == "main":
    if len(sys.argv) != 2:
        print("Usage: mnmcount <fiel>", file=sys.stderr)
        sys.exit(-1)

    spark = (SparkSession.builder.appName("SGR_Python_MnM Count").getOrCreate())

    mnm_file = sys.argv[1]

    mnm_df = (spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(mnm_file))

    count_mnm_df = (mnm_df.select("State", "Color", "Count").groupBy("State", "Color").sum("Count").orderBy("sum(Count)",ascending=False))

    count_mnm_df.show(n=60, truncate=False)
    print("Total rows= %d " % (count_mnm_df.count()))

    ca_count_mnm_df = (mnm_df.select("State", "Color", "Count").where(mnm_df.State == "CA").groupBy("Sate", "Color").sum("Count").orderBy("sum(Count)", ascending=False))

    ca_count_mnm_df.show(n=10, truncate=False)

    spark.stop()


