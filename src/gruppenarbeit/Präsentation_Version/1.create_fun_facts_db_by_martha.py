import psycopg2
from psycopg2 import sql
import pyautogui


pw = pyautogui.password('Bitte gib dein Passwort ein:', title= 'Password-Abfrage')

host = "localhost"
port = "5432"
user = "postgres"
password = pw
dbname = "funfact_db"

# Verbindung zur PostgreSQL-Server-Datenbank herstellen (normalerweise zur 'postgres'-Datenbank)
connection = psycopg2.connect(
    dbname="postgres",
    host=host,
    port=port,
    user=user,
    password=password
)

connection.autocommit = True
cursor = connection.cursor()

#"SELECT 1 FROM pg_database WHERE ...." ==  create DB if not exist
cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
if not cursor.fetchone():
    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))

print(f"Datenbank {dbname} erfolgreich erstellt.")

connection = psycopg2.connect(host=host,
                              port=port,
                              user=user,
                              password=password,
                              dbname=dbname
)
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

