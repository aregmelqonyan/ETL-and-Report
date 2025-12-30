import os
from functools import wraps
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


def with_db_cursor(commit=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            conn = None
            cur = None
            try:
                conn = psycopg2.connect(
                    dbname=DB_NAME,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    host=DB_HOST,
                    port=DB_PORT,
                )
                cur = conn.cursor()
                result = func(cur, *args, **kwargs)
                if commit:
                    conn.commit()
                return result
            except Exception as e:
                if conn:
                    conn.rollback()
                print("Database error:", e)
                raise
            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
        return wrapper
    return decorator
