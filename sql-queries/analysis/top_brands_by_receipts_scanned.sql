-- Question: What are the top 5 brands by receipts scanned for most recent month?
-- Note: would prefer to use brandId, but there is no reliable link between brands and receipts
SELECT 
    brand_code, 
    count(distinct receipt_id) receipts_scanned
FROM 
    silver.receipt_items
WHERE 
    purchase_date >= CURRENT_DATE - INTERVAL '1 months'
GROUP BY brand_code
ORDER BY receipts_scanned DESC 
LIMIT 5;

