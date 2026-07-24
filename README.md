# Data Engineering: Building an ETL Pipeline for Scoops

For this sprint, you'll be building a Python ETL pipeline to process weekly sales data for **Scoops**, a (fictional) ice cream company with multiple branches across the UK.

## Repo

You'll find three example CSV exports in the repo linked below, along with a skeleton project structure to build your pipeline into.

## Scenario

Scoops operates 16 ice cream shops across the UK (London, Manchester, Birmingham, Glasgow, Edinburgh, and more). At the end of each week, each branch's point-of-sale system exports a CSV of that week's sales. These files land with the data engineering team and need to go through an ETL pipeline before they're usable for analytics. You are that data engineering team.

You've been given three related exports:

| File           | Contents                                                                                         |
| -------------- | ------------------------------------------------------------------------------------------------ |
| `flavours.csv` | `id`, `name`, `contains_nuts` (bool), `cost_price_in_pence`: the ice cream flavours Scoops sells |
| `stores.csv`   | `store_id`, `store_name`, `region`, `latitude`, `longitude`: the branches                        |
| `sales.csv`    | `id`, `store_id`, `timestamp`, `flavour_id`, `price_in_pence`: individual sales                  |

## Pipeline stages

Your pipeline moves through four distinct stages, and **each stage saves its output to disk** before the next stage begins:

1. **Extract**: read the raw CSVs into memory.
2. **Clean**: fix data quality issues, save the cleaned data as its own set of files.
3. **Model**: reshape the cleaned data into a star schema (fact + dimensions), save _that_ as its own set of files.
4. **Load**: take the star-schema-shaped files and load them into a database.

Keeping these as separate, persisted steps means you can inspect, debug, or re-run any one stage without re-running the others: this is exactly how real pipelines are built.

## Learning Objectives

- Extract data from multiple related CSV sources into Python.
- Identify data quality issues by inspecting data.
- Clean raw exports into a trustworthy dataset, as a distinct step from schema design.
- Model cleaned data as a star schema, distinguishing facts from dimensions.
- Save outputs at each pipeline stage, rather than treating the pipeline as one monolithic step.
- Load a star schema into a database.

---

# Preliminary - Explore the Data

Before writing any pipeline code, get to know the data you're working with.

Load each CSV into a pandas DataFrame and inspect it: `head()`, `dtypes`, `describe()`, `isnull().sum()` are good starting points.

As you explore, keep notes on what you find. For each file, ask yourself:

- **`flavours.csv`**: Is `contains_nuts` consistently represented, or does it show up in different forms (e.g. `Y`/`N`, `yes`/`no`, `1`/`0`, `TRUE`/`FALSE`)? Does `cost_price_in_pence` look sensible for every row?
- **`stores.csv`**: Does anything here need cleaning, or does it already look ready to load?
- **`sales.csv`**: Are `timestamp` values all in the same format? Are there any negative prices?

You don't need to fix anything yet: just build a clear picture of what "clean" will need to mean for this data.

---

# Part 1 - Extract

Build the **extract** stage of your pipeline: functions that read each CSV into memory as a DataFrame (or equivalent structure) with no cleaning applied yet.

- Write one extract function per entity (`extract_flavours`, `extract_stores`, `extract_sales`), each taking a file path and returning a DataFrame.
- Keep extract "dumb" on purpose: its only job is getting the raw data in. Save cleaning logic for the next stage. This separation will make your pipeline much easier to test and debug.
- Think about how your functions should behave if a file is missing or empty. You don't need to solve this fully now, but it's worth deciding on an approach (raise an error? log and skip?).

---

# Part 2 - Clean

This stage is about **cleaning only**: fixing the data quality issues you found in the Preliminary section. Don't reshape the data into anything new yet; that's the next stage. Each function here should take a raw DataFrame and return a cleaned version of the _same shape_.

**Flavours**

- Coerce `contains_nuts` to a boolean, whatever form it arrives in (`Y`/`N`, `yes`/`no`, `1`/`0`, `TRUE`/`FALSE`, etc.).
- Confirm `cost_price_in_pence` is numeric and sensible: this column is already clean, but it's good practice to verify rather than assume.

**Sales**

- Parse `timestamp` into a uniform datetime, handling the inconsistent formats you found (some rows use `DD/MM/YYYY HH:MM:SS` instead of the standard `YYYY-MM-DD HH:MM:SS`).
- Coerce `price_in_pence` to a numeric type, and decide how to handle negative prices (drop the row? take the absolute value? flag it for review?).

**Save your output.** Once each DataFrame is cleaned, write it out, e.g. `data/cleaned/flavours.csv`, `data/cleaned/stores.csv`, `data/cleaned/sales.csv`. This is your checkpoint: the next stage should read from these files, not from the raw ones.

Add logging (or print a short summary) at the end of this stage: how many rows came in, how many were changed or dropped, and why. This kind of visibility is standard practice in production ETL pipelines.

## Tips

- Getting inconsistent results from `pd.to_datetime`? Look into the `format` and `errors` arguments: you may need to try more than one format and fall back gracefully.
- Not sure how to coerce a mixed-format boolean column? Consider adding in some logic to manually map the different representations to `True`/`False`, rather than relying on pandas to guess.

---

# Part 3 - Model as a Star Schema

Now that your data is clean, this stage is about **reshaping it**: turning three entity-shaped tables into a star schema: one fact table and three dimension tables. This is a modelling step, not a cleaning step; the data going in should already be trustworthy.

You've been given the schema as a diagram, not as SQL: working out the shape of each table is part of the task.

## The schema

You'll be given an ER diagram of the schema alongside this brief. It looks like this:

| Table         | Type      | Contents                                                                                                  |
| ------------- | --------- | --------------------------------------------------------------------------------------------------------- |
| `fact_sales`  | Fact      | `sale_id` (PK), `date_id` (FK), `store_id` (FK), `flavour_id` (FK), `price_in_pence`, `quantity`          |
| `dim_date`    | Dimension | `date_id` (PK), `full_date`, `day`, `month`, `month_name`, `quarter`, `year`, `day_of_week`, `is_weekend` |
| `dim_store`   | Dimension | `store_id` (PK), `store_name`, `region`, `latitude`, `longitude`                                          |
| `dim_flavour` | Dimension | `flavour_id` (PK), `name`, `contains_nuts`, `cost_price_in_pence`                                         |

## What you need to do

- **Read from `data/cleaned/`**, not from the original CSVs.
- **Populate `dim_date` programmatically.** This table isn't derived from any of the three source CSVs: you'll need to generate it, covering a sensible date range (e.g. every calendar day across the year your sample sales data spans), with all its derived columns (day of week, quarter, is_weekend, etc.) computed rather than hand-typed.
- **Build `fact_sales`** ensuring any dimensions can be joined onto it through foreign keys.
- **Save your output.** Write out each of the four tables as its own file, e.g. `data/star_schema/fact_sales.csv`, `data/star_schema/dim_date.csv`, `data/star_schema/dim_store.csv`, `data/star_schema/dim_flavour.csv`. This is your second checkpoint: you should be able to inspect these files directly and see a fully star-schema-shaped dataset, before any database is involved.

> **Hint:** it's worth building and testing `dim_date` in isolation first: it doesn't depend on your CSVs at all, so there's no reason to debug it at the same time as everything else.

---

# Part 4 - Load

Take the star-schema-shaped files from `data/star_schema/` and load them into a database.

- **Write the table creation statements yourself**, based on the schema table above: work out appropriate column types, primary keys, and foreign key constraints.
- Load each dimension table first, then `fact_sales`, so that the foreign key constraints can be satisfied.
- You can use Postgres or SQLite to build the database.

By the end of this section, you should be able to run your pipeline end-to-end (Extract → Clean → Model → Load) with a persisted file at each checkpoint along the way, and query the resulting database for clean, trustworthy sales data.

---

# Extra Challenge 1: Enrich with Bank Holidays

Scoops sells significantly more ice cream on bank holidays. You have access to a UK Bank Holidays API:

- `GET /uk/bank-holidays/{year}`: returns all UK bank holidays for a given year.
  - Example: `GET http://URL:8000/uk/bank-holidays/2024`
  - Response: `[{"date": "2024-01-01", "name": "New Year's Day"}, ...]`

- `/docs`: interactive API docs, including a "Try it out" button for each endpoint.

**Your task:**

- Fetch UK bank holidays for all years covered by your sales data.
- Add an `is_bank_holiday` column to `dim_date`, set to `True` for any date returned by the API.
- Re-save `dim_date` in `data/star_schema/` with the new column, so the enrichment is part of your persisted checkpoint, not just something computed on the fly.

---

# Extra Challenge 2: Automate the Pipeline

Turn your four stages into a single runnable pipeline: a script or CLI command that takes a week's set of CSVs and runs extract → clean → model → load in one go.

- It should be straightforward to point the pipeline at a _new week's_ export without editing code.
- Even though the pipeline runs end-to-end automatically, it should still write out the intermediate `data/cleaned/` and `data/star_schema/` files: automation shouldn't mean losing your checkpoints.
- Consider how you'd schedule this to run automatically once a week (a `cron` job, or a simple orchestration tool, would both be reasonable answers, you don't need to fully implement scheduling, just show you've thought about how it would work).

---

# Extra Challenge 3: Build an Analytics Layer

Now that clean data is loaded into your star schema, write queries (joining `fact_sales` to the relevant dimensions) to answer the kinds of questions the business would actually ask:

- Total revenue per store, per day.
- The best-selling flavour overall, and per store.
- Profit per flavour (revenue minus `cost_price_in_pence`), and which flavours have the highest margin.
- Which stores sell the highest proportion of nut-containing flavours (useful for allergen-related planning).
- (If you completed Extra Challenge 1) Average revenue on bank holidays vs non-bank holidays.
- (If you completed Extra Challenge 2) Correlation between weather (temperature, rainfall) and sales volume.

Present your results however you like: printed output, a simple chart, or a short markdown summary are all fine.

---

# Extra Challenge 4: Enrich with Weather Data

Scoops sells significantly more ice cream on warm, sunny days. You have access to the Open-Meteo Historical Weather API (free, no signup required):

- `GET https://archive-api.open-meteo.com/v1/archive`: returns historical weather data for a location and date range.
  - Example: `https://archive-api.open-meteo.com/v1/archive?latitude=51.5159&longitude=-0.1431&start_date=2024-06-01&end_date=2024-06-07&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code`
  - Response includes temperature (°C), precipitation (mm), and a WMO weather code (you'll need to map these codes to readable categories like "Sunny", "Rainy", "Cloudy").
  - Documentation: https://open-meteo.com/en/docs/historical-weather-api

**Your task:**

- For each store location (latitude/longitude) and the date range of your sales, fetch historical weather data from Open-Meteo.
- Map the WMO weather codes to simple categories: "Sunny" (codes 0-1), "Cloudy" (2-3), "Rainy" (45, 48, 51-67, 80-82), "Snowy" (71-77, 85-86), etc. (reference: https://www.open-meteo.com/en/docs/historical-weather-api).
- Create a new `fact_weather` table: `date_id`, `store_id`, `temp_celsius`, `rainfall_mm`, `weather_condition`. Save it to `data/star_schema/fact_weather.csv` alongside your other star schema tables.
- Load `fact_weather` into your database, with foreign keys to `dim_date` and `dim_store`, so it can be joined to `fact_sales` in your analytics queries.

This exercise introduces **additive fact tables**, a real analytics pattern where multiple fact tables share the same dimensions and can be joined together (in this case, sales and weather both key off `date_id` and `store_id`).

---

# Conclusion

Well done! You've built a full ETL pipeline that takes real-world-shaped data and turns it into something an analytics team could actually trust, with a clear, inspectable checkpoint at every stage along the way.

## Sprint outcomes

You have accomplished some major tasks in data engineering:

- Extracting data from multiple related CSV sources
- Identifying and resolving real data quality issues, as a distinct step from schema design
- Modelling cleaned data as a star schema, with dimensions and a fact table
- Persisting intermediate outputs at every pipeline stage
- Loading a star schema into a structured database
