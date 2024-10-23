# import osmium
from cds_requests import cmip6 

def main():
    # Ask for a location. To be replaced by a request to OSM!
    long = float(input("Longitude: "))
    lat = float(input("Latitude: "))

    # Ask for container size
    storage_size = float(input("Volume of existing storage tank (type 0 if none): "))
    roof_surface = float(input("Land surface of collecting roof: "))
    people = int(input("Number of people in the household: "))

    # Retrive meteorological data
    cmip6(lat, long)

    # Start calculations

if __name__ == "__main__":
    main()