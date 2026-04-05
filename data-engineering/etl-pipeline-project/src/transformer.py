import pandas as pd
import os
from loguru import logger

RAW_DATA_PATH = "data/raw_countries.json"
PROCESSED_DATA_PATH = "data/processed_countries.csv"

def transform():
    logger.info("Starting transformation...")

    df = pd.read_json(RAW_DATA_PATH)

    logger.info(f"Raw data shape: {df.shape}")

    # Extract only the fields we need
    transformed = pd.DataFrame()
    transformed['country']    = df['name'].apply(lambda x: x.get('common') if isinstance(x, dict) else None)
    transformed['capital']    = df['capital'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None)
    transformed['region']     = df['region']
    transformed['subregion']  = df['subregion']
    transformed['population'] = df['population']
    transformed['area_km2']   = df['area']

    # Handle nulls
    transformed.dropna(subset=['country', 'population', 'area_km2'], inplace=True)

    # Add calculated column
    transformed['population_density'] = (transformed['population'] / transformed['area_km2']).round(2)

    # Sort by population descending
    transformed.sort_values('population', ascending=False, inplace=True)
    transformed.reset_index(drop=True, inplace=True)

    os.makedirs("data", exist_ok=True)
    transformed.to_csv(PROCESSED_DATA_PATH, index=False)

    logger.success(f"Transformed {len(transformed)} countries and saved to {PROCESSED_DATA_PATH}")
    return transformed

if __name__ == "__main__":
    df = transform()
    print(df.head(10))