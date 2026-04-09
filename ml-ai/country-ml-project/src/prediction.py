import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings("ignore")


##Build absolute paths
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SRC_DIR)
ML_DIR = os.path.join(PROJECT_DIR)
REPO_DIR = os.path.dirname(ML_DIR)

DATA_PATH = os.path.join(REPO_DIR, "../data-engineering",
                         "etl-pipeline-project", "data",
                         "processed_countries.csv")

def load_data():
    df = pd.read_csv(DATA_PATH)
    return df

def prepare_features(df):
    """
    Prepare features for prediction.
    Note : we exclude population to avoid data leakage
    since population_density = population / area_km2
    """
    
    le_region = LabelEncoder()
    le_subregion = LabelEncoder()
    
    X= df[['area_km2', 'region', 'subregion']].copy()
    y = df['population_density']
    
    X['region'] = le_region.fit_transform(X['region'])
    X['subregion'] = le_subregion.fit_transform(X['subregion'])
    X['area_km2'] = np.log1p(X['area_km2'])
    y_log = np.log1p(y)

    return X, y_log

def train_linear_regression(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def train_random_forest(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test, model_name):
    y_pred_log = model.predict(X_test)
    y_pred = np.expm1(y_pred_log)
    y_actual = np.expm1(y_test)

    mae = mean_absolute_error(y_actual, y_pred)
    r2 = r2_score(y_actual, y_pred)

    print(f"\n{model_name} Results:")
    print(f"Mean Absolute Error: {mae:.2f}")
    print(f"R^2 Score: {r2:.2f}")
    return mae, r2


def run_prediction():
    print("Loading data...")
    df = load_data()

    print("Preparing features...")
    X, y = prepare_features(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    lr_model = train_linear_regression(X_train, y_train)
    evaluate_model(lr_model, X_test, y_test, "Linear Regression")

    rf_model = train_random_forest(X_train, y_train)
    evaluate_model(rf_model, X_test, y_test, "Random Forest Regressor")

    print("\n Note:Low R^2 scores are expected due to the limited features used for prediction. The models are primarily capturing the relationship between area and population density, while other factors influencing population density are not included in the dataset.    ")
    print("Dataset has only 195 rows - too small for reliable prediction")
    print("Ara and region alone are weak predictors of density")
    print("This is documented as key learning outcome")


if __name__ == "__main__":
    run_prediction()

    