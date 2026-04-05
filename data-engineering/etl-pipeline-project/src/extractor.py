import requests
import json
import os
from loguru import logger

API_URL = "https://restcountries.com/v3.1/independent?status=true"
RAW_DATA_PATH = "data/raw_countries.json"

def extract():
    logger.info("Starting extraction from REST Countries API...")
    
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        data = response.json()
        
        os.makedirs("data", exist_ok=True)
        with open(RAW_DATA_PATH, "w") as f:
            json.dump(data, f)
        
        logger.success(f"Extracted {len(data)} countries and saved to {RAW_DATA_PATH}")
        return data
    else:
        logger.error(f"Failed to fetch data. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    extract()