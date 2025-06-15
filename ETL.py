import mysql.connector

# DB Connection
conn = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_pass',
    database='sale_db'
)
cursor = conn.cursor(buffered=True)



