import requests

"""
    This file asks the user to enter a location, searches for it, asks for confirmation and returns coordinates.
    Interaction is through the Terminal.
"""

def queryLocation(query):
    url = "https://nominatim.openstreetmap.org/search"
    payload = {'q': query, 'format': 'json'}
    headers= {'user-agent': 'eautarkos/0.0.1'}
    response = requests.get(url=url, params=payload, headers=headers)    
    queryresult = response.json()

    if response.status_code != requests.codes.ok:
        print("The server did not respond.")
        raise ConnectionError
    
    if len(queryresult) == 0:
        print("Location could not be found!")
        queryLocation()

    return queryresult

def selectLocation(queryresult):

    print("The following location(s) have been found for your request. Please confirm yours.")
    for entry, index in zip(queryresult, range(len(queryresult))):
        print(f"{index}: {entry.get('display_name')}")
    location = queryresult[int(input("Chosen location (enter number): "))]

    lat = round(float(location.get('lat')), 2)
    lon = round(float(location.get('lon')), 2)

    return (lat, lon)   