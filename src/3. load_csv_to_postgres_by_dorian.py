import csv
import psycopg2
import os

pw = input('Bitte gib dein Passwort ein:')

def connect_to_db():
    return psycopg2.connect(
        host='localhost',
        port=5432,
        user='postgres',
        password=pw,
        dbname='funfact_db'
    )

def load_csv_to_facts_table(csv_file):
    conn = connect_to_db()
    cursor = conn.cursor()

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, quotechar='"', delimiter=',')

        # Überspringe die erste Zeile (Header)
        next(reader)

        rows = []

        # Zeilen einlesen
        for row in reader:
            rows.append((row[0],))

    # Setze die Spalte 'facts' als Ziel für das Insert
    insert_query = "INSERT INTO facts (facts) VALUES (%s)"

    # Einfügen Daten in die Tabelle
    cursor.executemany(insert_query, rows)

    # Änderungen speichern und Verbindung schließen
    conn.commit()
    cursor.close()
    conn.close()

    print("Import abgeschlossen. Verbindung zur Datenbank geschlossen.")

load_csv_to_facts_table(csv_file='fakten.csv')
