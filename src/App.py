import ImageTk
import customtkinter as ctk
#from PIL.Image import Image
from PIL import Image, ImageTk


# Hauptfenster
root = ctk.CTk()
root.geometry('600x300')
root.title('Fun Fact Generator')
root.resizable( width=False, height=False)

# Hintergrund
bg_image=Image.open('hintergrund6.png')
bg_ctk_image=ctk.CTkImage(light_image=bg_image,size=(600,300))
bg_label = ctk.CTkLabel(root, image = bg_ctk_image, text = "")
bg_label.place(relwidth=1, relheight=1)

# Theme für das Hauptfenster
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')


# Frame für die Textbox
text_frame = ctk.CTkFrame(root, width=300, height=150, fg_color='black')
text_frame.grid(column=0, row=0, columnspan=2, padx=10, pady=10)
text_frame.grid_propagate(False)# <----hat eine ähnliche Wirkung auf das # Frame wie resizable auf das root-Fenster


# Textfenster auf dem die fun_facts wiedergegeben werden
text_box = ctk.CTkTextbox(text_frame, width=200, height=150, fg_color='black', text_color='white')
text_box.grid(column=0, row=0, padx=10, pady=10)


# Standartwert für radio_button_auswahl
selected_option = ctk.StringVar(value='nicht gesehen')

# Frame + radio_button
radio_button_frame = ctk.CTkFrame(root, fg_color='black')
radio_button_frame.grid(column=0, row=1)

radio_button1 = ctk.CTkRadioButton(radio_button_frame,
                                    text='Gesehen',
                                    variable=selected_option,
                                    value='gesehen',
                                    text_color='white')
radio_button1.grid(column=0, row=0)

radio_button2 = ctk.CTkRadioButton(radio_button_frame,
                                    text='Ungesehen',
                                    variable=selected_option,
                                    value='nicht gesehen',
                                    text_color='white')
radio_button2.grid(column=0, row=1)


# start_button mit Command für API_Abfrage
start_button = ctk.CTkButton(root, text='Start', fg_color='black', text_color='white')
start_button.grid(column=1, row=1, padx=10)


root.mainloop()