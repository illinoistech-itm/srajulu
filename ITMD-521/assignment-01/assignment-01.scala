package main.scala.assignment
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
/**
 * Usage: MnMcount <mnm_file_dataset>
 */
object assignment{
def main(args: Array[String]) {
     val spark = SparkSession.builder.appName("Assignment1").getOrCreate()
     if (args.length < 1) {
     print("Usage: DivvySet <Divvy_file_dataset>") 
     sys.exit(1)
     }

     val DivvyFile = args(0)
     val Infer_DF = spark.read.format("csv") .option("header", "true") .option("inferSchema", "true") .load(DivvyFile)
     Infer_DF.show(20)


}
}