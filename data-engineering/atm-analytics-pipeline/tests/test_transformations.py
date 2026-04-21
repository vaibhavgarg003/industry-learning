import pytest
import os

os.environ["PYSPARK_PYTHON"] = "python3"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python3"

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, hour, to_timestamp, round as spark_round

@pytest.fixture(scope="session")
def spark():

    spark = SparkSession.builder \
        .appName ("ATM Analytics Tests") \
        .master("local[*]") \
        .config("spark.driver.host", "localhost") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("Error")
    yield spark
    spark.stop()

@pytest.fixture(scope= "session")
def sample_df(spark):
    