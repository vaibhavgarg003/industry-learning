import pandas as pd
from sqlalchemy import create_engine
from loguru import logger

PROCESSED_DATA_PATH = "data/processed_countries.csv"
DATABASE_PATH = "data/countries.db"

def load():
    logger.info("Starting loading phase...")

    # Read transformed data
    df = pd.read_csv(PROCESSED_DATA_PATH)
    logger.info(f"Loaded {len(df)} rows from {PROCESSED_DATA_PATH}")

    # Create SQLite database engine
    engine = create_engine(f"sqlite:///{DATABASE_PATH}")

    # Load into database
    df.to_sql(
        name="countries",
        con=engine,
        if_exists="replace",
        index=False
    )

    logger.success(f"Loaded {len(df)} countries into {DATABASE_PATH} -> table: countries")

if __name__ == "__main__":
    load()