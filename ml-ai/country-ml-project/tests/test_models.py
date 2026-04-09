import pytest
import sys
import os
import numpy as np
import pandas as pd

SRC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src')
sys.path.insert(0, SRC_PATH)

from clustering import load_data, prepare_features, train_clustering, print_cluster_summary
from prediction import prepare_features as prep_pred_features, train_linear_regression, train_random_forest, evaluate_model
from sklearn.model_selection import train_test_split

def test_load_data_returns_dataframe():
    df = load_data()
    assert df is not None
    assert isinstance(df, pd.DataFrame), "load_data should return a pandas DataFrame"

def test_load_data_correct_shape():
    df = load_data()
    assert df.shape[0] >= 190
    assert df.shape[1] == 7

def test_load_data_no_nulls():
    df = load_data()
    assert df.isnull().sum().sum() == 0, "Data should not contain null values"

def test_load_data_correct_columns():
    df = load_data()
    expected = ['country', 'capital', 'region', 'subregion',
                'population', 'area_km2', 'population_density']
    
    for col in expected:
        assert col in df.columns

##clustering tests

def test_prepare_features_returns_correct_shape():
     df = load_data()
     features = prepare_features(df)
     assert features.shape[0] == df.shape[0]
     assert features.shape[1] == 3

def test_train_clustering_returns_clusters():
    df = load_data()
    df_clustered, kmeans,scaler = train_clustering(df)
    assert 'cluster' in df_clustered.columns
    assert df_clustered['cluster'].nunique() == 4

def test_train_clustering_no_nulls_in_clusters():
    df = load_data()
    df_clustered, kmeans, scaler = train_clustering(df)
    assert df_clustered['cluster'].isnull().sum() == 0


##prediction tests

def test_prepare_pred_features_correct_shape():
    df = load_data()
    X, y = prep_pred_features(df)
    assert 'area_km2' in X.columns
    assert 'region' in X.columns
    assert 'subregion' in X.columns
    assert len(y) == len(X)

def test_linear_regression_trains():
    df = load_data()
    X, y = prep_pred_features(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = train_linear_regression(X_train, y_train)
    assert model is not None

def test_random_forest_trains():
    df = load_data()
    X, y = prep_pred_features(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = train_random_forest(X_train, y_train)
    assert model is not None


