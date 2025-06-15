import mysql.connector
import pandas as pd

def normalize_persian_date(pdate):
    if isinstance(pdate, str):
        return pdate.replace('/', '-')
    return pdate

def normalize_datetime(row):
    time_part, date_part = row['date_time'].split()
    date_norm = normalize_persian_date(date_part)
    return f"{date_norm} {time_part}:00"

# DB Connection
conn = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_pass',
    database='sale_db'
)
cursor = conn.cursor(buffered=True)

# Read Excel
df = pd.read_excel('data/sample_sale.xlsx')
df['date'] = df['date'].apply(normalize_persian_date)
df['date_time'] = df.apply(normalize_datetime, axis=1)

# Maps
store_map = {}
seller_map = {}
customer_map = {}
product_category_map = {}
product_sub_category_map = {}
product_map = {}
invoice_map = {}

def insert_or_get_id(table, key_col, key_value, return_col='id', insert_query=None, insert_values=None):
    cursor.execute(f"SELECT {return_col} FROM {table} WHERE {key_col} = %s", (key_value,))
    result = cursor.fetchone()
    if result:
        return result[0]
    if insert_query and insert_values:
        cursor.execute(insert_query, insert_values)
        conn.commit()
        return cursor.lastrowid if return_col == 'id' else key_value
    return None
