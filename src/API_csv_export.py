import requests
import csv
import os
import time

api_key = '1tp7yPNOP31Gano9R+Vc3w==AXWMvVp68JudOYG1'
url = 'https://uselessfacts.jsph.pl/api/v2/facts/random'
headers = {
    'Authorization': f'Bearer {api_key}'}

num_facts = 500
file_path = r'C:\Users\Admin\Documents\kursverlauf\07_Python_für_Datenanalysten\Tag_10\Tutorium\Krypto\API_Projektwoche\src\util\fakten.csv'
file_exists = os.path.exists(file_path)
facts_set = set()

with open(file_path, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(['Fakt'])

    facts_collected = 0
    while facts_collected < num_facts:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            fact = response.json()['text']
            if fact not in facts_set:
                print(f"Zufälliger Fakt: {fact}")
                writer.writerow([fact])
                facts_set.add(fact)
                facts_collected += 1
            else:
                print("Doppelt gefundener Fakt, überspringe...")
        else:
            print(f"Fehler beim Abrufen des Fakts: {response.status_code}. Versuche in 5 Sekunden...")
            time.sleep(5)

