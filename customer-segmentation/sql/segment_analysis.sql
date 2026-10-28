-- Optional examples for use after loading customers_segmented.csv into SQLite
-- as a table named customers_segmented.

-- 1. Segment size and share
SELECT
    Segment_ID,
    COUNT(*) AS customers,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM customers_segmented), 2) AS customer_share_pct
FROM customers_segmented
GROUP BY Segment_ID
ORDER BY customers DESC;

-- 2. Average income, total spending, and recency per segment
SELECT
    Segment_ID,
    ROUND(AVG(Income), 2) AS avg_income,
    ROUND(AVG(Total_Spending), 2) AS avg_total_spending,
    ROUND(AVG(Recency), 2) AS avg_days_since_purchase
FROM customers_segmented
GROUP BY Segment_ID
ORDER BY avg_total_spending DESC;

-- 3. Campaign response rate by segment
SELECT
    Segment_ID,
    COUNT(*) AS customers,
    ROUND(100.0 * AVG(Response), 2) AS campaign_response_rate_pct
FROM customers_segmented
GROUP BY Segment_ID
ORDER BY campaign_response_rate_pct DESC;
