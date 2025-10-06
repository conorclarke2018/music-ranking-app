import requests
import base64
import time
import os
from dotenv import load_dotenv

load_dotenv()
# Replace with your Spotify app credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_access_token():
    # Spotify's token endpoint
    auth_url = 'https://accounts.spotify.com/api/token'
    
    # Encode credentials
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post(auth_url, headers=headers, data=data)

    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info['access_token']
        expires_in = token_info['expires_in']  # usually 3600 (1 hour)
        print(f"Access Token: {access_token}")
        return access_token, expires_in
    else:
        raise Exception(f"Failed to get access token: {response.status_code} {response.text}")



def auto_refresh_token():
    while True:
        token, expires_in = get_access_token()

        # Use the token for whatever you need here
        # e.g., set it as a global variable or store it in a database

        print("Token refreshed. Waiting for next refresh...")

        # Sleep for slightly less than an hour (buffer time)
        time.sleep(expires_in - 60)

auto_refresh_token()