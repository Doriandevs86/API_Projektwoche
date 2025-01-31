import csv
import psycopg2
from config import DATABASE_CONFIG, CSV_PATH

def connect_to_db():
    return psycopg2.connect(**DATABASE_CONFIG)

def load_csv_to_facts_table():
    conn = connect_to_db()
    cursor = conn.cursor()

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Header überspringen

        rows = []
        for row in reader:
            rows.append((row[0],))

    # Daten in die Tabelle einfügen
    insert_query = "INSERT INTO facts (facts) VALUES (%s)"
    cursor.executemany(insert_query, rows)

    conn.commit()
    cursor.close()
    conn.close()
    print("Import abgeschlossen. Verbindung zur Datenbank geschlossen.")

load_csv_to_facts_table(csvfile=CSV_PATH)