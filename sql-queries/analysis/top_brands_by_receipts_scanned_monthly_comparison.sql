-- Question: How does the ranking of the top 5 brands by receipts scanned for the recent month compare to the ranking for the previous month?
-- Note: would prefer to use brandId, but there is no reliable link between brands and receipts
WITH monthly_brand_rank AS (
  SELECT
    DATE_TRUNC('month', purchase_date) as month,
    brand_code,
    COUNT(distinct receipt_id) as receipt_count,
    RANK() OVER (PARTITION BY DATE_TRUNC('month', purchase_date) ORDER BY COUNT(distinct receipt_id) DESC) as rank
  FROM
    silver.receipt_items
  WHERE
    purchase_date >= CURRENT_DATE - INTERVAL '2 months'
  GROUP BY
    DATE_TRUNC('month', purchase_date), brand_code
),
top_5_current AS (
  SELECT
    brand_code,
    rank as current_rank
  FROM
    monthly_brand_rank
  WHERE
    month = DATE_TRUNC('month', CURRENT_DATE)
  AND rank <= 5
),
top_5_previous AS (
  SELECT
    brand_code,
    rank as previous_rank
  FROM
    monthly_brand_rank
  WHERE
    month = DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
  AND rank <= 5
)
SELECT 
  COALESCE(c.brand_code, p.brand_code) as brand_code,
  p.previous_rank,
  c.current_rank
FROM 
  top_5_previous p
FULL OUTER JOIN 
  top_5_current c using (brand_code)