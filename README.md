# Scoops ETL Pipeline

A Python ETL pipeline that processes weekly sales data for Scoops, a fictional UK ice cream company.

```

## Pipeline stages

### Extract

Reads the following files from `data/raw_data/`:

```text
flavours.csv
stores.csv
sales.csv
```

### Clean

The cleaning stage:

- normalises `contains_nuts` values into booleans;
- parses mixed timestamp formats;
- converts prices and coordinates to numeric values;
- removes rows with missing required values;
- removes negative prices;
- validates store coordinates and duplicate store IDs.

Cleaned files are written to:

```text
data/cleaned_data/
```

### Model

The cleaned data is reshaped into a star schema:

```text
dim_date
dim_flavour
dim_store
fact_sales
```

Modelled CSV files are written to:

```text
data/star_schema/
```

### Load

The star-schema files are loaded into PostgreSQL.

Dimension tables are loaded before `fact_sales` so that foreign-key constraints are satisfied.

## Project structure

```text
.
├── data/
│   ├── raw_data/
│   ├── cleaned_data/
│   └── star_schema/
├── sql/
│   ├── schema.sql
│   ├── setup_db.sh
│   └── setup_test_db.sh
├── src/
│   ├── extract.py
│   ├── clean.py
│   ├── model.py
│   ├── load.py
│   └── pipeline.py
├── test/
├── main.py
├── Makefile
└── requirements.txt
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

PostgreSQL must be installed, and the current user must have permission to create and drop databases.

## Running the pipeline

Run the complete pipeline:

```bash
make pipeline
```

This command recreates the `scoops_sales` database and runs:

```text
Extract → Clean → Model → Load
```

You can also run the steps manually:

```bash
bash sql/setup_db.sh
python main.py
```

> `setup_db.sh` deletes and recreates the development database. Existing data will be removed, and open database sessions may be disconnected.

## Running tests

Run:

```bash
make test
```

This recreates `scoops_sales_test` and runs pytest.

The same steps can be run manually:

```bash
bash sql/setup_test_db.sh
pytest -q
```

## Current scope

This repository implements the core ETL pipeline.

Future stretch features:

- bank-holiday enrichment;
- weather enrichment;
- analytics dashboards or visualisations;
- weekly scheduling;
- incremental loading.