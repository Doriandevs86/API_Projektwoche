import psycopg2
from psycopg2 import sql
from config import DATABASE_CONFIG



# Funktion für Verbindung
def connect_to_db():
    return psycopg2.connect(**DATABASE_CONFIG)


# Erstellt die Datenbank, falls sie noch nicht existiert
def create_database():
    connection = connect_to_db()
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DATABASE_CONFIG["dbname"],))
    if not cursor.fetchone():
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DATABASE_CONFIG["dbname"])))

    print(f"Datenbank {DATABASE_CONFIG['dbname']} erfolgreich erstellt.")
    cursor.close()
    connection.close()



# Funktion zum Erstellen der Tabelle "facts"
def create_facts_table():
    connection = connect_to_db()
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

    print('Tabelle "facts" erfolgreich erstellt.')
    cursor.close()
    connection.close()


# Hauptausführung
if __name__ == "__main__":
    create_database()
    create_facts_table()
