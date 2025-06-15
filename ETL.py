import mysql.connector
import pandas as pd

def clean_value(val):
    if pd.isna(val):
        return None
    return val

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

# Stores
for store_name in df['store_name'].dropna().unique():
    if store_name not in store_map:
        insert_query = "INSERT IGNORE INTO stores (name) VALUES (%s)"
        store_id = insert_or_get_id('stores', 'name', store_name, insert_query=insert_query, insert_values=(clean_value(store_name),))
        if store_id is None:
            cursor.execute("SELECT id FROM stores WHERE name=%s", (store_name,))
            store_id = cursor.fetchone()[0]
        store_map[store_name] = store_id

# Sellers
for seller_id, seller_name in df[['seller_id', 'seller_name']].drop_duplicates().values:
    if pd.notna(seller_id) and pd.notna(seller_name) and seller_id not in seller_map:
        cursor.execute("INSERT IGNORE INTO sellers (id, name) VALUES (%s, %s)", (seller_id, seller_name))
        conn.commit()
        seller_map[seller_id] = seller_id

# Customers
for customer_id, customer_category in df[['customer_id', 'customer_category']].drop_duplicates().values:
    if pd.notna(customer_id) and pd.notna(customer_category) and customer_id not in customer_map:
        cursor.execute("INSERT IGNORE INTO customers (id, category) VALUES (%s, %s)", (customer_id, customer_category))
        conn.commit()
        customer_map[customer_id] = customer_id

# Product Categories
for product_category in df['product_category'].dropna().unique():
    if product_category not in product_category_map:
        insert_query = "INSERT IGNORE INTO products_category (name) VALUES (%s)"
        cat_id = insert_or_get_id('products_category', 'name', product_category, insert_query=insert_query, insert_values=(clean_value(product_category),))
        product_category_map[product_category] = cat_id

# Product Subcategories
subcat_unique = df[['product_sub_category', 'product_category']].drop_duplicates()
for _, row in subcat_unique.iterrows():
    sub_cat = row['product_sub_category']
    cat_name = row['product_category']
    if pd.isna(sub_cat) or not cat_name:
        continue
    key = (sub_cat, cat_name)
    if key not in product_sub_category_map:
        cat_id = product_category_map.get(cat_name)
        if not cat_id:
            continue
        cursor.execute("INSERT IGNORE INTO product_sub_category (category_id, sub_category) VALUES (%s, %s)", (cat_id, sub_cat))
        conn.commit()
        cursor.execute("SELECT id FROM product_sub_category WHERE category_id=%s AND sub_category=%s", (cat_id, sub_cat))
        subcat_id = cursor.fetchone()[0]
        product_sub_category_map[key] = subcat_id
