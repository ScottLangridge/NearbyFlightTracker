import requests

from geopy.distance import geodesic
from geopy.point import Point


class OpenSky:
    def __init__(self, username, password):
        self.root_url = 'https://opensky-network.org/api'

        # If no username and password are provided, opensky will work, but limit you as an anonymous user.
        # https://openskynetwork.github.io/opensky-api/rest.html#limitations
        self.auth = None
        if username and password:
            self.auth = (username, password)

        self.assert_connection()

    def assert_connection(self):
        params = {
            'lamin': 0,
            'lomin': 0,
            'lamax': 1,
            'lomax': 1,
        }
        response = requests.get(self.root_url + '/states/all', auth=self.auth, params=params)

        assert response.status_code != 401, f'OpenSky assert_connection received 401 - Unauthorized. Likely incorrect login details.'
        assert response.status_code == 200, f'OpenSky assert_connection received unexpected status: {response.status_code}'

    # Note, actually returns flights in a box of dimensions range_km.
    # Flights in the corners of the box will be further away than range_km.
    def get_flights_in_range(self, lat, lon, range_km):
        origin = Point(lat, lon)

        north_point = geodesic(kilometers=range_km).destination(origin, 0)  # North (max latitude)
        south_point = geodesic(kilometers=range_km).destination(origin, 180)  # South (min latitude)
        east_point = geodesic(kilometers=range_km).destination(origin, 90)  # East (max longitude)
        west_point = geodesic(kilometers=range_km).destination(origin, 270)  # West (min longitude)

        min_lat = south_point.latitude
        max_lat = north_point.latitude
        min_lon = west_point.longitude
        max_lon = east_point.longitude

        return self.get_flights_in_box(min_lat, min_lon, max_lat, max_lon)

    def get_flights_in_box(self, lamin, lomin, lamax, lomax):
        params = {
            'lamin': lamin,
            'lomin': lomin,
            'lamax': lamax,
            'lomax': lomax,
        }

        response = requests.get(self.root_url + '/states/all', auth=self.auth, params=params)
        return response.json()
