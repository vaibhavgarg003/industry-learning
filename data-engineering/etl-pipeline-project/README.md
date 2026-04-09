# ETL Pipeline Project 🔧

A production-grade ETL pipeline extracting live data for 195 countries 
from a REST API, transforming it with Pandas, and loading into SQLite.

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

- All configuration stored in `.env` — never committed to Git
- `.gitignore` excludes secrets, generated data and logs
- `.env.example` provided as safe template for anyone cloning
- Mirrors industry best practices for secrets management

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
│       └── sample_output.csv
├── logs/
│   └── sample_pipeline.log
├── .env.example
├── .gitignore
├── Dockerfile
└── requirements.txt

---

## ⚙️ Tech Stack

Python · Pandas · SQLAlchemy · SQLite · Docker · pytest · Loguru · REST API · Git · GitHub Actions

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
Total: 15 passed ✅

---

## 💡 Key Engineering Decisions

| Decision | Reason |
|----------|--------|
| Save raw JSON before transforming | Safety net — no need to re-call API if transformation fails |
| Use `replace` strategy in loader | Small reference data — full refresh is appropriate |
| File-based logging with daily rotation | Keeps logs manageable, mirrors production standards |
| Environment variables for config | Security best practice — secrets never in version control |
| pytest for testing | Industry standard — catches regressions when code changes |

---

## ✅ Completed

- [x] ETL Pipeline — fully working end to end
- [x] 15 unit tests — all passing
- [x] Dockerized — runs anywhere
- [x] GitHub Actions CI/CD — tests auto-run on every push
- [x] Security-first design with .env

## 🔜 Upcoming Improvements

- [ ] Schedule pipeline with Apache Airflow
- [ ] Move to cloud storage (AWS S3)
- [ ] Add incremental loading for large datasets