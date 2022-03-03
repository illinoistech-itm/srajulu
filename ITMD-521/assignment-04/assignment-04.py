from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark import *

spark = SparkSession\
.builder\
.master('local[*]')\
.appName('Assignment04')\
.config('spark.driver.extraClassPath', '/home/vagrant/spark/jars/mysql-connector-java-8.0.28.jar')\
.getOrCreate()

JDBC_DF_TEMP = spark.read.format("jdbc").option("url","jdbc:mysql://localhost/employees").option("driver","com.mysql.jdbc.Driver").option("dbtable","employees").option("user","worker").option("password","cluster").load().createOrReplaceTempView("Employees")
JDBC_DF = spark.read.format("jdbc").option("url","jdbc:mysql://localhost/employees").option("driver","com.mysql.jdbc.Driver").option("dbtable","employees").option("user","worker").option("password","cluster").load()
JDBC_DF.show()
#Assignment Part 1
# Q1 - Display the count of the number of records in the DF
Q1_DF=spark.sql("Select count(*) from Employees")
Q1_DF.show()

# Q2 - Display the schema of the Employees Table from the DF
JDBC_DF.printSchema()

# Q3 - Create a DataFrame of the top 10,000 employee salaries (sort DESC) from the salaries table
Q3 = spark.read.format("jdbc")\
.option("url","jdbc:mysql://localhost/employees")\
.option("driver","com.mysql.jdbc.Driver")\
.option("dbtable","salaries")\
.option("user","worker")\
.option("password","cluster").load().createOrReplaceTempView("Salaries")
spark.read.table("Salaries").show(5)
Salary_DF = spark.sql("SELECT * from Salaries order by salary DESC limit 10000")

Salary_DF.write.format("jdbc")\
  .option("url", "jdbc:mysql://localhost/employees")\
  .option("driver","com.mysql.jdbc.Driver")\
  .option("dbtable", "salaries")\
  .option("user", "worker")\
  .option("password", "cluster")\
  .save()

Salary_DF.write.format("csv").save("salaries.parquet")

#Assignment Part 2
# Q4
Q4_DF = spark.read.format("jdbc")\
.option("url","jdbc:mysql://localhost/employees")\
.option("driver","com.mysql.jdbc.Driver")\
.option("query","select * from titles where title = 'Senior Engineer' ")\
.option("user","worker")\
.option("password","cluster").load().show()