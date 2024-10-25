import requests
import requests_cache

def queryLocation():
    query = str(input("Location: "))

    # requests_cache.install_cache(cache_name='location_cache', backend='sqlite', expire_after=3600)
    url = "https://nominatim.openstreetmap.org/search"
    payload = {'q': query, 'format': 'json'}
    headers= {'user-agent': 'eautarkos/0.0.1'}
    response = requests.get(url=url, params=payload, headers=headers)    
    queryresult = response.json()

    if response.status_code != requests.codes.ok:
        print("Lookup failed, try again.")
        queryLocation()
        return
    else:
        if len(queryresult) == 0:
            print("Location could not be found!")
        else:
            print("The following location(s) have been found for your request. Please confirm yours.")
            for entry, index in zip(queryresult, range(len(queryresult))):
                print(f"{index}: {entry.get('display_name')}, {entry.get('lat')}, {entry.get('lon')}")
            location = queryresult[int(input("Chosen location (enter number): "))]

    lat = round(float(location.get('lat')), 2)
    lon = round(float(location.get('lon')), 2)

    return (lat, lon)   