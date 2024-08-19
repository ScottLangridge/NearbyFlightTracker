from OpenSky import OpenSky
from secrets import SECRETS


CONST_RANGE = 10

def debug():
    api = OpenSky(SECRETS['username'], SECRETS['password'])
    print(api.get_flights_in_range(SECRETS['my_lat'], SECRETS['my_lon'], CONST_RANGE))


if __name__ == '__main__':
    debug()
