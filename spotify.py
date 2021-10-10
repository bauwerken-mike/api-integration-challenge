import urllib.parse
import requests
import base64

#api to search for artist
main_api = "https://api.spotify.com/v1/search?"
#client authentication keys (key and secret key)
client_id = ""
client_secret =""
#encoding of keys
client_creds = f"{client_id}:{client_secret}"
client_creds_b64 = base64.b64encode(client_creds.encode())
#setup headers
authurl = "https://accounts.spotify.com/api/token"
method = "POST"
token_data = {"grant_type": "client_credentials"}
token_headers = {"Authorization": f"Basic {client_creds_b64.decode()}"}
#send for authentication token
r = requests.post(authurl, data=token_data, headers=token_headers)
valid_request = r.status_code in range (200, 299)

#check if request is valid
if valid_request:
    #get access token from response, add to headers
    access_response_data = r.json()
    access_token = access_response_data["access_token"]
    query_headers = {'Authorization': f"Bearer {access_token}"}
    #user input
    artist = input("Artist to search for: ")
    #request artists based on user input
    url = main_api + urllib.parse.urlencode({"q":artist, "type":"artist"})

    r2 = requests.get(url, headers=query_headers)
    json_data = r2.json()
    valid_artists_request = r2.status_code in range (200, 299)
    teller = 0
    #check if request is valid
    if valid_artists_request:
        print("*"*120)
        print(f'{"Name":<40} {"Genres":<70} {" Popularity":<10}')
        #read out name, genres and popularity for every artist returned
        for each in json_data['artists']['items']:
            artist_name = json_data["artists"]['items'][teller]['name']
            artist_genres = json_data["artists"]['items'][teller]['genres']
            artist_popularity = json_data["artists"]['items'][teller]['popularity']
            teller += 1
            print(f'{artist_name:<40} {str(artist_genres):<70}  {str(artist_popularity):<10}')
        print("*"*120)
else:
    print("**********************************************")

    print("Status Code: " + str(r.status_code) + "; Something went wrong.")

    print("**********************************************\n")