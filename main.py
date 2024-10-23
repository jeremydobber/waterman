import zipfile
from datetime import date
from cds_requests import cmip6
from nominatim_requests import queryLocation
from read_netcdf import readNC


def main():
    
    today = date.today()
    years = list(range(int(today.strftime("%Y")),int(today.strftime("%Y"))+50))    
    years = list(map(str, years))

    # Ask for a location and return coordinates.
    (lat, lon) = queryLocation()

    # Retrive meteorological data for the coordinates and return a path to the file.
    weather_data = cmip6(lat, lon, years)
    # Extract the file to the ./data directory
    zipfile.ZipFile.extract(member=weather_data, path="./data/")

    # Read in data
    daily_pr = readNC('./data/*.nc')

    # Ask for container size
    storage_size = float(input("Volume of existing storage tank (type 0 if none): "))
    roof_surface = float(input("Land surface of collecting roof: "))
    people = int(input("Number of people in the household: "))

    # Start calculations
    calculate(daily_pr, storage_size, roof_surface, people)

    return

def calculate(daily_pr, storage_size, roof_surface, people):
    # In any case, make a copy of the daily_pr
    available = daily_pr.copy()

    if storage_size != 0:
        return

    raise NotImplementedError

if __name__ == "__main__":
    main()