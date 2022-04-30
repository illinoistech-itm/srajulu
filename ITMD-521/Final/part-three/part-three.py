from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import year
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import col
from pyspark.sql.functions import desc

import os
import sys

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usage: part-three.py <file> ", file=sys.stderr)
        sys.exit(-1)

    config = SparkConf()
    config.set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.2.0')
    config.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider')
    
    config.set('spark.hadoop.fs.s3a.access.key', os.getenv('SECRETKEY'))
    config.set('spark.hadoop.fs.s3a.secret.key', os.getenv('ACCESSKEY'))
    config.set("spark.hadoop.fs.s3a.endpoint", "http://192.168.172.50:9000")
   
