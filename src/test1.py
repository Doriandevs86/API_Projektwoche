import customtkinter as ctk

root=ctk.CTk()
root.geometry('420x320')
root.title('Fun_Fact_Generator')
root.resizable(width=False,height=False)
root.configure(bg="#1e1e1e")

root.grid_columnconfigure((1,2,3),weight=1) # Ermöglicht es den Spalten 1, 2 und 3, sich automatisch an die Fenstergröße anzupassen


start_btn = ctk.CTkButton(root, text='Start',fg_color="#0084ff", hover_color="#006dcc")
start_btn.grid(column = 0, row = 3, columnspan = 3, pady =15, sticky = 'ew')

text_frame = ctk.CTkTextbox(root)
text_frame.grid(column = 0,row = 0, columnspan = 3, pady =10, padx =10, sticky = 'ew')

text_fenster = ctk.CTkTextbox(text_frame, width = 350, height=100)
text_fenster.grid(column = 0, row = 0,padx =10, pady=10)

radio_btn_frame = ctk.CTkFrame(root)
radio_btn_frame.grid(column = 0, row = 1, columnspan = 3, pady =10)

radio_btn1 = ctk.CTkRadioButton(radio_btn_frame, text='nicht gesehen')
radio_btn1.grid(column = 1, row = 0, padx = 10, pady=5)

radio_btn2 = ctk.CTkRadioButton(radio_btn_frame, text='gesehen')
radio_btn2.grid(column = 0, row = 0, padx = 10, pady =5)



root.mainloop()
