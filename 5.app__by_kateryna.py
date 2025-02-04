import customtkinter as ctk
import psycopg2
from PIL import Image
import requests
import random
import textwrap

from config import IMAGE_PATH, DATABASE_CONFIG


''' FUNKTIONEN '''

# Variable, um die fact_id des angezeigten Fun Facts zu speichern
current_fact_id = None


# Funktion zum Abrufen eines Fun Facts
def fetch_fun_fact():
    global current_fact_id  # Auf die globale Variable zugreifen
    status_value = selected_option.get()  # Gesehen oder nicht gesehen abrufen

    response = requests.get(f'http://localhost:8000/filter?status={status_value}')
    if response.status_code == 200:
        response_data = response.json()

        if response_data:
            random_fact = random.choice(response_data)  # Zufälligen Fakt aus der Liste auswählen
            text_box.delete(1.0, "end")
            text_box.insert("end", random_fact['facts'])

            # Verwende textwrap, um den Text zu formatieren
            wrapped_text = textwrap.fill(random_fact['facts'], width=150)
            text_box.delete(1.0, "end")
            text_box.insert("end", wrapped_text)

            # Speichern der fact_id des angezeigten Fakts
            current_fact_id = random_fact['fact_id']

            # Status des angezeigten Fakts aktualisieren
            fact_id = random_fact['fact_id']
            update_response = requests.patch(f'http://localhost:8000/facts/update?fact_id={fact_id}')

        else:
            text_box.delete(1.0, "end")
            text_box.insert("end", "Keine passenden Fun Facts gefunden.")
    else:
        text_box.delete(1.0, "end")
        text_box.insert("end", f"Keine Fun Facts mit diesem Status gefunden. (Code: {response.status_code})")





# Funktion zum Wechseln des Status zwischen "favourite" und "nicht gesehen"
def toggle_favourite():
    global current_fact_id  # Auf die fact_id zugreifen
    if current_fact_id is None:
        text_box.delete(1.0, "end")
        text_box.insert("end", "Kein Fun Fact ausgewählt!")
        return

    # API-Anfrage zum Wechseln des Status
    response = requests.patch(f'http://localhost:8000/facts/favourite?fact_id={current_fact_id}')

    if response.status_code == 200:
        updated_fact = response.json()  # Die aktualisierten Daten des Fakts abrufen
        new_status = updated_fact['status']

        # Textfeld mit dem neuen Status aktualisieren
        text_box.delete(1.0, "end")
        text_box.insert("end", f"Fun Fact ist nun {new_status}: {updated_fact['facts']}")
    else:
        text_box.delete(1.0, "end")
        text_box.insert("end", f"Fehler beim Aktualisieren des Status (Code: {response.status_code})")







def get_funfact_stats():
    """ Berechnet die Gesamtzahl aller Fun Facts und den prozentualen Anteil 'gesehen'/'nicht gesehen'. """

    connection = psycopg2.connect(**DATABASE_CONFIG)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM facts;")
    total_facts = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM facts WHERE status = 'gesehen';")
    seen_facts = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM facts WHERE status = 'nicht gesehen';")
    unseen_facts = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM facts WHERE status = 'favourite';")
    favourite_facts = cursor.fetchone()[0]

    seen_percentage = round((seen_facts / total_facts) * 100, 2) if total_facts > 0 else 0
    unseen_percentage = round((unseen_facts / total_facts) * 100, 2) if total_facts > 0 else 0
    favourite_percentage = round((favourite_facts / total_facts) * 100, 2) if total_facts > 0 else 0

    cursor.close()
    connection.close()

    return {
        "All Fun Facts": f"{total_facts}\n\n",
        "Fun Facts seen": f"{seen_facts} ({seen_percentage}%)",
        "Fun Facts unseen": f"{unseen_facts} ({unseen_percentage}%)",
        "Favourite Fun Facts": f"{favourite_facts} ({favourite_percentage}%)"
    }


# Funktion zur Anzeige der Statistik
def toggle_statistics():
    if stats_label.winfo_ismapped():  # Prüfen, ob das Label sichtbar ist
        stats_label.grid_remove()  # Statistik ausblenden
    else:
        stats = get_funfact_stats()  # Statistiken abrufen
        stats_text = "\n".join([f"{key}: {value}" for key, value in stats.items()])
        stats_label.configure(text=stats_text)  # Text im Label aktualisieren
        stats_label.grid(column=1, row=1, padx=10, pady=10)  # Statistik einblenden



# Hauptfenster
root = ctk.CTk()
root.geometry('600x300')
root.title('Fun Fact Generator')
root.resizable( width=False, height=False)


# Hintergrund
bg_image=Image.open(IMAGE_PATH)
bg_ctk_image=ctk.CTkImage(light_image=bg_image,size=(600,300))
bg_label = ctk.CTkLabel(root, image = bg_ctk_image, text = "")
bg_label.place(relwidth=1, relheight=1)


# Theme für das Hauptfenster
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')


''' FRAMES '''



# Frame für die Textbox
text_frame = ctk.CTkFrame(root, width=300, height=150, corner_radius=20, fg_color='black')
text_frame.grid(column=0, row=0, padx=10, pady=10)
text_frame.grid_propagate(False)

# Option_Frame (Start, Dropdown, Statistik...)
option_frame = ctk.CTkFrame(root, fg_color='black', corner_radius=20, border_color= 'black')
option_frame.grid(column=0, row=1, padx=10, pady=10)


''' Textfenster '''



# Textfenster auf dem die fun_facts wiedergegeben werden
text_box = ctk.CTkTextbox(text_frame, width=280, height=150, corner_radius=20 , fg_color='black', text_color='white')
text_box.grid(column=0, row=0, padx=10, pady=10)
text_box.configure(wrap="word")


# Statistik-Fenster (anfangs versteckt)
stats_label = ctk.CTkLabel(root, text="", fg_color="black", text_color="white", corner_radius=20)
stats_label.grid(padx=10, pady=10)
stats_label.grid_remove()  # Verstecken


''' BUTTONS '''



# Standartwert für dropdown_auswahl
selected_option = ctk.StringVar(value='nicht gesehen')


dropdown_menu = ctk.CTkComboBox(option_frame,
                                values=["gesehen", "nicht gesehen", "favourite"],
                                variable=selected_option,
                                fg_color="black",  # Hintergrund des Hauptfelds
                                text_color="white",  # Textfarbe des Hauptfelds
                                dropdown_fg_color="black",  # Hintergrundfarbe der Dropdown-Liste
                                dropdown_text_color="white",  # Textfarbe der Dropdown-Elemente
                                dropdown_hover_color="#1F6AA5",
                                button_color='#1F6AA5',
                                button_hover_color='#1F6AA5',
                                border_color='#1F6AA5',
                                corner_radius=20,
                                state='readonly')
dropdown_menu.grid(column=1, row=1, padx=5, pady=5)


# start_button mit Command für API_Abfrage
start_button = ctk.CTkButton(option_frame,
                            text='Start',
                            fg_color='black',
                            text_color='white',
                            corner_radius=20,
                            command=fetch_fun_fact)
start_button.grid(column=0, row=1, padx=5, pady=5)


# statistik_button mit Command für API_Abfrage
statistik_button = ctk.CTkButton(option_frame,
                            text='Statistik',
                            fg_color='black',
                            text_color='white',
                            corner_radius=20,
                            command=toggle_statistics)
statistik_button.grid(column=0, row=3, padx=5, pady=5)


# Favourite_button
favourite_button = ctk.CTkButton(option_frame,
                            text='Favourite',
                            fg_color='black',
                            text_color='white',
                            corner_radius=20,
                            command=toggle_favourite
                            )
favourite_button.grid(column=0, row=2, padx=5, pady=5)

root.mainloop()