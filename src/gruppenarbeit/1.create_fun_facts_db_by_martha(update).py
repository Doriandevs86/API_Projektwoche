import psycopg2
from psycopg2 import sql
from config import DATABASE_CONFIG


# Verbindung zur Datenbank
connection = psycopg2.connect(**DATABASE_CONFIG)
connection.autocommit = True
cursor = connection.cursor()


# Heir wird unsere Datenbank erstellt
cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DATABASE_CONFIG,))
if not cursor.fetchone:
    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DATABASE_CONFIG)))

print(f"Datenbank {DATABASE_CONFIG['dbname']} erfolgreich erstellt.")


# Verbindung zur neu erstellen Datenbank
connection = psycopg2.connect(**DATABASE_CONFIG)
connection.autocommit = True
cursor = connection.cursor()


cursor.execute("""
    DROP TABLE IF EXISTS facts;
    CREATE TABLE facts (
        fact_id SERIAL PRIMARY KEY,
        facts TEXT,
        status TEXT DEFAULT 'nicht gesehen'
    );
""")

print('Tabelle "facts" erfolgreich erstellt')

cursor.close()
connection.close()

