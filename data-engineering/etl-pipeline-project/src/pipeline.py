from loguru import logger
from extractor import extract
from transformer import transform
from loader import load
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(__file__))

# Log to file
os.makedirs("logs", exist_ok=True)
logger.add("logs/pipeline_{time:YYYY-MM-DD}.log", rotation="1 day", retention="7 days")

def run_pipeline():
    logger.info("=" * 50)
    logger.info("ETL PIPELINE STARTED")
    logger.info("=" * 50)

    # Step 1: Extract
    logger.info("STEP 1: EXTRACT")
    data = extract()
    if data is None:
        logger.error("Extraction failed! Stopping pipeline.")
        return False

    # Step 2: Transform
    logger.info("STEP 2: TRANSFORM")
    df = transform()
    if df is None or len(df) == 0:
        logger.error("Transformation failed! Stopping pipeline.")
        return False

    # Step 3: Load
    logger.info("STEP 3: LOAD")
    load()

    logger.info("=" * 50)
    logger.success("ETL PIPELINE COMPLETED SUCCESSFULLY")
    logger.info("=" * 50)
    return True

if __name__ == "__main__":
    run_pipeline()