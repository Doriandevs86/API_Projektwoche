import requests

api_key = '1tp7yPNOP31Gano9R+Vc3w==AXWMvVp68JudOYG1'
url = 'https://uselessfacts.jsph.pl/api/v2/facts/random'
headers = {
    'Authorization': f'Bearer {api_key}'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    fact = response.json()['text']
    print(f"Zufälliger Fakt: {fact}")
else:
    print("Fehler beim Abrufen des Fakts:", response.status_code)

