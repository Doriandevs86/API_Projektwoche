import customtkinter as ctk
from PIL import Image
import requests
import random


def fetch_fun_fact():
    response = requests.get('http://localhost:8000/facts')

    if response.status_code == 200:
        response_data = response.json()
        fact = response_data[1]

        selected_option.set(fact['status'])

        text_box.delete(1.0, "end")
        text_box.insert("end", fact['facts'])

    else:
        text_box.delete(1.0,"end")
        text_box.insert("end", "Fehler beim Abrufen des Fun Facts")



# Hauptfenster
root = ctk.CTk()
root.geometry('600x300')
root.title('Fun Fact Generator')
root.resizable( width=False, height=False)

# Hintergrund
bg_image=Image.open(r'C:\Users\Admin\Desktop\API_Projektwoche\src\images\hintergrund6.png')
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