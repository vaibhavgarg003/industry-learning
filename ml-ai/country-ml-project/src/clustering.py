import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import joblib
import os
# Build absolute paths
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SRC_DIR)
ML_DIR = os.path.dirname(PROJECT_DIR)
REPO_DIR = os.path.dirname(ML_DIR)

DATA_PATH = os.path.join(REPO_DIR, "data-engineering", "etl-pipeline-project", "data", "processed_countries.csv")
MODEL_PATH = os.path.join(PROJECT_DIR, "models", "kmeans_model.pkl")

def load_data():
    df = pd.read_csv(DATA_PATH)
    return df

def prepare_features(df):
    features = df[['population', 'area_km2', 'population_density']].copy()
    features['population']= np.log1p(features['population'])
    features['area_km2']= np.log1p(features['area_km2'])
    features['population_density']= np.log1p(features['population_density'])
    return features

def train_clustering(df, n_clusters=4):
    features = prepare_features(df)
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(scaled_features)
    os.makedirs("models", exist_ok=True)
    joblib.dump(kmeans, MODEL_PATH)
    joblib.dump(scaler, MODEL_PATH.replace('.pkl', '_scaler.pkl'))
    
    return df, kmeans, scaler
    

def print_cluster_summary(df):
    print("Countries per cluster:")
    print(df['cluster'].value_counts().sort_index())
    print("\nSample countries in each cluster:")
    for cluster in sorted(df['cluster'].unique()):
        countries = df[df['cluster'] == cluster]['country'].head(5).tolist()
        print(f"\nCluster {cluster}: {countries}")


if __name__ == "__main__":
    df = load_data()
    df, kmeans, scaler = train_clustering(df)
    print_cluster_summary(df)