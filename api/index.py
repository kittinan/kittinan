from flask import Flask, Response

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import SpotifyOAuth

import json

app = Flask(__name__)

username = "21jsj34glwsu3dboqjpqzm2sa"
scope = "user-read-currently-playing"

auth_manager = SpotifyOAuth(username=username, scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)

@app.route('/')
def index():
    return Response("Kittinan API")

@app.route('/spotify-playing')
def spotify():
    print(sp.current_user_playing_track())
    return Response(json.dumps(sp.current_user_playing_track()))


if __name__ == "__main__":
    app.run(debug=True)