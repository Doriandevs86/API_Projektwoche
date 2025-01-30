import requests

def handle_start_button(selected_option, text_box):
    # Beispiel-URL, muss noch angepasst werden! "params" schaut welcher radio_button ausgewählt ist
    api_url = "https://example.com/api/funfacts"
    params = {"status": selected_option.get()}

    response = requests.get(api_url, params=params)
    response.raise_for_status()
    data = response.json()
    fun_fact = data.get("fun_fact", "Kein Fun Fact gefunden.")

    # Textbox aktualisieren
    text_box.delete("1.0", "end")
    text_box.insert("1.0", fun_fact)
