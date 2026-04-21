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
        .master("local[2]") \
        .config("spark.driver.host", "localhost") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("Error")
    yield spark
    spark.stop()

@pytest.fixture(scope="session")
def sample_df(spark):
    data = [
        {"TransactionID": "TXN001", "ATMID": "ATM001", "City": "Hyderabad",
         "TransactionType": "Withdrawal", "Amount": 800.0,
         "Status": "Success", "Timestamp": "2024-01-15 09:30:00"},
        {"TransactionID": "TXN002", "ATMID": "ATM002", "City": "Mumbai",
         "TransactionType": "Balance Inquiry", "Amount": 0.0,
         "Status": "Failed", "Timestamp": "2024-01-15 14:00:00"},
        {"TransactionID": "TXN003", "ATMID": "ATM003", "City": "Delhi",
         "TransactionType": "Deposit", "Amount": 300.0,
         "Status": "Success", "Timestamp": "2024-01-15 22:00:00"},
        {"TransactionID": "TXN004", "ATMID": "ATM004", "City": "Chennai",
         "TransactionType": "Withdrawal", "Amount": 600.0,
         "Status": "Success", "Timestamp": "2024-01-15 03:00:00"},
    ]
    return spark.createDataFrame(data)

def test_dataframe_has_correct_columns(sample_df):
    expected = {"TransactionID", "ATMID", "City", "TransactionType", "Amount", "Status", "Timestamp"}
    assert expected.issubset(set(sample_df.columns))

def test_dataframe_is_double(sample_df):
    amount_type = dict(sample_df.types)["Amount"]
    assert amount_type == "double"

def test_dataframe_is_double(sample_df):
    assert sample_df.count() == 4

# ── TRANSFORMATION TESTS ───────────────────────────

def test_timestamp_cast(sample_df):
    df = sample_df.withColumn("Timestamp",
        to_timestamp(col("Timestamp"), "yyyy-MM-dd HH:mm:ss"))
    assert dict(df.dtypes)["Timestamp"] == "timestamp"

def test_hour_extraction(sample_df):
    df = sample_df.withColumn("Timestamp",
        to_timestamp(col("Timestamp"), "yyyy-MM-dd HH:mm:ss"))
    df = df.withColumn("Hour", hour(col("Timestamp")))
    hours = [r["Hour"] for r in df.collect()]
    assert 9 in hours
    assert 14 in hours

def test_high_value_flag_true(sample_df):
    df = sample_df.withColumn("IsHighValue",
        when(col("Amount") > 500, True).otherwise(False))
    high_value = df.filter(col("IsHighValue") == True).count()
    assert high_value == 2  # TXN001=800, TXN004=600

def test_high_value_flag_false(sample_df):
    df = sample_df.withColumn("IsHighValue",
        when(col("Amount") > 500, True).otherwise(False))
    low_value = df.filter(col("IsHighValue") == False).count()
    assert low_value == 2  # TXN002=0, TXN003=300

def test_time_bucket_morning(sample_df):
    df = sample_df.withColumn("Timestamp",
        to_timestamp(col("Timestamp"), "yyyy-MM-dd HH:mm:ss"))
    df = df.withColumn("Hour", hour(col("Timestamp")))
    df = df.withColumn("TimeBucket",
        when((col("Hour") >= 6) & (col("Hour") < 12), "Morning")
        .when((col("Hour") >= 12) & (col("Hour") < 17), "Afternoon")
        .when((col("Hour") >= 17) & (col("Hour") < 21), "Evening")
        .otherwise("Night"))
    morning = df.filter(col("TimeBucket") == "Morning").count()
    assert morning == 1  # only TXN001 at 09:30

def test_time_bucket_night(sample_df):
    df = sample_df.withColumn("Timestamp",
        to_timestamp(col("Timestamp"), "yyyy-MM-dd HH:mm:ss"))
    df = df.withColumn("Hour", hour(col("Timestamp")))
    df = df.withColumn("TimeBucket",
        when((col("Hour") >= 6) & (col("Hour") < 12), "Morning")
        .when((col("Hour") >= 12) & (col("Hour") < 17), "Afternoon")
        .when((col("Hour") >= 17) & (col("Hour") < 21), "Evening")
        .otherwise("Night"))
    night = df.filter(col("TimeBucket") == "Night").count()
    assert night == 2  # TXN003 at 22:00, TXN004 at 03:00

# ── ANALYTICS TESTS ────────────────────────────────

def test_status_groupby(sample_df):
    result = sample_df.groupBy("Status").count()
    assert result.count() == 2  # Success and Failed

def test_city_groupby(sample_df):
    result = sample_df.groupBy("City").count()
    assert result.count() == 4  # 4 unique cities

def test_no_null_transaction_ids(sample_df):
    nulls = sample_df.filter(col("TransactionID").isNull()).count()
    assert nulls == 0

def test_balance_inquiry_amount_is_zero(sample_df):
    df = sample_df.filter(col("TransactionType") == "Balance Inquiry")
    non_zero = df.filter(col("Amount") != 0.0).count()
    assert non_zero == 0