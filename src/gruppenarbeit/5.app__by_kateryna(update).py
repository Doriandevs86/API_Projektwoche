import customtkinter as ctk
from PIL import Image
import requests
import random

from config import IMAGE_PATH


def fetch_fun_fact():
    status_value = selected_option.get()  # Gesehen oder nicht gesehen abrufen
    response = requests.get(f'http://localhost:8000/filter?status={status_value}')

    if response.status_code == 200:
        response_data = response.json()

        if response_data:
            random_fact = random.choice(response_data)  # Zufälligen Fakt aus der Liste auswählen
            text_box.delete(1.0, "end")
            text_box.insert("end", random_fact['facts'])

            # Status des angezeigten Fakts aktualisieren
            fact_id = random_fact['fact_id']
            update_response = requests.patch(f'http://localhost:8000/facts/update?fact_id={fact_id}')

            if update_response.status_code != 204:
                text_box.insert("end", "\n\nFehler beim Aktualisieren des Status.")
        else:
            text_box.delete(1.0, "end")
            text_box.insert("end", "Keine passenden Fun Facts gefunden.")
    else:
        text_box.delete(1.0, "end")
        text_box.insert("end", f"Keine Fun Facts mit diesem Status gefunden. (Code: {response.status_code})")





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


# Frame für die Textbox
text_frame = ctk.CTkFrame(root, width=300, height=150, corner_radius=20, fg_color='black')
text_frame.grid(column=0, row=0, columnspan=2, padx=10, pady=10)
text_frame.grid_propagate(False)# <----hat eine ähnliche Wirkung auf das # Frame wie resizable auf das root-Fenster


# Textfenster auf dem die fun_facts wiedergegeben werden
text_box = ctk.CTkTextbox(text_frame, width=280, height=150, corner_radius=20 , fg_color='black', text_color='white')
text_box.grid(column=0, row=0, padx=10, pady=10)


# Standartwert für radio_button_auswahl
selected_option = ctk.StringVar(value='nicht gesehen')

# Frame + radio_button
radio_button_frame = ctk.CTkFrame(root, fg_color='black', corner_radius=20, border_width=15, border_color= 'white')
radio_button_frame.grid(column=0, row=1)

radio_button1 = ctk.CTkRadioButton(radio_button_frame,
                                    text='Gesehen',
                                    corner_radius=20,
                                    variable=selected_option,
                                    value='gesehen',
                                    text_color='white',
                                    radiobutton_height=13,
                                    radiobutton_width=13
                                    )
radio_button1.grid(column=0, row=0)

radio_button2 = ctk.CTkRadioButton(radio_button_frame,
                                    text='Ungesehen',
                                    corner_radius=20,
                                    variable=selected_option,
                                    value='nicht gesehen',
                                    text_color='white',
                                    radiobutton_height=13,
                                    radiobutton_width=13
                                    )
radio_button2.grid(column=0, row=1)


# start_button mit Command für API_Abfrage
start_button = ctk.CTkButton(root,
                            text='Start',
                            fg_color='black',
                            text_color='white',
                            corner_radius=20,
                            command=fetch_fun_fact)
start_button.grid(column=1, row=1, padx=10)


root.mainloop()