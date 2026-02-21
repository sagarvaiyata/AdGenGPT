import os
from dotenv import load_dotenv
import psycopg2
import boto3

def main() -> None:
    load_dotenv()

    conn_info = {
        "host": os.environ["DB_HOST"],
        "port": int(os.environ.get("DB_PORT", "5432")),
        "dbname": os.environ["DB_NAME"],
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
        # RDS generally supports SSL; require it to avoid plaintext in transit
        "sslmode": os.environ.get("DB_SSLMODE", "require"),
    }

    try:
        with psycopg2.connect(**conn_info) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                result = cur.fetchone()

        print("Connection successful.")
        print("Test query result:", result)

    except Exception as e:
        print("Connection failed.")
        print("Error:", e)

if __name__ == "__main__":
    main()