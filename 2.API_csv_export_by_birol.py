import requests
import csv
import os
import time

from config import CSV_PATH

# API_URL
url = 'https://uselessfacts.jsph.pl/api/v2/facts/random'

# Anzahl der Fakten die gesucht werden sollen
num_facts = 356

file_path = CSV_PATH
os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
facts_set = set()

# CSV erstellen ohne Anführungszeichen
with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['facts'])  # Header hinzufügen

    facts_collected = 0
    while facts_collected < num_facts:
        response = requests.get(url)

        if response.status_code == 200:
            fact = response.json()['text']
            if fact not in facts_set:
                print(f"Zufälliger Fakt: {fact}")
                writer.writerow([fact])  # Nur der Fakt wird gespeichert
                facts_set.add(fact)
                facts_collected += 1
            else:
                print("Doppelt gefundener Fakt, überspringe...")
        else:
            print(f"Fehler beim Abrufen des Fakts: {response.status_code}. Versuche in 5 Sekunden...")
            time.sleep(5)
