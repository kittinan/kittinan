from flask import Flask, Response

from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import SpotifyOAuth

import spotipy
import json

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    username = "21jsj34glwsu3dboqjpqzm2sa"
    scope = "user-read-currently-playing"

    auth_manager = SpotifyOAuth(username=username, scope=scope)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return Response(json.dumps(sp.current_user_playing_track()), mimetype="text/json")