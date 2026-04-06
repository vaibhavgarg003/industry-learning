markdown# Country ML Project 🤖

A machine learning project built on top of the ETL pipeline's cleaned country data.

---

## 🎯 What This Project Does

Uses real-world country data (195 countries) to:
- **Cluster** similar countries together using K-Means (Unsupervised Learning)
- **Predict** population density using Linear Regression (Supervised Learning)

---

## 🔗 Data Source

Data comes from the ETL pipeline in this same repo:
`data-engineering/etl-pipeline-project/data/processed_countries.csv`

This is intentional — the ETL pipeline's job is to get and clean data.
The ML project's job is to learn from it.

---

## 📁 Project Structure
country-ml-project/
├── src/
│   ├── data_loader.py      # Reads data from ETL pipeline output
│   ├── clustering.py       # K-Means clustering
│   └── prediction.py       # Linear Regression model
├── notebooks/
│   └── exploration.ipynb   # Data exploration and visualisations
├── models/
│   └── density_model.pkl   # Saved trained model
├── tests/
│   └── test_models.py      # Unit tests
└── requirements.txt

---

## ⚙️ Tech Stack

Python · Scikit-learn · Pandas · Matplotlib · Seaborn · Joblib · Jupyter

---

## 🔜 Status

🚧 In Progress