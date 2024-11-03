import xarray as xr
import cdsapi

"""
    This file runs checks if data is already downloaded and if not pulls the data from the CDS API and reads it in to return a single Pandas time series as (date: precipitation(kg*m-2*s-1)).
    Needed in the SETUP phase.
    The open_weather_data can be simplified a lot with arg(lat, lon, years) if it has to fire only once at setup.
    Sould we set the timeframe for downloads ?
"""


def cmip6(lat, lon, years):
    # DOI: 10.24381/cds.c866074c
    # CIMP6 projection data from 2000 to 2100 on quasi-global scale.
    # Grid-size can be provided!

    # print("Coordinates : " + str(lat) + " & " + str(lon))
    # Use 0.25 to restrict to the nearest grid coordinate
    nbound = lat - 0.25
    ebound = lon - 0.25
    sbound = lat + 0.25
    wbound = lon + 0.25

    dataset = "projections-cmip6"
    request = {
        "temporal_resolution": "daily",
        "experiment": "ssp1_2_6",
        "variable": "precipitation",
        "model": "cnrm_cm6_1_hr",
        "month": [
            "01",
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
            "08",
            "09",
            "10",
            "11",
            "12",
        ],
        "day": [
            "01",
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
            "08",
            "09",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
            "21",
            "22",
            "23",
            "24",
            "25",
            "26",
            "27",
            "28",
            "29",
            "30",
            "31",
        ],
        "year": years,
        "area": [nbound, ebound, sbound, wbound],
    }

    client = cdsapi.Client()
    zippath = client.retrieve(dataset, request).download()

    # return the file path...
    return zippath


def readNC(ncfile):
    ds = xr.open_dataset(ncfile)

    # Reduce the multidimentional array to a single DataFrame
    df = ds.sel(
        lat=ds.lat[0], lon=ds.lon[0], axis_nbounds=ds.axis_nbounds[0]
    ).to_dataframe()

    # Convert Dataframe to Series
    pr_series = df["pr"].squeeze()

    # Process values to get the daily precipitation amount
    pr_series *= 3600 * 24

    return pr_series
