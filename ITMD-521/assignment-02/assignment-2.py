from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

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
if __name__ == "_main_":
    data_source = spark.read.format("csv").option("header","True").schema(struct_schema).load("/home/vagrant/srajulu/ITMD-521/assignment-02/sf-fire-calls.csv")
    data_source.show(30)