import os
from dotenv import load_dotenv
import psycopg2

load_dotenv(override=True)
url = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(url, sslmode="require")
    cur = conn.cursor()
    cur.execute("SELECT 1")
    print("✅ Запрос выполнен:", cur.fetchone())
    conn.close()
except Exception as e:
    print("❌ Ошибка:", e)