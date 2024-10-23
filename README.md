# Rainwater management

## Objectives

This program's purpose is to assist rainwater management in households. 

## Inputs

A location has to be provided.

The program retrieves climatological data for the given location.  
The dataset used is provided by the ECMWF's CDS (Climate Data Store).  

The user can provide : 

- size of rainwater container if already existing
- surface of the roof
- number of people

To be implemented in GUI, unavailable in the first version :
- water destination : 
    - if WC are in use or if they have been supplanted by dry toilets ?
    - dishwasher ?
    - washing machine ?

## Output

The program calculates the available cumultaive rainwater stocks (over a year ? with weekly or daily precision ?).
- If the user provided a size for an already existing container, the stockes are capped at the given capacity.

The program subtracts from this stock the water needed by the houshold (with weekly or daily precision ?).
- If the user provided a size for an already existing container, the program has to "free" space in the container for refill.


The program draws charts showing the fluctuation of stocks and marks the periods, where availablity falls below the estimated consumption.
- If the user did NOT provide a container size, or, in any case, the program also calculates an ideal container size given the estimated consumption, the available roof size, and the given location.

> The idea behind using a weekly scale is that we can assume that all the equipments of a household will get to be used within a week, which wouldn't be the case for a daily scale.

## Further developement

This piece of software could be included in a "smart home" appliance that collects data in real time about the available water in the container and the consumption. Data collected could be used to train a model that could predict periods of drought due to over-consumption and alert the users.

## Dataset

The `requests.py` file contains the API requests to the ECMWF owned Climate Data Store specifying the variable of interest ("precipitation"), and the years of interest. 

The climatological data is provided for Europe by the *[Temperature and precipitation climate impact indicators from 1970 to 2100 derived from European climate projections](https://cds.climate.copernicus.eu/datasets/sis-hydrology-meteorology-derived-projections?tab=overview)* dataset. Since this is a time-series dataset with daily precision, and it cannot be shrinked down to some specific coordinates, we should consider a backend to store the data once downloaded (there are no updates to it).

This dataset might not be the best choice however due to the absence of updates and the size. We could maybe use an in-situ dataset provided by observation ( [second request to the CDS](https://cds.climate.copernicus.eu/datasets/insitu-gridded-observations-global-and-regional) ) which we could extrapolate but with probably less precision and success than the ECMWF itself.

Alternatively, we could rely on high quality predictions and update the model every year with a new climatological dataset and new replays and predictions. The third request tries to tackle this problem pulling data from the [CIMP6 climate projections](https://cds.climate.copernicus.eu/datasets/projections-cmip6). In this dataset, the region can be specified when pulling the data. The region is shrinked down to ±1° of the latitude and longitude provided.