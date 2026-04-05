import pytest
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from extractor import extract

def test_extract_returns_data():
    """Test that extractor returns a list of countries"""
    data = extract()
    assert data is not None
    assert isinstance(data, list)

def test_extract_country_count():
    """Test that we get at least 190 countries"""
    data = extract()
    assert len(data) >= 190

def test_extract_saves_file():
    """Test that raw JSON file is saved to disk"""
    extract()
    assert os.path.exists("data/raw_countries.json")

def test_extract_country_has_name():
    """Test that each country has a name field"""
    data = extract()
    for country in data[:5]:
        assert "name" in country
        assert "common" in country["name"]