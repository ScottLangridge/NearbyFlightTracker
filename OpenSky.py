import requests

class OpenSky:
    def __init__(self, username=None, password=None):
        self.root_url = 'https://opensky-network.org/api'

        # If no username and password are provided, opensky will work, but limit you as an anonymous user.
        # https://openskynetwork.github.io/opensky-api/rest.html#limitations
        self.auth = None
        if username and password:
            self.auth = (username, password)


    def get_flights_in_box(self, lamin, lomin, lamax, lomax):
        params = {
            'lamin': lamin,
            'lomin': lomin,
            'lamax': lamax,
            'lomax': lomax,
        }

        response = requests.get(self.root_url + '/states/all', auth=self.auth, params=params)
        return response.json()
