import pandas as pd

def calculate_available(daily_pr, storage_size, roof_surface, consumption):
    # Given the collecting surface, create a new series with the daily_pr
    # The daily precipitation is multiplied by the collecting surface
    # kg/m2 * m2 = kg
    # Converted to cubic metres
    # kg = L = 0.001 m3
    available = roof_surface * daily_pr * 0.001
    # Consumption in m3
    consumption *= 0.001

    # Define a new series to populate 
    overconsumption = pd.Series([0] * daily_pr.size, daily_pr.keys())
    wasted = pd.Series([0] * daily_pr.size, daily_pr.keys())

    # Substract the daily consumption from the available resources. Daily!
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
        else:
            if leftovers < 0:
                overconsumption[i] = leftovers
                leftovers = 0

        # Real capacity at the end of the day
        available[i] = leftovers

    return available

def extrapolate_consumption(people, daily_pr):
    consumption = pd.Series([175] * daily_pr.size, daily_pr.keys(), name="consumption")
    consumption *= people
    consumption.name()

    return consumption