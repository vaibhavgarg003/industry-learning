import sqlite3
import pandas as pd

conn = sqlite3.connect("data/countries.db")

# Query top 10 most populous countries
df = pd.read_sql_query("""
    SELECT country, population, area_km2, population_density, region
    FROM countries
    ORDER BY population DESC
    LIMIT 10
""", conn)

print("Top 10 Most Populous Countries:")
print(df.to_string(index=False))

conn.close()