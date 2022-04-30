from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import to_date
from pyspark.sql.functions import *
from pyspark.sql.types import StructType
from pyspark.sql.types import *

# Removing hard coded password - using os module to import them
import os
import sys

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usage: json-read-part-two.py <file> ", file=sys.stderr)
        sys.exit(-1)

    conf = SparkConf()
    conf.set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.2.0')
    conf.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider')
    
    conf.set('spark.hadoop.fs.s3a.access.key', os.getenv('SECRETKEY'))
    conf.set('spark.hadoop.fs.s3a.secret.key', os.getenv('ACCESSKEY'))
    conf.set("spark.hadoop.fs.s3a.endpoint", "http://192.168.172.50:9000")


    spark = SparkSession.builder.appName("json read Part2").config('spark.driver.host','192.168.172.45').config(conf=conf).getOrCreate()
    

    json_file_80 = "s3a://srajulu/80.json"
    
    spark.sql("set spark.sql.legacy.timeParserPolicy=LEGACY")    
    file_scehma =  StructType([StructField('WeatherStation', StringType(), True),
                    StructField('WBAN', StringType(), True),
                    StructField('ObservationDate', DateType(), True),
                    StructField('ObservationHour', IntegerType(), True),
                    StructField('Latitude', DoubleType(), True),
                    StructField('Longitude', DoubleType(), True),
                    StructField('Elevation', IntegerType(), True),
                    StructField('WindDirection', IntegerType(), True),
                    StructField('WDQualityCode', IntegerType(), True),
                    StructField('SkyCeilingHeight', IntegerType(), True),
                    StructField('SCQualityCode', IntegerType(), True),
                    StructField('VisibilityDistance', IntegerType(), True),
                    StructField('VDQualityCode', IntegerType(), True),
                    StructField('AirTemperature', FloatType(), True),
                    StructField('ATQualityCode', FloatType(), True),
                    StructField('DewPoint', FloatType(), True),
                    StructField('DPQualityCode', DoubleType(), True),
                    StructField('AtmosphericPressure', FloatType(), True)])
    

    json_df = spark.read.json(json_file_80,schema=file_scehma)
     
    json_df.show(10)
    json_df.printSchema()