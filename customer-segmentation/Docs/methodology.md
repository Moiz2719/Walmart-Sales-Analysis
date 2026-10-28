# Methodology

## 1. Inspect and clean

Read the source file with delimiter detection because the downloaded file may be tab-delimited despite its .csv suffix. Standardise column names, remove duplicate customer records, convert numeric fields, and remove rows with missing income.

## 2. Engineer features

Create customer age using a fixed 2014 reference year, total household children, a parent indicator, a simplified living arrangement, aggregate product spending, total purchase count, prior campaign acceptance count, and enrolment tenure measured relative to the latest enrolment date present in the data.

## 3. Select segmentation inputs

Use numeric behaviour and spending fields such as age, income, household children, recency, total spending, total purchases, web visits, and discount purchases when available. Customer identifiers and campaign response are kept for profiling, not used as primary clustering inputs.

## 4. Scale and cluster

Standardise the selected features with StandardScaler so that larger-scale variables do not dominate distance calculations. Fit K-Means models for cluster counts from 2 through 8 (or fewer for smaller datasets), using a fixed random seed. Select the candidate with the highest silhouette score.

The selected score is one diagnostic, not proof that the segments are objectively correct. Compare other cluster counts and inspect interpretability before finalising a business narrative.

## 5. Profile and visualise

Calculate customer count and share per segment, averages for spending and purchasing channels, and campaign response where available. Create a cluster-size chart, spending chart, PCA projection, and income-versus-spending chart.

## 6. Turn segments into actions

Name segments only after reviewing actual profile output. Recommendations should be specific hypotheses to test, such as tailored bundles, loyalty messages, or re-engagement campaigns. Measure outcomes with a controlled test where possible.
