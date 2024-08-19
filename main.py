from OpenSky import OpenSky


def debug():
    api = OpenSky()
    print(api.get_flights_in_box(45.8389, 5.9962, 47.8229, 10.5226))


if __name__ == '__main__':
    debug()
