CREATE TABLE bronze.receipts (
	id text primary key,
	"bonusPointsEarned" numeric, 
	"bonusPointsEarnedReason" text,
	"createDate" bigint,
	"dateScanned" bigint,
	"finishedDate" numeric,
	"modifyDate" bigint,
	"pointsAwardedDate" numeric,
	"pointsEarned" numeric,
	"purchaseDate" numeric,
	"purchasedItemCount" numeric,
	"rewardsReceiptStatus" text,
    "rewardsReceiptItemList" jsonb,
	"totalSpent" numeric,
	"userId" text
);