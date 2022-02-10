package main.scala.assignment
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._


object assignment{
def main(args: Array[String]) {
     val spark = SparkSession.builder.appName("Assignment1").getOrCreate()
     if (args.length < 1) {
     print("Usage: DivvySet <Divvy_file_dataset>") 
     sys.exit(1)
     }

     val data_source = args(0)
     val infer_divvy_df = spark.read.format("csv") .option("header", "true") .option("inferSchema", "true") .load(data_source)
     infer_divvy_df.show(20)
     infer_divvy_df.printSchema()


     val struct_schema = StructType(Array(StructField("trip_id", IntegerType),
     StructField("starttime", StringType),
     StructField("stoptime", StringType),
     StructField("bikeid", IntegerType),
     StructField("tripduration", IntegerType),
     StructField("from_station_id", IntegerType),
     StructField("from_station_name", StringType),
     StructField("to_station_id", IntegerType),
     StructField("to_station_name", StringType),
     StructField("usertype", StringType),
     StructField("gender", StringType),
     StructField("birthyear", IntegerType)))

     val struct_divvy_df = spark.read.schema(struct_schema).format("csv").option("header", "true").option("structureSchema", "true").load(data_source)
     struct_divvy_df.show(10)
     struct_divvy_df.printSchema()


     val ddl_schema = "trip_id INT,starttime STRING,stoptime STRING,bikeid INT,tripduration INT,from_station_id INT,from_station_name STRING,to_station_id INT,to_station_name STRING,usertype STRING,gender STRING,birthyear INT"
     val ddl_df = (spark.read.schema(ddl_schema).format("csv")).option("header", "true").load(data_source)
     ddl_df.show()
     ddl_df.printSchema()


    val select_gender_df = (infer_divvy_df.select("gender", "to_station_id", "to_station_name", "Count").where(infer_divvy_df.gender == "Male").groupBy("to_station_id").sum("Count").orderBy(desc("sum(Count)"))
    select_gender_df.show(10, false)


     }
}