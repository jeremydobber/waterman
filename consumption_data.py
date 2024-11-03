import csv
import os
import pandas as pd
import math

"""
    The purpose of this file is to import real water usage values from a digital water meter.
    The format that was arbitrarely chosen is csv such as : (day(date) : consumption(L or m3)). 
    The ultimate goal is to allow this program to run on a RPi for example and make daily etimates about future water usage to alert in case of overconsumption.
"""

def open_consumption_data(filepath):
    try:
        with os.open(filepath, 'r') as file:
            consumption_data = csv.DictReader(file)
    except FileNotFoundError as e:
        print("An error occured: ", e)

    consumption_series = pd.Series(consumption_data)

    return consumption_series

def format_data(data_series, target_size):

    # Measure length
    data_size = data_series.size

    consumption_model = pd.Series()

    # If length is below a week, resize with mean data
    if data_size < 7:
        consumption_model = pd.Series([data_series.mean]*target_size)
    # If length is more than a week but below a year, take a sample of a multiple of seven and fill to resize
    else:
        if data_size < 365:
            consumption_model = pd.Series([data_series.tail(- math.floor(data_size % 7))])
        else:
            # Take the whole year and resize (! what to do with 366 ?)
            print()

    return consumption_model