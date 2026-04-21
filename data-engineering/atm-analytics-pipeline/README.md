# ATM Transaction Analytics Pipeline 🏧

**Author:** Vaibhav Garg — Data Engineer | AI & ML Graduate  
**Tech Stack:** PySpark, Python, Pytest, Loguru, Parquet  
**Domain:** ATM Transaction Analytics — built for Diebold Nixdorf interview preparation

---

## 📌 Project Overview

A production-grade PySpark pipeline that generates, processes, and analyses
10,000 realistic ATM transactions. Built to demonstrate hands-on PySpark skills
relevant to the Diebold Nixdorf Data Engineer role.

---

## 📁 Project Structure
atm-analytics-pipeline/
├── src/
│   ├── pipeline.py          # Main pipeline — ingestion, transformations, analytics
│   └── data_generator.py    # Generates 10,000 realistic ATM transactions
├── tests/
│   └── test_transformations.py  # 12 pytest unit tests — all passing
├── data/                    # Parquet output (gitignored)
├── logs/                    # Pipeline logs (gitignored)
└── README.md

---

## 🔧 How to Run

```bash
# Clone the repo
git clone https://github.com/vaibhavgarg003/industry-learning.git
cd industry-learning/data-engineering/atm-analytics-pipeline

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install pyspark==3.5.1 loguru pytest

# Run pipeline
cd src && python3 pipeline.py

# Run tests
cd ..
python3 -m pytest tests/ -v
```

---

## 🔄 Pipeline Architecture
data_generator.py
│
▼
Generate 10,000 ATM transactions (Python list)
│
▼
spark.createDataFrame() — load into Spark
│
▼
Repartition to 4 partitions
│
▼
Transformations (narrow — no shuffle)
├── Cast Timestamp string → TimestampType
├── Extract Hour from Timestamp
├── Classify into TimeBucket (Morning/Afternoon/Evening/Night)
├── Flag IsHighValue (Amount > 500)
└── Round Amount to 2 decimal places
│
▼
Analytics (wide — groupBy causes shuffle)
├── Status distribution
├── Transactions by city
├── Transactions by time bucket
└── High value transaction count
│
▼
Write to Parquet (4 part files)

---

## 🧠 Engineering Decisions

| Decision | What | Why |
|---|---|---|
| PySpark 3.5.1 | Downgraded from 4.1.1 | 4.x has known Windows/WSL compatibility issues — 3.5.x is stable and used in production |
| WSL2 + Ubuntu | Run environment | PySpark on Windows has Docker hostname conflicts — WSL2 provides clean Linux environment |
| Virtual environment | Dependency isolation | Prevents conflicts with other Python projects on same machine |
| 4 partitions | `df.repartition(4)` | Default 16 partitions for 10,000 rows is overkill — 4 reduces overhead while maintaining parallelism |
| Parquet output | Columnar format | Faster analytics queries than CSV — industry standard for big data pipelines |
| Loguru logging | Replace print statements | Timestamped, levelled logs saved to file — production monitoring standard |
| Dictionary-based data generator | List of dicts not tuples | Spark infers column names automatically — more readable and maintainable |
| Controlled test data | 4 rows in fixtures | Predictable assertions — know exact expected output without randomness |

---

## ✅ Test Results
12 tests — all passing
Schema tests:
✅ test_dataframe_has_correct_columns
✅ test_dataframe_row_count
✅ test_amount_is_double
Transformation tests:
✅ test_timestamp_cast
✅ test_hour_extraction
✅ test_high_value_flag_true
✅ test_high_value_flag_false
✅ test_time_bucket_morning
✅ test_time_bucket_night
Analytics tests:
✅ test_status_groupby
✅ test_city_groupby
✅ test_no_null_transaction_ids
✅ test_balance_inquiry_amount_is_zero

---

## 💡 Key PySpark Concepts Demonstrated

- **SparkSession** — entry point to Spark, configured for local execution
- **Lazy evaluation** — transformations build a DAG, actions trigger execution
- **Narrow vs Wide transformations** — withColumn (narrow) vs groupBy (wide/shuffle)
- **Partitioning** — repartition for controlled parallelism
- **Parquet** — columnar format for efficient analytics storage
- **Schema inference vs explicit schema** — trade-offs documented
- **Window functions** — ready for next iteration

---

## 📬 Connect

- **LinkedIn:** [linkedin.com/in/vaibhavgarg003](https://linkedin.com/in/vaibhavgarg003)
- **GitHub:** [github.com/vaibhavgarg003](https://github.com/vaibhavgarg003