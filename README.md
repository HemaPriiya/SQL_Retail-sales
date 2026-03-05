# Retail Sales Analysis

A data analysis project that demonstrates **SQL** for database setup, data cleaning, exploratory analysis, and business reporting on retail transaction data. Built for portfolio use to showcase practical analytics skills.

---

## What's in this repo

| Item | Description |
|------|-------------|
| **SQL_RETAIL_P1.sql** | Full pipeline: schema, cleaning, exploration, and 10 business queries |
| **SQL - Retail Sales Analysis_utf .csv** | Sample dataset (~2,000 transactions) |
| **validate_queries.py** | Optional script to run all queries without PostgreSQL (Python + DuckDB) |
| **requirements.txt** | Python dependencies for the validation script only |

---

## Skills demonstrated

- **Database design**: `CREATE DATABASE`, `CREATE TABLE`, primary key, data types (DATE, TIME, INT, FLOAT, VARCHAR)
- **Data cleaning**: Null checks, `DELETE` for invalid rows
- **Exploratory analysis**: `COUNT`, `COUNT(DISTINCT)`, `DISTINCT`, aggregations
- **Business queries**: Filtering (`WHERE`, `TO_CHAR`), grouping (`GROUP BY`), sorting (`ORDER BY`), `LIMIT`
- **Advanced SQL**: Window functions (`RANK() OVER PARTITION BY`), CTEs (`WITH`), date/time (`EXTRACT`, `EXTRACT(HOUR)`)

---

## Project flow

1. **Setup** — Create database `retail_project` and table `retail_sales`; load the CSV.
2. **Cleaning** — Identify and remove rows with nulls in any column.
3. **Exploration** — Total records, unique customers, product categories.
4. **Analysis** — 10 queries answering business questions (e.g. sales by category, top customers, best month per year, orders by time-of-day shift).

---

## Key findings (from the analysis)

- **Demographics**: Purchases span age groups and categories (e.g. Clothing, Beauty, Electronics).
- **High-value sales**: Multiple transactions exceed 1,000 in total sale amount.
- **Seasonality**: Best-selling month per year identified via aggregated sales and ranking.
- **Operational**: Order volume by shift (Morning / Afternoon / Evening) for staffing and planning.

---

## How to run (PostgreSQL)

1. Clone the repo and open the project folder.
2. Create the database and table by running the first part of **SQL_RETAIL_P1.sql** in your PostgreSQL client.
3. Load the CSV into `retail_sales`, for example:
   ```sql
   COPY retail_sales FROM '<full-path-to-csv>' WITH (FORMAT csv, HEADER true);
   ```
4. Run the rest of **SQL_RETAIL_P1.sql** (cleaning, exploration, and business queries) in order.

*Note: The CSV column `quantiy` is kept to match the file; the script uses the same name.*

---

## Optional: validate without PostgreSQL

To verify the project end-to-end without a database install:

```bash
pip install -r requirements.txt
python validate_queries.py
```

This loads the CSV and runs all 10 business queries; success is printed in the console.

---

## Author

**Hhemapriiya S. N.**  
[LinkedIn](https://www.linkedin.com/in/hhemapriiya-sn-32bb5a282/)

This project is part of my portfolio to show SQL and data analysis in a business context. Open to feedback and collaboration—feel free to connect.
