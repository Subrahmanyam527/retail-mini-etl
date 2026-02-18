# Retail Mini ETL

A beginner-friendly Python project for data extraction, transformation, and loading.

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the ETL Script
```bash
python src/etl.py
```

### 4. Run Tests
```bash
pytest -q
```

## Project Structure

- `src/` - Source code files
- `tests/` - Test files
- `data/raw/` - Raw input data (ignored by git)
- `data/processed/` - Processed output data (ignored by git)
- `db/` - Database files (ignored by git)
- `docs/` - Documentation files