from calendar import month
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import year
from pyspark.sql.functions import *
from pyspark.sql.functions import to_timestamp
from pyspark.sql.functions import to_date
from pyspark.sql.functions import col
from pyspark.sql.functions import weekofyear

spark = SparkSession.builder.appName("Assignment02").getOrCreate()


# Defining the schema 
struct_schema = StructType([StructField('CallNumber', IntegerType(), True),
                    StructField('UnitID', StringType(), True),
                    StructField('IncidentNumber', IntegerType(), True),
                    StructField('CallType', StringType(), True),
                    StructField('CallDate', StringType(), True),
                    StructField('WatchDate', StringType(), True),
                    StructField('CallFinalDisposition', StringType(), True),
                    StructField('AvailableDtTm', StringType(), True),
                    StructField('Address', StringType(), True),
                    StructField('City', StringType(), True),
                    StructField('Zipcode', IntegerType(), True),
                    StructField('Battalion', StringType(), True),
                    StructField('StationArea', StringType(), True),
                    StructField('Box', StringType(), True),
                    StructField('OriginalPriority', StringType(), True),
                    StructField('Priority', StringType(), True),
                    StructField('FinalPriority', IntegerType(), True),
                    StructField('ALSUnit', BooleanType(), True),
                    StructField('CallTypeGroup', StringType(), True),
                    StructField('NumAlarms', IntegerType(), True),
                    StructField('UnitType', StringType(), True),
                    StructField('UnitSequenceInCallDispatch', IntegerType(), True),
                    StructField('FirePreventionDistrict', StringType(), True),
                    StructField('SupervisorDistrict', StringType(), True),
                    StructField('Neighborhood', StringType(), True),
                    StructField('Location', StringType(), True),
                    StructField('RowID', StringType(), True),
                    StructField('Delay', FloatType(), True)])

# Reading from CSV file
if __name__ == "__main__":
    data_source = spark.read.format("csv").option("header","True").schema(struct_schema).load("/home/vagrant/srajulu/ITMD-521/assignment-02/sf-fire-calls.csv")
    data_source.show(30)

# Q1 - What were all the different types of fire calls in 2018?
q1_call_df = data_source.select('CallType').groupBy('CallType').count().orderBy("count", ascending=False)
q1_call_df.show()
rename_fire_df = data_source.withColumnRenamed("Delay", "ResponseDelayedinMins")
diff_fire_calls_df = (rename_fire_df.withColumn("IncidentDate", to_timestamp(col("CallDate"), "MM/dd/yyyy")).drop("CallDate"))

# Q2 - What months within the year 2018 saw the highest number of fire calls?
diff_fire_calls_df.filter(year('IncidentDate') == 2018).groupBy(month('IncidentDate')).count().orderBy('count', ascending=False).show()

# Q3 - Which neighborhood in San Francisco generated the most fire calls in 2018? 
diff_fire_calls_df.select("Neighborhood","IncidentDate","City").filter(col("City") == 'San Francisco').filter(year("IncidentDate") == 2018).groupBy(col("Neighborhood"),col("City")).count().orderBy('count', ascending=False).show()

# Q4 - Which neighborhoods had the worst response times to fire calls in 2018? (To check the issue)
diff_fire_calls_df.select("Neighborhood", "ResponseDelayedinMins","IncidentDate").filter(year("IncidentDate"))

# Q5 - Which week in the year in 2018 had the most fire calls?
diff_fire_calls_df.filter(year('IncidentDate') == 2018).groupBy(weekofyear('IncidentDate')).count().orderBy('count', ascending=False).show()
