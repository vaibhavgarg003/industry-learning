# Country ML Project 🤖

A machine learning project built on top of the ETL pipeline's 
cleaned country data — exploring clustering and prediction 
on 195 countries.

---

## 🔗 Data Source

Data comes directly from our ETL pipeline:
`data-engineering/etl-pipeline-project/data/processed_countries.csv`

This is intentional — ETL pipeline cleans the data, 
ML project learns from it.

---

## 📊 Part 1 — Exploratory Data Analysis (EDA)

**9 cells of exploration before touching any model:**

| Finding | Detail |
|---------|--------|
| Dataset | 195 countries, 7 columns, zero nulls |
| Most dense | Monaco — 19,021 people/km² |
| Least dense | Mongolia — 2.27 people/km² |
| Most countries | Africa — 54 countries |
| Highest avg density | Europe — 612 people/km² |
| Data distribution | Right skewed — most countries low density |
| Key correlation | Area and density = -0.06 (almost no relationship) |

**Key lesson:** Data corrected our assumptions before 
we built any model. Africa has most countries but Europe 
has highest density — not what we expected.

---

## 🎯 Part 2 — K-Means Clustering (Unsupervised Learning)

**Goal:** Group similar countries together with no labels.

**Challenges and fixes:**

| Problem | Fix | Why |
|---------|-----|-----|
| Different scales (billions vs hundreds) | StandardScaler | Equal importance to all columns |
| 187 countries in one cluster | Log transformation | Compressed extreme outliers |
| How many clusters | Elbow Method | K=4 identified as optimal |

**Final 4 clusters:**

| Cluster | Sample Countries | Type |
|---------|----------------|------|
| 0 | Brazil, Russia, Sudan | Large area, low density |
| 1 | Singapore, Bahrain | Small, very dense |
| 2 | India, China, USA | Large population + area |
| 3 | Netherlands, Rwanda | Medium, moderate density |

✅ **Result: Successful — meaningful clusters found**

---

## 📈 Part 3 — Prediction (Supervised Learning)

**Goal:** Predict population density from area and region.

**Models tried:**

| Model | MAE | R² | Outcome |
|-------|-----|-----|---------|
| Linear Regression (raw) | 323.70 | -6.34 | Data not scaled |
| Linear Regression + log | 3.68 | 1.00 | Data leakage identified |
| Linear Regression (fixed) | 96.25 | -0.03 | Weak features |
| Random Forest (fixed) | 89.68 | -0.21 | Small dataset |

**⚠️ Honest Assessment:**

Prediction models showed poor results for three reasons:
- **Data leakage** — population density is calculated from 
  population and area, so using population as a feature 
  is cheating
- **Small dataset** — 195 rows is too small for reliable 
  ML prediction
- **Weak features** — area and region alone cannot 
  reliably predict density

**Key insight:** Not every dataset suits every ML algorithm. 
Knowing when NOT to use a model is as important as 
knowing how to build one.

---

## 💡 Key Concepts Learned

| Concept | Meaning |
|---------|---------|
| EDA | Explore data before building any model |
| StandardScaler | Brings all columns to same scale |
| Log transformation | Compresses extreme outliers |
| Elbow Method | Finds optimal number of clusters |
| Data leakage | When features directly contain the answer |
| Overfitting | Model memorises training data, fails on new data |
| Supervised learning | Model learns from labelled data |
| Unsupervised learning | Model finds patterns on its own |

---

## 📁 Project Structure
country-ml-project/
├── src/
│   ├── clustering.py     # K-Means clustering
│   └── prediction.py     # Linear Regression + Random Forest
├── notebooks/
│   └── exploration.ipynb # Full EDA + experiments
├── models/
│   ├── kmeans_model.pkl  # Saved K-Means model
│   └── scaler.pkl        # Saved StandardScaler
└── requirements.txt

---

## ⚙️ Tech Stack

Python · Scikit-learn · Pandas · Matplotlib · 
Seaborn · Joblib · Jupyter · NumPy

---

## 🚀 How To Run

```bash
# Run clustering
python src/clustering.py

# Run prediction experiments
python src/prediction.py

# Open notebook
jupyter notebook notebooks/exploration.ipynb
```

---

## 🔜 Future Improvements

- [ ] Try with a larger dataset (World Bank data)
- [ ] Add more features (GDP, urbanisation rate)
- [ ] Try classification instead of regression
- [ ] Deploy K-Means model as a simple API