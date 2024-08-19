import datetime
import json


def nullable_datetime(epoch):
    if epoch is None:
        return None
    else:
        return datetime.datetime.fromtimestamp(epoch)


def debug_states_all_response(aircraft_count=50):
    with open('debug_states_all.json', 'r') as f:
        response = json.loads(f.read())
    response['states'] = response['states'][:aircraft_count]
    return response
