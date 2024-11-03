from nominatim_requests import queryLocation, selectLocation
from weather_data import cmip6, readNC
from utils import get_prev_len, extract_zipfile
from render_models import calculate_available, extrapolate_consumption
import glob


def main():
    # Ask for a location and return coordinates
    query = str(input("Location: "))
    res = queryLocation(query)
    (lat, lon) = selectLocation(res)

    # Ask for length of previsions and return years as list
    years = get_prev_len()

    print("Downloading weather data.")
    print("This can take up to 5 minutes depending on your connection speed.")
    weather_data = str(cmip6(lat, lon, years))

    # .cache naming convention
    filename = f"{lat}-{lon}_{int(len(years))}"
    path = f"./.cache/{filename}"

    extract_zipfile(weather_data, path)

    # Read in weather data as a pandas series with daily precipitation in kg*m-2
    daily_pr = readNC(glob.glob(f"{path}/*.nc")[0])

    storage_size = float(input("Volume of existing water tank in m3: "))
    roof_surface = float(input("Land surface of collecting roof in m2: "))
    people = int(input("Number of people in the household: "))

    # Format data
    consumption = extrapolate_consumption(people, daily_pr)

    available = calculate_available(daily_pr, storage_size, roof_surface, consumption)

    print(available.describe())
    print(consumption.describe())

    return


if __name__ == "__main__":
    main()
