# How to get Spotify API

- First go to [developer.spotify.com](https://developer.spotify.com/)'s dashboard
- Get Client ID and Client Secret from a page
- Add `http://localhost/callback` in Edit Settings in Dashboard
- Put this URL 

```
https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&scope=user-read-currently-playing&redirect_uri=http://localhost/callback/
```

 on the browser, you will get URL something like `http://localhost/callback/?code={CODE}  back
- Then, grab Base64 encode of `{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}` and `{CODE}` to request refresh token using:

```sh
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -H "Authorization: Basic {ENCODE}" -d "grant_type=authorization_code&redirect_uri=http://localhost/callback/&code={CODE}" https://accounts.spotify.com/api/token
```

- Now, we can put

```sh
SPOTIFY_CLIENT_ID='____'
SPOTIFY_SECRET_ID='____'
SPOTIFY_REFRESH_TOKEN='____'
```

into `.env` file for development

- Run `python spotify-playing.py` to server via `http://localhost:5000`

Original document by @titipata