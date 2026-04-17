import boto3
import os
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

PROCESSED_DATA_PATH = os.getenv("PROCESSED_DATA_PATH", "data/processed_countries.csv")
S3_KEY = "countries/processed_countries.csv"

def upload_to_s3():
    logger.info("Starting S3 upload...")

    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

    s3.upload_file(
        PROCESSED_DATA_PATH,
        AWS_BUCKET_NAME,
        S3_KEY
    )

    logger.success(f"Uploaded {PROCESSED_DATA_PATH} to s3://{AWS_BUCKET_NAME}/{S3_KEY}")

if __name__ == "__main__":
    upload_to_s3()