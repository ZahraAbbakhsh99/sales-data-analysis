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

