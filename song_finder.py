import urllib
import requests
import base64
import json


ACCESS_TOKEN=""

def _make_authorization_headers(client_id, client_secret):
    #auth_header = base64.b64encode(six.text_type(client_id + ':' + client_secret).encode('ascii'))
    auth_header = base64.standard_b64encode(client_id + ':' + client_secret)
    return {'Authorization': 'Basic %s' % auth_header.decode('ascii')}

def get_authorization_code(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/authorize/?client_id={}&response_type=code&redirect_uri=http://127.0.0.1:8000"
    response = requests.get(auth_url)
    print response.text
    return response.text


def make_authorized_request(url, verb="get"):
    token = {"access_token": ACCESS_TOKEN}
    if not ACCESS_TOKEN:
        client_id = "730272e359a0489193deb78388e6923c"
        client_secret = "a358b739317d40fea4f41fbe2154c321"

        #get_authorization_code(client_id, client_secret)

        grant_type = "client_credentials"
        body_params = {"grant_type": grant_type}

        # authorize first
        auth_url = "https://accounts.spotify.com/api/token"
        auth_credentials = _make_authorization_headers(client_id, client_secret)
        token_response = requests.post(auth_url, data=body_params, auth = (client_id, client_secret))
        #token_response = requests.post(auth_url, data=body_params, headers=auth_credentials)
        token = token_response.json()

    # make the request
    auth_headers = {"Authorization": "Bearer {}".format(token['access_token'])}
    if verb == "get":
        return requests.get(url, headers=auth_headers)
    elif verb == "post":
        return requests.post(url, headers=auth_headers)


def get_song(title="", artist=""):
    song  = ""
    url = ""

    # url encode title and artist
    title_encoded = urllib.quote(title)
    artist_encoded = urllib.quote(artist)

    if title != "":
        url = "https://api.spotify.com/v1/search?q={}&type=track".format(title_encoded)
    else:
        url = "https://api.spotify.com/v1/search?q={}&type=artist".format(artist_encoded)
    
    response = make_authorized_request(url)
    json_response = response.json()
    songs = json_response['tracks']['items']
    for song in songs:
        print "\n\n-----------------"
        print json.dumps(song, indent=4)

        # if both are provided then find based on artist
        if title and artist:
            artist_names = [a['name'] for a in song['artists']]
            print "Title: {}\nArtists: {}".format(song['name'], artist_names)
            if artist in artist_names:
                return song
    return songs 


if __name__ == '__main__':
    song = raw_input("Enter a song title: ")
    get_song(title=song)
