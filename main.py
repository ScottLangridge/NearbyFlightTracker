from OpenSky import OpenSky
from secrets import SECRETS

DEBUG_MODE = False
CONST_RANGE = 50

def debug():
    opensky = OpenSky(SECRETS['username'], SECRETS['password'], DEBUG_MODE)
    opensky_response = opensky.get_states_in_range(SECRETS['my_lat'], SECRETS['my_lon'], CONST_RANGE)
    opensky_response.print_report()

if __name__ == '__main__':
    debug()
