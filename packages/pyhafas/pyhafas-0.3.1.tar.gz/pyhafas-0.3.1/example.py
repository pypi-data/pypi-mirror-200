from collections.abc import Iterable
import datetime
import enum

import pytz

from pyhafas import HafasClient
from pyhafas.profile import DBProfile

client = HafasClient(DBProfile(), debug=True)


def todict(obj):
    """
    Recursively convert a Python object graph to sequences (lists)
    and mappings (dicts) of primitives (bool, int, float, string, ...)
    """
    if isinstance(obj, str):
        return obj
    elif isinstance(obj, enum.Enum):
        return str(obj)
    elif isinstance(obj, dict):
        return dict((key, todict(val)) for key, val in obj.items())
    elif isinstance(obj, Iterable):
        return [todict(val) for val in obj]
    elif hasattr(obj, '__slots__'):
        return todict(dict((name, getattr(obj, name)) for name in getattr(obj, '__slots__')))
    elif hasattr(obj, '__dict__'):
        return todict(vars(obj))
    return obj


# print(todict(client.arrivals(
#     station='8005556',
#     date=datetime.datetime.now(),
#     max_trips=5,
#     direction='8002753'
# )))

j = client.journeys(
        destination="8011160",
        origin="8000105",
        date=datetime.datetime(2022, 11, 20, hour=15, minute=00),
        min_change_time=0,
        max_changes=0,
        max_journeys=2,
    )
#print(j)
print('Searching from', todict(j[1].legs[0])['name'])
jl = client.journeys_from_leg(
        origin=j[1].legs[0],
        destination="8010399",
        #via=['8011160']
    )

for leg in jl[0].legs:
    dt = leg.departure
    if leg.departureDelay:
        dt += leg.departureDelay

    at = leg.arrival
    if leg.arrivalDelay:
        at += leg.arrivalDelay

    print(f"{leg.name} from {leg.origin.name} Pl. {leg.departurePlatform} to {leg.destination.name} Pl. {leg.arrivalPlatform} \t\t {dt.time()} - {at.time()}")
