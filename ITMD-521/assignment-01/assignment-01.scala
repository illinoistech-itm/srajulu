package main.scala.assignment1 
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

object assignment {
    def main(args: Array[String]) {
    val spark = SparkSession .builder.appName("assignment1").getOrCreate()
    if (args.length < 1) {
        print("Usage: assignment1 <mnm_file_dataset>")
        sys.exit(1)
        }

    }
    val DivvyFile = args(0)

    val Infer_DF = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(DivvyFile)
    Infer_DF.show()
    Infer_DF.printSchema()
}