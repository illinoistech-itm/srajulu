from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import sys
from pyspark.sql.functions import col, desc
from pyspark.sql.functions import expr


spark = SparkSession.builder.appName("Assignment03").getOrCreate()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: Please input the file name and its path as an argument <file>", file=sys.stderr)
        sys.exit(-1)
    spark = (SparkSession.builder.appName("Assignment-03").getOrCreate())
    data_file = sys.argv[1]

    data_source = (spark.read.format("csv").option("header","True").option("inferschema", "True").load(data_file))
    data_source.createOrReplaceTempView("us_delay_flights_tbl")
    data_source.show(5)

#Part 1 
# Q1 - Find all flights whose distance is greater than 1,000 miles

    Q1 = spark.sql("""SELECT distance, origin, destination FROM us_delay_flights_tbl WHERE distance > 1000 ORDER BY distance DESC""")
    Q1.show(10)

