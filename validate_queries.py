"""
Validates the Retail Sales Analysis project by loading the CSV and running
all 10 business queries. Uses DuckDB (PostgreSQL-compatible SQL). No database install required.
Run: pip install -r requirements.txt && python validate_queries.py
"""
import os
import duckdb

DB_PATH = "retail_project.duckdb"
CSV_PATH = "SQL - Retail Sales Analysis_utf .csv"


def main():
    if not os.path.exists(CSV_PATH):
        print(f"ERROR: CSV not found: {CSV_PATH}")
        return False

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    con = duckdb.connect(DB_PATH)

    try:
        print("1. Loading CSV into retail_sales...")
        con.execute("""
            CREATE TABLE retail_sales AS
            SELECT * FROM read_csv_auto(?, header=true, dateformat='%Y-%m-%d')
        """, [CSV_PATH])
        n = con.execute("SELECT COUNT(*) FROM retail_sales").fetchone()[0]
        print(f"   Loaded {n} rows.")

        print("2. Data cleaning (remove nulls)...")
        nulls = con.execute("""
            SELECT COUNT(*) FROM retail_sales
            WHERE transactions_id IS NULL OR sale_date IS NULL OR sale_time IS NULL
               OR customer_id IS NULL OR gender IS NULL OR age IS NULL
               OR category IS NULL OR quantiy IS NULL OR price_per_unit IS NULL
               OR cogs IS NULL OR total_sale IS NULL
        """).fetchone()[0]
        con.execute("""
            DELETE FROM retail_sales
            WHERE transactions_id IS NULL OR sale_date IS NULL OR sale_time IS NULL
               OR customer_id IS NULL OR gender IS NULL OR age IS NULL
               OR category IS NULL OR quantiy IS NULL OR price_per_unit IS NULL
               OR cogs IS NULL OR total_sale IS NULL
        """)
        n_after = con.execute("SELECT COUNT(*) FROM retail_sales").fetchone()[0]
        print(f"   Removed {nulls} rows with nulls. Rows remaining: {n_after}.")

        print("3. Running business queries 1–10...")
        con.execute("SELECT COUNT(*) FROM retail_sales WHERE sale_date = '2022-11-05'").fetchone()
        con.execute("""
            SELECT COUNT(*) FROM retail_sales
            WHERE category = 'Clothing' AND strftime(sale_date, '%Y-%m') = '2022-11' AND quantiy >= 4
        """).fetchone()
        con.execute("SELECT category, SUM(total_sale) FROM retail_sales GROUP BY category").fetchall()
        con.execute("SELECT ROUND(AVG(age), 2) FROM retail_sales WHERE category = 'Beauty'").fetchone()
        con.execute("SELECT COUNT(*) FROM retail_sales WHERE total_sale > 1000").fetchone()
        con.execute("SELECT category, gender, COUNT(*) FROM retail_sales GROUP BY category, gender").fetchall()
        con.execute("""
            SELECT year, month, total_sale, avg_sale FROM (
                SELECT EXTRACT(YEAR FROM sale_date) AS year, EXTRACT(MONTH FROM sale_date) AS month,
                       SUM(total_sale) AS total_sale, ROUND(AVG(total_sale), 2) AS avg_sale,
                       RANK() OVER (PARTITION BY EXTRACT(YEAR FROM sale_date) ORDER BY SUM(total_sale) DESC) AS rnk
                FROM retail_sales GROUP BY 1, 2
            ) t WHERE rnk = 1 ORDER BY year
        """).fetchall()
        con.execute("""
            SELECT customer_id, SUM(total_sale) FROM retail_sales GROUP BY 1 ORDER BY 2 DESC LIMIT 5
        """).fetchall()
        con.execute("SELECT category, COUNT(DISTINCT customer_id) FROM retail_sales GROUP BY category").fetchall()
        con.execute("""
            WITH hourly_sale AS (
                SELECT *, CASE
                    WHEN EXTRACT(HOUR FROM sale_time) < 12 THEN 'Morning'
                    WHEN EXTRACT(HOUR FROM sale_time) BETWEEN 12 AND 17 THEN 'Afternoon'
                    ELSE 'Evening' END AS shift FROM retail_sales
            )
            SELECT shift, COUNT(*) FROM hourly_sale GROUP BY shift
        """).fetchall()

        print("\n   All 10 queries completed successfully.")
        return True

    except Exception as e:
        print(f"\nERROR: {e}")
        return False
    finally:
        con.close()
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)


if __name__ == "__main__":
    ok = main()
    exit(0 if ok else 1)
