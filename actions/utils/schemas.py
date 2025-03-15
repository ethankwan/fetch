receipts_columns = ['id', 'bonusPointsEarned', 'bonusPointsEarnedReason', 'createDate', 'dateScanned', 'finishedDate', 'modifyDate', 'pointsAwardedDate', 'pointsEarned', 'purchaseDate', 'purchasedItemCount', 'rewardsReceiptStatus', 'rewardsReceiptItemList', 'totalSpent', 'userId']
users_columns = ['id', 'state', 'createdDate', 'role', 'active', 'signUpSource', 'lastLoginDate']
brands_columns = ['id', 'barcode', 'brandCode', 'category', 'categoryCode', 'name', 'topBrand', 'cpgId', 'cpgRef']
load_columns = {
    'receipts': receipts_columns,
    'users': users_columns,
    'brands': brands_columns
}