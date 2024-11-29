import json
from requests import get, post
from dotenv import load_dotenv
import os
import base64

# ENV VARIABLES

load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# FUNCTIONS

def get_token():
    # client id + secret encoded in base 64 sent to get auth token
    auth_string = SPOTIFY_CLIENT_ID + ":" + SPOTIFY_CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {"grant_type" : "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    # debugging
    # if result.status_code == 200:
    #     print("Access token is valid!")
    #     print(result.json())  # Optional: Print user profile data
    # elif result.status_code == 401:
    #     print("Access token is invalid or expired.")
    #     print(result.json())  # Optional: Check error details
    # else:
    #     print(f"Unexpected response: {result.status_code}")
    #     print(result.json())

    # print(token)
    return token

def get_auth_header(token):
    return{"Authorization" : "Bearer " + token}

# testing API, not useful for project
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    # type is comma sep list of things i am looking for
    # limit = 1 for most popular
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No Artist with this name exists...")
        return None
    return json_result[0]

def get_songs_by_Artist(token, artist_id):
    url = url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_playlist_tracks(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    if len(json_result) == 0:
        print("No playlist with this ID exists...")
        return None
    
    song_list = []
    for track in json_result:
        song_id = track["track"]["id"]
        song_list.append(song_id)
    
    return song_list

def get_tracks_audio_features(token, song_ids):
    song_url = ""
    for song in song_ids:
        song_url += song + "%2C"
    url = f"https://api.spotify.com/v1/audio-features?ids={song_url}"
    # print(url)
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    return result
    # json_result = json.loads(result.content)
    # return json_result


# MAIN 

token = get_token()
result = search_for_artist(token, "Ariana")
print(result["name"])
artist_id = result["id"]
songs = get_songs_by_Artist(token, artist_id)

for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")
    
playlist_id = '1aRVHcrkoX57qJF09wTime'
song_ids = get_playlist_tracks(token, playlist_id)
print(song_ids)
songs_info = get_tracks_audio_features(token, song_ids)
print(songs_info)

# spotify API depreciated the audio-features function, so now we cannot use real-user data and look up song values
# https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api




    
