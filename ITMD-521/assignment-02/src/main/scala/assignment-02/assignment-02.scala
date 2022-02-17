package main.scala.assignment-02

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.SparkContext._
import org.apache.spark.sql._
import org.apache.spark.sql.types._

// Schema definition
case class Deviceiotdata(battery_level: Long, c02_level: Long, cca2: String, cca3: String, cn: String, device_id: Long, device_name: String, humidity: Long, ip: String, latitude: Double,lcd: String, longitude: Double, scale: String, temp: Long, timestamp: Long)

object assignment-02 {
  def main(args: Array[String]) {

      val spark=(SparkSession.builder.appName("assignment02").getOrCreate())
        import spark.implicits._
        import spark.sql

      val ds = spark.read.json("/home/vagrant/iot_devices.json").as[Deviceiotdata]
      ds.show(10, false)
  }
}