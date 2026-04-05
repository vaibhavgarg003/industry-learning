import pytest
import sqlite3
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from extractor import extract
from transformer import transform
from loader import load

# Run extract and transform first so loader has data to work with
def setup_module(module):
    """Run extractor and transformer before loader tests"""
    extract()
    transform()

def test_loader_creates_database():
    """Test that database file is created"""
    load()
    assert os.path.exists("data/countries.db")

def test_loader_creates_table():
    """Test that countries table exists in database"""
    load()
    conn = sqlite3.connect("data/countries.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='countries'")
    result = cursor.fetchone()
    conn.close()
    assert result is not None

def test_loader_correct_row_count():
    """Test that database has at least 190 rows"""
    load()
    conn = sqlite3.connect("data/countries.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM countries")
    count = cursor.fetchone()[0]
    conn.close()
    assert count >= 190

def test_loader_has_correct_columns():
    """Test that all expected columns exist in database"""
    load()
    conn = sqlite3.connect("data/countries.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(countries)")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()
    expected = ['country', 'capital', 'region', 'subregion', 'population', 'area_km2', 'population_density']
    for col in expected:
        assert col in columns, f"Missing column: {col}"

def test_loader_no_duplicate_countries():
    """Test that there are no duplicate country names"""
    load()
    conn = sqlite3.connect("data/countries.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT country) FROM countries")
    distinct = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM countries")
    total = cursor.fetchone()[0]
    conn.close()
    assert distinct == total