package main.scala.assignment02

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.SparkContext._
import org.apache.spark.sql._
import org.apache.spark.sql.types._

// Schema definition
case class Deviceiotdata(battery_level: Long, c02_level: Long, cca2: String, cca3: String, cn: String, device_id: Long, device_name: String, humidity: Long, ip: String, latitude: Double,lcd: String, longitude: Double, scale: String, temp: Long, timestamp: Long)

object assignment02 {
  def main(args: Array[String]) {

      val spark=(SparkSession.builder.appName("assignment02").getOrCreate())
        import spark.implicits._
        import spark.sql

      val data_source = spark.read.json("/home/vagrant/iot_devices.json").as[Deviceiotdata]
      data_source.show(10, false)

    //Q1 - Detect failing devices with battery levels below a threshold.
    val DStemp = data_source.select("*").where("battery_level < 5").as[Deviceiotdata]
    DStemp.show(5, false)

    //Q2 - Identify offending countries with high levels of CO2 emissions.
    val DStemp1 = data_source.select("c02_level","cn").distinct().orderBy(desc("c02_level"))
    //groupBy("c02_level","cca3").orderBy(desc("(c02_level)"))
    DStemp1.show(10, false)

    //Q3 - Compute the min and max values for temperature, battery level, CO2, and humidity.
    val temperature = data_source.columns(13)
    val min_max = data_source.agg(min(temperature), max(temperature))
    min_max.show()

  }
}