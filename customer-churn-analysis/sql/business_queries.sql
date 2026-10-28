-- Run against outputs/customer_churn_analysis.db after src/load_and_clean.py.
-- The cleaned merged table is named churn_data.

-- 1. Overall churn and retention
SELECT
    COUNT(DISTINCT customerid) AS customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(100.0 * AVG(churn_flag), 2) AS churn_rate_pct,
    ROUND(100.0 * (1 - AVG(churn_flag)), 2) AS retention_rate_pct
FROM churn_data;

-- 2. Churn rate and customer count by plan type
SELECT
    plan_type,
    COUNT(DISTINCT customerid) AS customers,
    ROUND(100.0 * AVG(churn_flag), 2) AS churn_rate_pct
FROM churn_data
GROUP BY plan_type
ORDER BY churn_rate_pct DESC;

-- 3. Churn rate by state
SELECT
    state,
    COUNT(DISTINCT customerid) AS customers,
    ROUND(100.0 * AVG(churn_flag), 2) AS churn_rate_pct
FROM churn_data
GROUP BY state
ORDER BY churn_rate_pct DESC;

-- 4. Churned customers and monthly charges at risk by subscription source
SELECT
    subscription_type,
    COUNT(DISTINCT customerid) AS churned_customers,
    ROUND(SUM(monthly_charges), 2) AS monthly_charges_at_risk
FROM churn_data
WHERE churn_flag = 1
GROUP BY subscription_type
ORDER BY monthly_charges_at_risk DESC;

-- 5. Churn-risk group distribution
SELECT
    churn_risk,
    COUNT(DISTINCT customerid) AS customers,
    ROUND(100.0 * AVG(churn_flag), 2) AS churn_rate_pct
FROM churn_data
GROUP BY churn_risk
ORDER BY customers DESC;
