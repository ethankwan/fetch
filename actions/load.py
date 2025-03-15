import psycopg2
from utils.schemas import load_columns

def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 1
    print("Connection successful")
    return conn

def copy_from_file(conn, csvFile, table, loading_cols):
    """
    Here we are going save the dataframe on disk as
    a csv file, load the csv file
    and use copy_from() to copy it to the table
    """
    # Save the dataframe to disk
    
    temp_table = 'temp_' + table
    f = open(csvFile, 'r')
    cursor = conn.cursor()
    try:
        primaryKeys = ['_id']
        update_cols = [col for col in loading_cols if col not in primaryKeys]
        update_set = ", ".join([f""" "{col}"=EXCLUDED."{col}" """ for col in update_cols])
        loading_cols_str = ",".join([f""" "{col}"  """ for col in loading_cols])
        
        cursor.execute(
            f"""
            CREATE TEMPORARY TABLE "{temp_table}" (LIKE bronze."{table}")
            ON COMMIT DROP
            """
        )
        
        cursor.copy_from(f, temp_table, sep="|", null='')

        cursor.execute(
            f"""
                INSERT INTO bronze.{table}({loading_cols_str})
                SELECT distinct on (1) * FROM {temp_table}
                ON CONFLICT (id) DO UPDATE SET {update_set} 
            """
        )
        cursor.execute(f"DROP TABLE {temp_table}")
        
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        # os.remove(tmp_df)
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        
        return 1
    print("copy_from_file() done")
    cursor.close()

# would use secrets here, but left dummy credentials in place
param_dic = {
        "host": 'localhost',
        "port": 5432,
        "database": 'postgres',
        "user": 'postgres',
        "password": 'test'
    }
conn = connect(param_dic)
# iterate through collections
collections = [
    'receipts', 
    'users', 
    'brands'
    ]


for collection in collections:
    print(f"Loading {collection} into DB")
    loading_cols = load_columns[collection]
    file_path = f'./{collection}.csv'
    copy_from_file(conn, file_path, collection, loading_cols)