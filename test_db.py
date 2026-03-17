import psycopg2
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Explicitly grab variables
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")

print(f"Attempting to connect to {dbname} on {host}:{port} as {user}...")

# Connect
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)

print("Status: Connected.")

# Use the cursor to prove it
cur = conn.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
tables = cur.fetchall()

print("Tables found in database:")
for table in tables:
    print(f"- {table[0]}")

cur.close()
conn.close()