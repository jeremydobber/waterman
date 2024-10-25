import zipfile
import glob
import os
import shutil
import pandas as pd
from cds_requests import cmip6
from nominatim_requests import queryLocation
from read_netcdf import readNC
from utils import get_prev_len, get_user_input, clean_tmp_files, draw_chart

def main():
    clean_tmp_files()

    # Ask for length of previsions and return years as list
    years = get_prev_len()

    # Ask for a location and return coordinates.
    (lat, lon) = queryLocation()

    # Retrive meteorological data for the coordinates and return a path to the file.
    print("Downloading weather data.")
    print("This can take up to 5 minutes depending on your connection speed.")
    weather_data = str(cmip6(lat, lon, years))

    # weather_data = "a88792553261e874bec1c3cc7bd7ba1c.zip"
    # Extract the file to the ./data directo
    try:
        with zipfile.ZipFile(weather_data, mode="r") as archive:
            archive.extractall('./data/')
    except IOError as e:
        print("An error occured: ", e)
    finally:
        archive.close()
        os.remove(weather_data)

    # Read in data : returns a pandas series with daily precipitation in kg*m-2
    daily_pr = readNC(glob.glob('./data/*.nc')[0])

    storage_size = float(input("Volume of existing water tank in m3 (type 0 if none): "))
    roof_surface = float(input("Land surface of collecting roof in m2: "))
    
    # Ask for consumption : returns a dict
    user_data = get_user_input() 

    # Format data
    consumption = estimate_consumption(user_data, daily_pr)

    # Start calculations
    calculate(daily_pr, storage_size, roof_surface, consumption)

    clean_tmp_files()

    return

def estimate_consumption(user_data, daily_pr):
    consumption = pd.Series([175] * len(daily_pr), daily_pr.keys())
    consumption *= int(user_data.get("people"))

    return consumption

def calculate(daily_pr, storage_size, roof_surface, consumption):
    # Define a new series to populate 
    overconsumption = pd.Series([0] * len(daily_pr), daily_pr.keys())
    wasted = pd.Series([0] * len(daily_pr), daily_pr.keys())

    # Given the collecting surface, create a new series with the daily_pr
    # The daily precipitation is multiplied by the collecting surface
    # kg/m2 * m2 = kg
    # Converted to cubic metres
    # kg = L = 0.001 m3
    available = roof_surface * daily_pr * 0.001
    # Consumption in m3
    consumption *= 0.001

    # Substract the daily consumption from the available resources. Daily!
    # Same as substracting the cumulative consumption from the cumulative precipitation.
    leftovers = 0
    for i in daily_pr.keys():
        # If there were leftovers, add them to the available.
        # Do not add negative leftovers
        # Do not exceed max capacity
        real_available = available[i] + leftovers
        if storage_size != 0 and leftovers > storage_size:
            available[i] = storage_size
        else:
            available[i] = real_available

        # For every day, we consume some of the available. The remaining is left.
        leftovers = available[i] - consumption[i]

        # Normalize the consumption to real boundaries.
        # Record wasted resources and overconsumption
        if storage_size != 0:
            if leftovers < 0:
                overconsumption[i] = leftovers
                leftovers = 0
            if leftovers > storage_size:
                wasted[i] = leftovers
                leftovers = storage_size

        # Real capacity at the end of the day
        available[i] = leftovers

    print(available.describe())

    draw_chart(available, "storage_state")
    draw_chart(overconsumption, "overcon")
    draw_chart(wasted, "wasted")

    return

if __name__ == "__main__":
    main()