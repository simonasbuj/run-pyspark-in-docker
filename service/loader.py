from pyspark.sql import SparkSession
from pyspark.sql.types import DecimalType
from pyspark.sql.functions import col
import pandas as pd

from .utils import logs
import time 

class Loader:

    def __init__(self):
        self.spark = self._setup_spark("FAKE")
        self.log = logs.setup_logging(
            logs_output_file = "logs/logs.txt",
            logger_name = f"{self.__class__.__name__} from {__name__}"
        )
        # time.sleep(1000)

    def _setup_spark(self, config):
        return (
            SparkSession.builder
            .appName("Spark Loader App")
            .config("spark.jars", "host_input/jars/postgresql-42.7.1.jar") 
            .config("spark.executor.extraClassPath", "host_input/jars/postgresql-42.7.1.jar")          
            .getOrCreate()
        )

    def load(self):
        print("starting loading")
        self.log.info("STARTING LOADING")
        self.log.info(self.spark)

        input_df = self.spark.read.csv("host_input/input_data.csv", header=True)
        df = input_df.withColumn("cool_stars", col("cool_stars").cast(DecimalType(2, 1)))
        df.show()
        df.printSchema()

        # self.export_to_excel(df, "host_output/results.xlsx")

        self.load_to_postgres(df)
        self.log.info("LOADING FINISHED. sb")
    
    def export_to_excel(self, spark_df, output_path):
        self.log.info("Starting exporting to excel")
        pandas_df = spark_df.toPandas()
        pandas_df.to_excel(output_path)
        self.log.info("Finished exporting to excel")


    def load_to_postgres(self, df):
        self.log.info("STARTING LOADING TO POSTGRES")

        conn_url = f'jdbc:postgresql://host.docker.internal:5432/mydb'
        (
            df.write
            .format("jdbc")
            .option("url", conn_url)
            .option("driver", "org.postgresql.Driver")
            .option("dbtable", "spark_table")
            .option("user", "postgres").option("password", "password")
            .mode("append")
            .save()
        )
        
        # .jdbc(url=conn_url, table="spark_table", mode="overwrite")

        self.log.info("FINISHED LOADING TO POSTGRES")
        


    