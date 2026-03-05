--- SQL RETAIL SALES ANALYSIS PROJECT
CREATE DATABASE retail_project;

---CREATE TABLE
DROP TABLE IF EXISTS retail_sales;
CREATE TABLE retail_sales
        (
             transactions_id INT PRIMARY KEY,
			  sale_date DATE,
			  sale_time	TIME,
			  customer_id INT,
			  gender VARCHAR(15),
			  age INT,
			  category VARCHAR(15),
			  quantiy INT,
			  price_per_unit FLOAT,
			  cogs FLOAT,
			  total_sale FLOAT
		);

SELECT * FROM retail_sales;


--- DATA CLEANING
SELECT * FROM retail_sales
WHERE
      transactions_id IS NULL
      OR
	  sale_date IS NULL
	  OR
	  sale_time IS NULL
	  OR
	  customer_id IS NULL
	  OR
	  gender IS NULL
	  OR
	  age IS NULL
	  OR
	  category IS NULL
	  OR
	  quantiy IS NULL
	  OR
	  price_per_unit IS NULL
	  OR
	  cogs IS NULL
	  OR
	  total_sale IS NULL;

---
DELETE FROM retail_sales
WHERE
     transactions_id IS NULL
      OR
	  sale_date IS NULL
	  OR
	  sale_time IS NULL
	  OR
	  customer_id IS NULL
	  OR
	  gender IS NULL
	  OR
	  age IS NULL
	  OR
	  category IS NULL
	  OR
	  quantiy IS NULL
	  OR
	  price_per_unit IS NULL
	  OR
	  cogs IS NULL
	  OR
	  total_sale IS NULL;
--- DATA EXPLORATION

--- Total number of sales
SELECT COUNT(*) AS total_sales FROM retail_sales

--- HOW MANY CUSTOMERS DO WE HAVE
SELECT COUNT(DISTINCT customer_id) AS total_customers FROM retail_sales

--- Product categories
SELECT DISTINCT category FROM retail_sales

--- Business analysis queries
-- 1. Retrieve all columns for sales made on '2022-11-05'
SELECT * 
FROM retail_sales
WHERE sale_date = '2022-11-05'

-- 2. Transactions: category 'Clothing', quantity >= 4, month Nov-2022
SELECT *
FROM retail_sales
WHERE 
category = 'Clothing'
AND 
TO_CHAR(sale_date, 'YYYY-MM') = '2022-11'
AND 
quantiy >= 4
   
-- 3. Total sales (net_sale) per category
SELECT 
  category,
  SUM(total_sale) AS net_sale
FROM retail_sales
GROUP BY category

-- 4. Average age of customers who purchased from 'Beauty' category
SELECT
   ROUND(AVG(age), 2) AS avg_age
FROM retail_sales
where
category = 'Beauty'

-- 5. All transactions where total_sale > 1000
SELECT * FROM retail_sales
WHERE total_sale > 1000

-- 6. Number of transactions by gender and category
SELECT category,gender,
count(*) AS total_trans
FROM retail_sales
GROUP BY category,gender
ORDER BY 1

-- 7. Best selling month in each year (by total sales, with avg sale)
SELECT
    year,
    month,
    total_sale,
    avg_sale
FROM (
    SELECT
        EXTRACT(YEAR FROM sale_date) AS year,
        EXTRACT(MONTH FROM sale_date) AS month,
        SUM(total_sale) AS total_sale,
        ROUND(AVG(total_sale), 2) AS avg_sale,
        RANK() OVER (PARTITION BY EXTRACT(YEAR FROM sale_date) ORDER BY SUM(total_sale) DESC) AS rnk
    FROM retail_sales
    GROUP BY 1, 2
) t
WHERE rnk = 1
ORDER BY year

-- 8. Top 5 customers by total sales
SELECT 
customer_id,
SUM(total_sale) AS total_sales
FROM retail_sales
GROUP BY 1
ORDER BY 2 DESC
LIMIT 5 

-- 9. Unique customers per category
SELECT
category,
COUNT(DISTINCT customer_id) as cnt_unique_cs
FROM retail_sales
GROUP BY category

-- 10. Orders by shift (Morning <12, Afternoon 12–17, Evening >17)
WITH hourly_sale
AS
(
SELECT *,
CASE
  WHEN EXTRACT(HOUR FROM sale_time) < 12 THEN 'Morning'
  WHEN EXTRACT(HOUR FROM sale_time) BETWEEN 12 AND 17 THEN 'Afternoon'
  ELSE 'Evening'
  END AS shift
FROM retail_sales
)
SELECT 
shift,
count(*) as total_orders
FROM hourly_sale
GROUP BY shift

--- END ---
