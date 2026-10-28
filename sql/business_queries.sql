-- Walmart Sales Analysis: reusable SQLite business queries.
-- Run these after src/clean_data.py has created the walmart table.

-- 1. Transactions and quantity by payment method
SELECT payment_method, COUNT(*) AS transactions, SUM(quantity) AS total_quantity
FROM walmart
GROUP BY payment_method
ORDER BY transactions DESC;

-- 2. Highest-rated category in each branch (ties are retained)
WITH category_ratings AS (
    SELECT branch, category, AVG(rating) AS avg_rating,
           RANK() OVER (PARTITION BY branch ORDER BY AVG(rating) DESC) AS rnk
    FROM walmart
    GROUP BY branch, category
)
SELECT branch, category, ROUND(avg_rating, 2) AS avg_rating
FROM category_ratings
WHERE rnk = 1
ORDER BY branch;

-- 3. Busiest weekday in each branch (ties are retained)
WITH weekday_counts AS (
    SELECT branch, day, COUNT(*) AS transactions,
           RANK() OVER (PARTITION BY branch ORDER BY COUNT(*) DESC) AS rnk
    FROM walmart
    GROUP BY branch, day
)
SELECT branch, day, transactions
FROM weekday_counts
WHERE rnk = 1
ORDER BY branch;

-- 4. Average rating by city and product category
SELECT city, category, AVG(rating) AS avg_rating,
       MIN(rating) AS min_rating, MAX(rating) AS max_rating
FROM walmart
GROUP BY city, category
ORDER BY city, category;

-- 5. Estimated profit proxy by category. Validate profit_margin semantics first.
SELECT category,
       SUM(unit_price * quantity * profit_margin) AS estimated_profit
FROM walmart
GROUP BY category
ORDER BY estimated_profit DESC;

-- 6. Transaction volume by time of day
SELECT CASE WHEN time < '12:00:00' THEN 'Morning'
            WHEN time < '17:00:00' THEN 'Afternoon'
            ELSE 'Evening' END AS shift,
       COUNT(*) AS transactions
FROM walmart
GROUP BY shift
ORDER BY transactions DESC;

-- 7. Revenue by branch and year; use actual years present in the dataset.
SELECT branch, CAST(strftime('%Y', date) AS INTEGER) AS year,
       SUM(unit_price * quantity) AS revenue
FROM walmart
GROUP BY branch, CAST(strftime('%Y', date) AS INTEGER)
ORDER BY branch, year;
