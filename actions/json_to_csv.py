import json
import csv
import pandas as pd
from pandas.io.json._table_schema import build_table_schema
from collections import defaultdict
from utils.schemas import load_columns

# Clean column names for DW ingestion, as '$' is a reserved character
receipt_columns_to_rename = {
    '_id.$oid' : 'id',
    'createDate.$date': 'createDate',
    'dateScanned.$date': 'dateScanned',
    'finishedDate.$date': 'finishedDate', 
    'modifyDate.$date': 'modifyDate',
    'pointsAwardedDate.$date': 'pointsAwardedDate',
    'purchaseDate.$date': 'purchaseDate'
}

users_columns_to_rename = {
    '_id.$oid': 'id', 
    'createdDate.$date': 'createdDate',
    'lastLogin.$date': 'lastLoginDate'
}

brands_columns_to_rename = {
    '_id.$oid': 'id',
    'cpg.$id.$oid': 'cpgId',
    'cpg.$ref': 'cpgRef'
}

columns_to_rename = {
    'receipts' : receipt_columns_to_rename,
    'users' : users_columns_to_rename,
    'brands' : brands_columns_to_rename
}

# iterate through collections
collections = [
    'receipts', 
    'users', 
    'brands'
    ]

# final column definitions
'''receipts_columns = ['id', 'bonusPointsEarned', 'bonusPointsEarnedReason', 'createDate', 'dateScanned', 'finishedDate', 'modifyDate', 'pointsAwardedDate', 'pointsEarned', 'purchaseDate', 'purchasedItemCount', 'rewardsReceiptStatus', 'rewardsReceiptItemList', 'totalSpent', 'userId']
users_columns = ['id', 'state', 'createdDate', 'role', 'active', 'signUpSource', 'lastLoginDate']
brands_columns = ['id', 'barcode', 'brandCode', 'category', 'categoryCode', 'name', 'topBrand', 'cpgId', 'cpgRef']
load_columns = {
    'receipts': receipts_columns,
    'users': users_columns,
    'brands': brands_columns
}'''

for collection in collections:
    file_path = f"../{collection}.json"
    records = []
    with open(file_path, "r") as f:
        for line in f:
            records.append(json.loads(line))

    # flatten nested columns 
    df = pd.json_normalize(records)
    print(f"{collection} Schema: ----------------------------")
    print(df.info())

    # clean column names
    df.rename(columns=columns_to_rename[collection], inplace=True)
    print(df.info())

    df = df[[col for col in load_columns[collection]]]
    print(df.info())

    # prepare json attributes 
    json_features = ['rewardsReceiptItemList']
    for feature in json_features:
        if feature in load_columns[collection]:
            df[feature] = [json.dumps(x) for x in df[feature]]
            df[feature] = df[feature].replace('NaN', '[]')
            df[feature].fillna('[]', inplace=True)

    # generate csv file
    df.to_csv(f'{collection}.csv', sep='|', index=False, header=False, quoting=csv.QUOTE_NONE, escapechar='\\')
    print(f"{collection} json converted to csv")
