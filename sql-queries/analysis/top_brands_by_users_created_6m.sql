-- Questions:
	-- Which brand has the most *spend* among users who were created within the past 6 months?
	-- Which brand has the most *transactions* among users who were created within the past 6 months?
-- Note: would prefer to use brandId, but there is no reliable link between brands and receipts
SELECT
	brand_code,
	SUM(final_price) total_spend,
	COUNT(distinct receipt_id) num_transactions
FROM
	silver.receipt_items 
WHERE 
	user_create_date <= CURRENT_DATE - interval '6 months' and brand_code is not null
GROUP BY 
	brand_code
ORDER BY total_spend DESC -- can swap total_spend for num_transactions
LIMIT 1