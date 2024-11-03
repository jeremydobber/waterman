# Rainwater management

#### Video demo :

### Objectives

This program's purpose is to assist rainwater management in households. 

### Inputs

Users are allowed to provide a timeframe. If exceeding the data available on the CDS, the default 2015-2099 is enforced.

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


### Output

The program calculates the available cumulative rainwater stocks (over a year ? with weekly or daily precision ?).

- If the user provided a size for an already existing container, the stocks are capped at the given capacity.

The program subtracts from this stock the water needed by the houshold (with weekly or daily precision ?).

- If the user provided a size for an already existing container, the program has to "free" space in the container for refill.


The program draws charts showing the fluctuation of stocks and marks the periods where availablity falls below the estimated consumption.

- If the user did NOT provide a container size, or, in any case, the program also calculates an ideal container size given the estimated consumption, the available roof size, and the given location.

> The idea behind using a weekly scale is that we can assume that all the equipments of a household will get to be used within a week, which wouldn't be the case for a daily scale. In the first version however, a monthly scale could be used because excludes decisions such as what to do with remaining days of a year that do not add up to a whole week. Another solution would be to work on the whole period starting from the day the program is run or a user selected date.

### Further developement

This piece of software could be included in a "smart home" appliance that collects data in real time about the available water in the container and the consumption. Data collected could be used to train a model that could predict periods of drought due to over-consumption and alert the users.

### Location

The user is asked to provide a location to calculate the climatology for. The coordinates are obtained through OSM's Nominatim API. This service has a strict usage policy you can read about [here](https://operations.osmfoundation.org/policies/nominatim/). If we would want to deploy it as a webapp, we should consider deploying an API gateway of our own.

### Dataset

The `requests.py` file contains the API requests to the ECMWF owned Climate Data Store specifying the variable of interest ("precipitation"), and the years of interest. 

For the climatological data for Europe we could use the *[Temperature and precipitation climate impact indicators from 1970 to 2100 derived from European climate projections](https://cds.climate.copernicus.eu/datasets/sis-hydrology-meteorology-derived-projections?tab=overview)* dataset. Since this is a time-series dataset with daily precision, and it cannot be shrinked down to some specific coordinates, we should consider a backend to store the data once downloaded (there are no updates to it).

This dataset might not be the best choice however due to the absence of updates and the size. We could maybe use an in-situ dataset provided by observation ( [second request to the CDS](https://cds.climate.copernicus.eu/datasets/insitu-gridded-observations-global-and-regional) ) which we could extrapolate but with probably less precision and success than the ECMWF itself.

Alternatively, we could rely on high quality predictions and update the model every year with a new climatological dataset and new replays and predictions. The third request tries to tackle this problem pulling data from the [CIMP6 climate projections](https://cds.climate.copernicus.eu/datasets/projections-cmip6). In this dataset, the region can be specified when pulling the data. The region is shrinked down to ±0.25° of the latitude and longitude provided. 

> The reasoning behind this can be criticized, but the idea is to simplify the processing of the data eliminating two dimensions of it. We get a single series of scalars for a single cell of the initial grid. We effectively end up with a time Series with days as keys and precipitation amounts as values. 

### Data handeling

The file returned by the CDS is a zip file wich containes a netcdf file. We can read in the data with python's xarray function build on top of the netCDF4 library. The data downloaded from the CDS has three dimensions (**lat**, **lon**, **time**) and two variables of which **pr** is of interest. The **lat** and **lon** dimensions have a single `float()` value as they have been shrinked down in the request in `cds_requests.py`. The timespane of the data retrieved is also known so we can *"hardcode"* the loops to filter years and months.

### Calculations

In the first development phase, we used a mean daily water consumption to reduce the amount of code and complexity. Although very convenient for the user, this choice is not coherent with the purpose of this piece of software. Since our aim is to not only help with the dimensioning of a water container, but also to provide insight into the different manners water could be saved in a houshold, breaking down the consumption seems necessary. The questions that remain are : do we take the average consumption of a dishwasher for instance or do we try to calculate it's consumption based on the number of cycles per annum guessed from the amount of people in the household ? How much more precise will be our guessing compared to the data provided by the reseller or the user ?