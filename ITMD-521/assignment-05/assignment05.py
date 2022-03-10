from select import select
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import expr
from pyspark.sql.functions import split, col

spark = SparkSession\
.builder\
.master('local[*]')\
.appName('Assignment05')\
.config('spark.driver.extraClassPath', '/home/vagrant/spark/mysql-connector-java-8.0.28.jar')\
.getOrCreate()