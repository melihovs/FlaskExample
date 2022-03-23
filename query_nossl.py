import psycopg2

from config_db import host, user, password, db_name

try:
    # DB connection
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        sslmode='disable'
    )
    # the cursor for performing database operations
    curs = connection.cursor()
    curs.execute("SELECT version();")
    print(f"Server version: {curs.fetchone()}")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)

finally:
    if connection:
        curs.close()
        connection.close()
        print("[INFO] PostgreSQL connection close.")
