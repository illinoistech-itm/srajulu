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

# Q2 - Display all of the longest flights were between Honolulu (HNL) and New York (JFK). 
# find all flights between San Francisco (SFO) and Chicago (ORD) with at least a two-hour delay

    Q2 = spark.sql("""SELECT date, delay, origin, destination FROM us_delay_flights_tbl WHERE delay > 120 AND ORIGIN = 'SFO' AND DESTINATION = 'ORD' ORDER by delay DESC""")
    Q2.show(10)

# Q3 - Query to use the CASE clause. to label all US flights, regardless of origin and destination, 
# Very Long Delays (> 6 hours), Long Delays (2–6 hours), etc. add these human-readable labels in a new column called Flight_Delays

    Q3 =spark.sql("""SELECT delay, origin, destination,
              CASE
                  WHEN delay > 360 THEN 'Very Long Delays'
                  WHEN delay > 120 AND delay < 360 THEN 'Long Delays'
                  WHEN delay > 60 AND delay < 120 THEN 'Short Delays'
                  WHEN delay > 0 and delay < 60  THEN  'Tolerable Delays'
                  WHEN delay = 0 THEN 'No Delays'
                  ELSE 'Early'
               END AS Flight_Delays
               FROM us_delay_flights_tbl
               ORDER BY origin, delay DESC""")
    Q3.show(10)

#Part 2
# Converting Spark SQL queries queries in DataFrame API 

# Q1
DF_Q1 = (data_source.select("distance", "origin", "destination").where(col("distance") > 1000).orderBy(desc("distance")))
DF_Q1.show(10)

# Q2
DF_Q2 = (data_source.select("date","delay","origin","destination").where((col("delay") > 120) & (col("origin") == 'SFO') & (col("destination") == 'ORD')).orderBy(desc("delay")))
DF_Q2.show(10)

# Q3
DF_Q3 = (data_source.select("delay","origin","destination",expr("CASE WHEN delay > 360 THEN 'Very Long Delays' WHEN delay > 120 AND delay < 360 THEN 'Long Delays' WHEN delay > 60 AND delay < 120 THEN 'Short Delays' WHEN delay > 0 and delay < 60  THEN 'Tolerable Delays' WHEN delay = 0 THEN 'No Delays' ELSE 'Early' END AS Flight_Delays"))).orderBy(("origin"),(desc("delay")))
DF_Q3.show(10)

#Creating DB and  managed Tables
spark.sql("CREATE DATABASE SGR_SPARK_DB")
spark.sql("USE SGR_SPARK_DB")
sgr_db_schema="date STRING, delay INT, distance INT, origin STRING, destination STRING" 
flights_df = spark.read.csv(data_file, schema=sgr_db_schema) 
flights_df.write.saveAsTable("us_delay_flights_tbl")
ORD_DF = spark.sql("SELECT date, delay, origin, destination FROM us_delay_flights_tbl  WHERE origin = 'ORD'")
#ORD_DF.show(5)
ORD_DF.createOrReplaceTempView("view_ord_us_delay_flights_tbl")
