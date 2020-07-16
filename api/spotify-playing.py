from flask import Flask, Response, jsonify
from base64 import b64encode

import requests
import json
import os


SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET_ID = os.getenv("SPOTIFY_SECRET_ID")
SPOTIFY_REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")

SPOTIFY_URL_REFRESH_TOKEN = "https://accounts.spotify.com/api/token"
SPOTIFY_URL_NOW_PLAYING = "https://api.spotify.com/v1/me/player/currently-playing"

app = Flask(__name__)


def get_authorization():

    return b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_SECRET_ID}".encode()).decode("ascii")


def refresh_token():

    data = {
        "grant_type": "refresh_token",
        "refresh_token": SPOTIFY_REFRESH_TOKEN,
    }

    headers = {"Authorization": "Basic {}".format(get_authorization())}

    response = requests.post(SPOTIFY_URL_REFRESH_TOKEN, data=data, headers=headers)
    repsonse_json = response.json()

    return repsonse_json["access_token"]


def get_now_playing():

    token = refresh_token()

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(SPOTIFY_URL_NOW_PLAYING, headers=headers)

    if response.status_code == 204:
        return {}

    repsonse_json = response.json()
    return repsonse_json


def get_svg_template():

    svg = """
        <svg width="200" height="320" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
            <foreignObject width="200" height="320">
                <div xmlns="http://www.w3.org/1999/xhtml">
                    <style>
                        .playing {{ font: bold 18px serif; color: red; text-align: center; }}
                        .artist {{ font: bold 18px serif; text-align: center; }}
                        .song {{ font: 16px serif; text-align: center; }}
                    </style>
                    {}
                </div>
            </foreignObject>
        </svg>
    """
    return svg


def load_image_b64(url):

    resposne = requests.get(url)
    return b64encode(resposne.content).decode("ascii")


def make_svg(data):

    template = get_svg_template()

    if data == {}:
        content = """
            <div class="playing">Nothing playing on Splotify</div>
        """
        return template.format(content)

    content = """
        <div class="playing">Now playing on Splotify</div>
        <br />
        <div class="artist">{}</div>
        <div class="song">{}</div>
        <br />
        <a href="{}" target="_BLANK">
            <img src="data:image/png;base64, {}" height="200"/>
        </a>
        """

    item = data["item"]

    """
    print(json.dumps(item))
    print(item["artists"][0]["name"])
    print(item["external_urls"]["spotify"])
    print(item["album"]["images"][0]["url"])
    """

    img = load_image_b64(item["album"]["images"][1]["url"])
    content_rendered = content.format(
        item["artists"][0]["name"], item["name"], item["external_urls"]["spotify"], img,
    )

    return template.format(content_rendered)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):

    # TODO: caching

    data = get_now_playing()
    svg = make_svg(data)

    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "s-maxage=1"

    return resp


if __name__ == "__main__":
    app.run(debug=True)
