# EnvVarMaster=""

import os
import json
import base64
import requests
from requests import post
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# setup sensitive env vars:
CLIENT_ID = os.environ.get('CLIENT_ID', 'Client ID does not exist')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET', 'Client Secret does not exist')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', 'access token does not exist')

base_url = "https://accounts.spotify.com/api/token"

def get_token():
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = base_url
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)

    json_result = json.loads(result.content)
    # Corrected line to fetch the access token
    token = json_result["access_token"]
    return token


token = get_token()
print(f"The token is: {token}")

# constants:
LIMIT_OF_MAXIMUM_SONGS_TO_DATA_SCRAPE = 5
counter = 1

def is_valid_title(title):
    """Checks if the title text is valid."""
    unwanted_keywords = ['Songwriter', 'Producer']
    return not any(keyword in title for keyword in unwanted_keywords) and len(title) <= 50

user_date_input = input("Which year do you want to Time Travel to? Please type the date in this format: YYYY-MM-DD: ")
print(user_date_input)

response = requests.get(f"https://www.billboard.com/charts/hot-100/{user_date_input}/")
if response.status_code != 200:
    print("Failed to retrieve data")
    exit()

html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

songs_and_artists = []

song_elements = soup.find_all(["h3", "span"], class_=["c-title", "c-label"])

current_title = None

for element in song_elements:
    if 'c-title' in element['class']:
        title_text = element.get_text(strip=True)
        if is_valid_title(title_text):
            current_title = title_text
    elif 'c-label' in element['class'] and current_title:
        artist_name_text = element.get_text(strip=True)
        if not any(char.isdigit() for char in artist_name_text):
            songs_and_artists.append((current_title, artist_name_text))
            current_title = None

print(f"\nSongs and Artists from {user_date_input}:")
for song, artist in songs_and_artists:
    print(f"Song {counter}: {song}, Artist {counter}: {artist}")
    counter += 1
