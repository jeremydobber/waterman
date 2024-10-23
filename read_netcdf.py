import numpy as np
import xarray as xr
import pandas as pd

def readNC(filepath):
    ds = xr.open_dataset(filepath)

    # Reduce the multidimentional array to a single DataFrame
    df = ds.sel(lat=ds.lat[0], lon=ds.lon[0], axis_nbounds=ds.axis_nbounds[0]).to_dataframe()

    # Convert Dataframe to Series
    pr_series = df["pr"].squeeze()
    
    # Process values to get the daily precipitation amount
    pr_series *= 3600*24

    return pr_series

"""
    The functions below were an experiment. They are not called in the current state of this code.
"""

def getYearlyPr(ds):

    for year in range(2015,2100):
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"

        ds_selection = ds.sel(lat=ds.lat[0], lon=ds.lon[0], axis_nbounds=ds.axis_nbounds[0], time=slice(start_date,end_date))
        df = ds_selection.to_dataframe()


def getMonthlyPr(df):

    labels = list()
    values = list()

    evelo = int(df.shape[0]/2)

    for month in range(1,13):

        if month in [1,3,5,7,8,10,12]:
            lastday = str(31)
        elif month == 2:
            if evelo % 2 == 0:
                lastday = str(29)
            else:
                lastday = str(28)
        else:
            lastday = str(30)

        if month < 10:
            month = f"0{month}"  

        start_date = f"{year}-{month}-01"
        end_date = f"{year}-{month}-{lastday}"  

        ds_selection = ds.sel(lat=ds.lat[0], lon=ds.lon[0], axis_nbounds=ds.axis_nbounds[0], time=slice(start_date,end_date))
        
        df = ds_selection.to_dataframe() # This sends it to a pandas Series (2 dimensions)
        
        monthly_pr = df.pr * 3600 * 24
        
        labels.append(f"{year}-{month}")
        values.append(monthly_pr.sum()) # Shouldn't sum over month. We need a cumulative series !

    pr = pd.Series(values, labels)

    return pr