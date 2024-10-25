import zipfile
import glob
import os
import shutil
import pandas as pd
from datetime import date
from cds_requests import cmip6
from nominatim_requests import queryLocation
from read_netcdf import readNC

def main():
    
    # today = date.today()
    # years = list(range(int(today.strftime("%Y")),int(today.strftime("%Y"))+50))    
    # years = list(map(str, years))

    # Ask for a location and return coordinates.
    # (lat, lon) = queryLocation()

    # Retrive meteorological data for the coordinates and return a path to the file.
    # weather_data = str(cmip6(lat, lon, years))

    weather_data = "a88792553261e874bec1c3cc7bd7ba1c.zip"
    # Extract the file to the ./data directory
    with zipfile.ZipFile(weather_data, mode="r") as archive:
        archive.extractall('./data/')
        # Delete the zip archive !!!

    # Read in data
    # Returns a pandas series with daily precipitation in kg*m-2
    daily_pr = readNC(glob.glob('./data/*.nc')[0])

    storage_size = float(input("Volume of existing water tank in m3 (type 0 if none): "))
    roof_surface = float(input("Land surface of collecting roof in m2: "))
    
    # Ask for consumption
    user_data = request_data()
    consumption = estimate_consumption(user_data, daily_pr)

    # Start calculations
    calculate(daily_pr, storage_size, roof_surface, consumption)

    clean_temp_files()

    return

def request_data():
    people = int(input("Number of people in the household: "))

    # Add other questions about water usage.

    data = {"people": people}

    return data

def estimate_consumption(user_data, daily_pr):
    consumption = pd.Series([175] * len(daily_pr))
    consumption *= int(user_data.get("people"))

    return consumption

def calculate(daily_pr, storage_size, roof_surface, consumption):
    # Given the collecting surface, create a new series with the daily_pr
    # The daily precipitation is multiplied by the collecting surface
    # kg/m2 * m2 = kg
    # Converted to cubic metres
    # kg = L = 0.001 m3
    available = roof_surface * daily_pr
    available *= 0.001

    # Convert series to cumulative
    available = available.cumsum()

    # Substract the daily consumption from the available resources. Daily!
    # Same as substracting the cumulative consumption from the cumulative precipitation.
    consumption *= 0.001
    consumption = consumption.cumsum()
    print(consumption.head)
    available.subtract(consumption)

    # Cap quantities within real boundaries
    if storage_size != 0:
        available.clip(0, storage_size, inplace=True)

    print(available.describe())
    print(available.head)

    raise NotImplementedError

def clean_temp_files():
    try:
        shutil.rmtree("./data")
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

if __name__ == "__main__":
    main()