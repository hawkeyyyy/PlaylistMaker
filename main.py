from dotenv import load_dotenv
from requests import post, get
import os
import base64
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")  # Corrected line

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64 + " ",  # Include a space after "Basic"
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result.get("access_token")
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"

    query_url = url + "?" + query  # Corrected line (added "?")
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result)==0:
        print("no result")
        return None
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    if "tracks" in json_result:
        return json_result["tracks"]
    else:
        return None


token = get_token()
artistname = input("Enter the name of the artist: ")
result = search_for_artist(token,artistname )
if result:
    artist_id = result["id"]
    songs = get_songs_by_artist(token, artist_id)
    if songs:
        print("Top Tracks for "+artistname)
        for idx, song in enumerate(songs):
            print(f"{idx + 1}. {song['name']}")
    else:
        print("No top tracks found for AC/DC.")
else:
    print("AC/DC not found in search results.")