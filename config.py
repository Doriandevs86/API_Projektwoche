import os
import pyautogui

# Basisverzeichnis des Projekts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pfade
CSV_PATH = os.path.join(BASE_DIR, 'src', 'fakten.csv')
IMAGE_PATH = os.path.join(BASE_DIR, 'src', 'images', 'hintergrund6.png')

# Datenbankkonfiguration (ohne Passwort)
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'user': 'postgres',
    'dbname': 'funfact_db'}

# Passwort zur Laufzeit abfragen
def get_db_password():
    return pyautogui.password('Bitte gib dein PostgreSQL-Passwort ein:', title='Passwort-Abfrage')

# Passwort zur Konfiguration hinzufügen
DATABASE_CONFIG['password'] = get_db_password()