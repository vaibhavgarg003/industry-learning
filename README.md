markdown# ETL Pipeline Project 🔧

A production-grade ETL (Extract, Transform, Load) pipeline built in Python that extracts live country data from a REST API, transforms it into clean structured data, and loads it into a SQLite database.

---

## 🏗️ Architecture
REST Countries API
↓
[Extractor]  → Fetches 195 countries, saves raw JSON
↓
[Transformer] → Cleans data, adds population density
↓
[Loader]     → Saves clean data into SQLite database
↓
[Logger]     → Logs every step to file and terminal

---

## 🔐 Security Decisions

- All configuration is stored in a `.env` file — **never committed to Git**
- `.gitignore` excludes secrets, generated data, and logs
- Sample data and logs are provided separately so recruiters can see real output without exposing sensitive config
- This mirrors industry best practices for secrets management

---

## 📁 Project Structure
etl-pipeline-project/
├── src/
│   ├── extractor.py      # Pulls data from REST API
│   ├── transformer.py    # Cleans and reshapes data
│   ├── loader.py         # Loads data into SQLite
│   └── pipeline.py       # Orchestrates all 3 steps
├── tests/
│   ├── test_extractor.py # 4 tests
│   ├── test_transformer.py # 6 tests
│   └── test_loader.py    # 5 tests
├── data/
│   └── samples/
│       └── sample_output.csv  # Sample of real pipeline output
├── logs/
│   └── sample_pipeline.log    # Sample of real pipeline logs
├── .env.example          # Template for environment variables
├── .gitignore            # Excludes secrets and generated files
├── Dockerfile            # Containerization for portability
└── requirements.txt      # Python dependencies

---

## ⚙️ Tech Stack

- **Python 3.12** — Core language
- **Pandas** — Data transformation
- **SQLAlchemy** — Database ORM
- **Requests** — API calls
- **Loguru** — Professional logging
- **pytest** — Unit testing
- **Docker** — Containerization
- **SQLite** — Local database
- **python-dotenv** — Environment variable management

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/vaibhavgarg003/industry-learning.git
cd industry-learning/data-engineering/etl-pipeline-project
```

### 2. Set up environment variables
```bash
cp .env.example .env
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the full pipeline
```bash
python src/pipeline.py
```

### 5. Run with Docker
```bash
docker build -t etl-pipeline .
docker run etl-pipeline
```

### 6. Run tests
```bash
pytest tests/ -v
```

---

## 📊 Sample Output

See `data/samples/sample_output.csv` for real pipeline output.

| Country | Population | Area km² | Density |
|---------|-----------|----------|---------|
| India | 1,417,492,000 | 3,287,263 | 431.21 |
| China | 1,408,280,000 | 9,706,961 | 145.08 |
| USA | 340,110,988 | 9,525,067 | 35.71 |

---

## 🧪 Test Results
tests/test_extractor.py    4 passed
tests/test_transformer.py  6 passed
tests/test_loader.py       5 passed
Total: 15 passed

---

## 💡 Key Engineering Decisions

| Decision | Reason |
|----------|--------|
| Save raw JSON before transforming | Raw layer acts as safety net — no need to re-call API if transformation fails |
| Use `replace` strategy in loader | Dataset is small reference data — full refresh is appropriate |
| File-based logging with daily rotation | Keeps logs manageable, mirrors production logging standards |
| Environment variables for config | Security best practice — secrets never committed to version control |
| pytest for testing | Industry standard, catches regressions when code changes |

---

## 🔜 Upcoming Improvements

- [ ] Schedule pipeline with Apache Airflow
- [ ] Move to cloud storage (AWS S3)
- [ ] Add incremental loading for large datasets
- [ ] Add GitHub Actions for CI/CD