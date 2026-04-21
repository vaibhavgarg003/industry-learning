import os 
os.environ["PYSPARK_PYTHON"] = "python3"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python3"

from pyspark.sql import SparkSession
from loguru import logger
from pyspark.sql.functions import col, when, hour, to_timestamp, round as spark_round
from data_generator import generate_atm_transactions


logger.add("../logs/pipeline.log", rotation="1 MB", retention="7 days")

##SPARK SESSION
logger.info("Initializing Spark Session")
spark = SparkSession.builder  \
    .appName("ATM Analytics Pipeline") \
    .master("local[*]") \
    .config("spark.driver.host", "localhost") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

logger.success("Spark Session initialized successfully")


print("=" * 50)
print("ATM Analytics Pipeline")
print("=" * 50)

logger.info("Generating ATM Transaction data")
data = generate_atm_transactions(10000)

df = spark.createDataFrame(data)

df = df.repartition(4)  # Repartition to 4 partitions for better performance
print(f"\nTotal records ingested: {df.count()}")

logger.success(f"Ingested {df.count()} records into Spark DataFrame")



##Transformations
logger.info ("Applying Transformations")
df = df.withColumn("Timestamp", to_timestamp(col("Timestamp"), "yyyy-MM-dd HH:mm:ss"))

df = df.withColumn("Hour", hour(col("Timestamp")))

df = df.withColumn("TimeBucket", when((col("Hour") >=6) & (col("Hour") < 12), "Morning")
                                .when((col("Hour") >=12) & (col("Hour") < 18), "Afternoon")
                                .when((col("Hour") >=18) & (col("Hour") < 24), "Evening")
                                .otherwise("Night"))

df = df.withColumn("IsHighValue", when(col("Amount") > 500, True).otherwise(False))

df = df.withColumn("Amount", spark_round(col("Amount"), 2))
logger.success("Transformations applied successfully")
df.printSchema()

df.show(10)


##Analytics
logger.info("Running Analytics")

logger.info(" Status distribution:")
df.groupBy("Status").count().orderBy("count", ascending=False).show()

logger.info("Transaction by City:")
df.groupBy("City").count().orderBy("count", ascending=False).show()

logger.info("Transaction by Time Bucket:")
df.groupBy("TimeBucket").count().orderBy("count", ascending=False).show()

logger.info("High-Value Transactions:")
df.groupBy("IsHighValue").count().show()


# Save to Parquet — columnar format used in production
output_path = "../data/atm_transactions.parquet"
logger.info(f"Saving data to Parquet: {output_path}")
df.write.mode("overwrite").parquet(output_path)
logger.success(f"Data saved to Parquet: {output_path}")

# Read it back to confirm
df_loaded = spark.read.parquet(output_path)
logger.info(f"Records loaded back from Parquet: {df_loaded.count()}")

spark.stop()