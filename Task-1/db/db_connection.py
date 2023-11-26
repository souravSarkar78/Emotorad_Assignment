import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()


try:
    conn = psycopg2.connect(
            host="localhost",
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])
    print("Connection established!")
except:
    print("Invalid configuration!")