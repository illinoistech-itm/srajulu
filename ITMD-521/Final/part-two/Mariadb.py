from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark import SparkConf

import os
import sys

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usage: Mariadb.py <file> ", file=sys.stderr)
        sys.exit(-1)

    conf = SparkConf()
    conf.set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.2.0')
    conf.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider')
    
    conf.set('spark.hadoop.fs.s3a.access.key', os.getenv('SECRETKEY'))
    conf.set('spark.hadoop.fs.s3a.secret.key', os.getenv('ACCESSKEY'))
    conf.set("spark.hadoop.fs.s3a.endpoint", "http://192.168.172.50:9000")


    spark = SparkSession.builder.appName('MariaDbconnection').config('spark.driver.extraClassPath', '/home/srajulu/srajulu/mysql-connector-java-8.0.29/mysql-connector-java-8.0.29.jar').config('spark.driver.host','192.168.172.45').config(conf=conf).getOrCreate()


# Reading the ncdc database into a DataFrame refering the table name fifties #.option("dbtable","fifties")\

    df = spark.read.format("jdbc") \
    .option("url","jdbc:mysql://192.168.172.31:3306/ncdc")\
    .option("driver","com.mysql.cj.jdbc.Driver")\
    .option("dbtable","thirties")\
    .option("user","worker")\
    .option("password", "cluster").load()

   
    df.show(10)
    df.printSchema()
    