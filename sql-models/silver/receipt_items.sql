CREATE TABLE silver.receipt_items as
SELECT 
  gen_random_uuid() as receipt_item_id,
  r.id as receipt_id,
  r."rewardsReceiptStatus",
  to_timestamp(r."purchaseDate" / 1000)::date as purchase_date,
  to_timestamp(r."finishedDate" / 1000)::date as finish_date,
  to_timestamp(r."createDate" / 1000)::date as create_date,
  r."userId" as user_id,
  u.active as user_active, 
  to_timestamp(u."createdDate" / 1000)::date as user_create_date,
  i->>'barcode' as barcode,
  (i->>'finalPrice')::numeric as final_price,
  (i->>'itemPrice')::numeric as item_price,
  (i->>'quantityPurchased')::integer as qty_purchased,
  i->>'brandCode' as brand_code,
  i->>'rewardsGroup' as rewards_group,
  i->>'rewardsProductPartnerId' as brand_cpg_id,
  --b.name brand_name,
  --b.category category_name,
  (i->>'discountedItemPrice')::numeric as discounted_item_price,
  (i->>'deleted')::boolean as item_deleted,
  (i->>'priceAfterCoupon')::numeric as price_after_coupon
FROM 
  bronze.receipts r
LEFT JOIN 
  bronze.users u ON u.id = r."userId",
  jsonb_array_elements(r."rewardsReceiptItemList") as i
--LEFT JOIN 
  --bronze.brands b 