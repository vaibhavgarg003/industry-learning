import pytest
import pandas as pd
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from extractor import extract
from transformer import transform

# Run extract first so transformer has data to work with
def setup_module(module):
    """Run extractor before transformer tests"""
    extract()

def test_transform_returns_dataframe():
    """Test that transformer returns a pandas DataFrame"""
    df = transform()
    assert df is not None
    assert isinstance(df, pd.DataFrame)

def test_transform_has_correct_columns():
    """Test that all expected columns exist"""
    df = transform()
    expected_columns = ['country', 'capital', 'region', 'subregion', 'population', 'area_km2', 'population_density']
    for col in expected_columns:
        assert col in df.columns, f"Missing column: {col}"

def test_transform_no_null_countries():
    """Test that no country name is null"""
    df = transform()
    assert df['country'].isnull().sum() == 0

def test_transform_population_density_calculated():
    """Test that population density is correctly calculated"""
    df = transform()
    assert 'population_density' in df.columns
    assert df['population_density'].isnull().sum() == 0
    assert (df['population_density'] > 0).all()

def test_transform_sorted_by_population():
    """Test that data is sorted by population descending"""
    df = transform()
    assert df['population'].iloc[0] >= df['population'].iloc[1]

def test_transform_saves_csv():
    """Test that processed CSV file is saved to disk"""
    transform()
    assert os.path.exists("data/processed_countries.csv")