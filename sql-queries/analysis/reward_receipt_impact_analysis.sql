-- Questions:
	-- When considering *average spend* from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
	-- When considering *total number of items purchased* from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
WITH base as (
	SELECT
		receipt_id,
		"rewardsReceiptStatus",
		SUM(final_price) total_spend,
		COUNT(receipt_item_id) num_items,
		SUM(qty_purchased) qty_purchased
	FROM 
		silver.receipt_items 
	WHERE 
		"rewardsReceiptStatus" in ('FINISHED','REJECTED')
	GROUP BY
		receipt_id, "rewardsReceiptStatus"
)
SELECT
	"rewardsReceiptStatus",
	ROUND(AVG(total_spend),2) avg_total_spend,
	ROUND(SUM(total_spend),2) total_spend,
	SUM(num_items) total_items_purchased,
	SUM(qty_purchased) total_quantity_purchased
FROM 
	base
GROUP BY 
	"rewardsReceiptStatus"