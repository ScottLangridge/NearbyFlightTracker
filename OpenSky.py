import requests
from geopy.distance import geodesic
from geopy.point import Point

import utils
from utils import nullable_datetime


class OpenSkyResponse:
    def __init__(self, response_json):
        # See https://openskynetwork.github.io/opensky-api/rest.html#response
        self.time = nullable_datetime(response_json['time'])
        self.states = []
        if response_json['states']:
            self.states = [OpenSkyState(state) for state in response_json['states']]

    def __str__(self):
        return f'OpenSkyResponse | time: {self.time} | aircraft count: {len(self.states)}'

    def print_report(self):
        print(f'====================')
        print(f'OpenSkyResponse from {self.time}')

        print(f'Aircraft:')
        for state in self.states:
            print(
                f'  - {state.callsign} | '
                f'lat: {state.latitude} '
                f'lon: {state.longitude} '
                f'alt: {state.baro_altitude} '
                f'vel: {state.velocity} '
                f'hdg: {state.true_track} '
            )
        print(f'====================')


class OpenSkyState:
    def __init__(self, state_json):
        # See https://openskynetwork.github.io/opensky-api/rest.html#response for definitions
        self.icao24 = state_json[0]
        self.callsign = state_json[1]
        self.origin_country = state_json[2]
        self.time_position = nullable_datetime(state_json[3])
        self.last_contact = nullable_datetime(state_json[4])
        self.longitude = state_json[5]
        self.latitude = state_json[6]
        self.baro_altitude = state_json[7]
        self.on_ground = state_json[8]
        self.velocity = state_json[9]
        self.true_track = state_json[10]
        self.vertical_rate = state_json[11]
        self.sensors = state_json[12]
        self.geo_altitude = state_json[13]
        self.squawk = state_json[14]
        self.spi = state_json[15]

        # OpenSky is not providing one of these values. Since I can't tell which, I am commenting them out to avoid
        # confusion. If I ever need them I'll figure out which is missing and add the other back in.
        # self.position_source = state_json[16]
        # self.category = state_json[17]

    def __str__(self):
        return self.callsign


class OpenSky:
    def __init__(self, username, password, debug_mode=False):
        self.root_url = 'https://opensky-network.org/api'

        # If no username and password are provided, opensky will work, but limit you as an anonymous user.
        # https://openskynetwork.github.io/opensky-api/rest.html#limitations
        self.auth = None
        if username and password:
            self.auth = (username, password)
        self.assert_connection()

        # Debug mode gives mock data instead of calling to the API
        self.debug_mode = debug_mode

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
        if self.debug_mode:
            return OpenSkyResponse(utils.debug_opensky_response(5))

        params = {
            'lamin': lamin,
            'lomin': lomin,
            'lamax': lamax,
            'lomax': lomax,
        }

        response = requests.get(self.root_url + '/states/all', auth=self.auth, params=params)
        return OpenSkyResponse(response.json())
