import cdsapi

# DOI: 10.24381/cds.9eed87d5
# Projections derived from observation. Europe, daily.

def siseurope():
    dataset = "sis-hydrology-meteorology-derived-projections"
    request = {
        "product_type": "essential_climate_variables",
        "variable": ["precipitation"],
        "processing_type": "bias_corrected",
        "variable_type": "absolute_values",
        "time_aggregation": ["daily"],
        "horizontal_resolution": "5_km",
        "experiment": [
            "historical",
            "rcp_4_5"
        ],
        "rcm": "cclm4_8_17",
        "gcm": "ec_earth",
        "ensemble_member": ["r12i1p1"],
        "period": [
            "2018",
            "2019",
            "2020",
            "2021",
            "2022",
            "2023",
            "2024",
            "2025",
            "2026",
            "2027",
            "2028",
            "2029",
            "2030",
            "2031",
            "2032",
            "2033"
        ]
    }

    client = cdsapi.Client()
    client.retrieve(dataset, request).download()

# DOI: 10.24381/cds.11dedf0c
# In situ data with no projections. Quasi-global, daily.

def insitu():
    dataset = "insitu-gridded-observations-global-and-regional"
    request = {
        "origin": "cmorph",
        "region": "quasi_global",
        "variable": ["precipitation"],
        "time_aggregation": "daily",
        "horizontal_aggregation": ["0_5_x_0_5"],
        "year": [
            "1998", "1999", "2000",
            "2001", "2002", "2003",
            "2004", "2005", "2006",
            "2007", "2008", "2009",
            "2010", "2011", "2012",
            "2013", "2014", "2015",
            "2016", "2017", "2018",
            "2019", "2020", "2021"
        ],
        "version": ["v1_0"]
    }

    client = cdsapi.Client()
    client.retrieve(dataset, request).download()


# DOI: 10.24381/cds.c866074c
# CIMP6 projection data from 2000 to 2100 on quasi-global scale.
# Grid-size can be provided!

def cmip6(lat, long):

    print("Coordinates : " + str(lat) + " & " + str(long))
    nbound = lat - 1
    ebound = long - 1
    sbound = lat + 1
    wbound = long + 1

    print(nbound)

    return

    dataset = "projections-cmip6"
    request = {
        "temporal_resolution": "daily",
        "experiment": "ssp1_2_6",
        "variable": "precipitation",
        "model": "cnrm_cm6_1_hr",
        "month": [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12"
        ],
        "day": [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12",
            "13", "14", "15",
            "16", "17", "18",
            "19", "20", "21",
            "22", "23", "24",
            "25", "26", "27",
            "28", "29", "30",
            "31"
        ],
        "year": [
            "2050", "2051", "2052",
            "2053", "2054", "2055",
            "2056", "2057", "2058",
            "2059", "2060", "2061",
            "2062", "2063", "2064",
            "2065", "2066", "2067",
            "2068", "2069", "2070",
            "2071", "2072", "2073",
            "2074", "2075", "2076",
            "2077", "2078", "2079",
            "2080", "2081", "2082",
            "2083", "2084", "2085",
            "2086", "2087", "2088",
            "2089", "2090", "2091",
            "2092", "2093", "2094",
            "2095", "2096", "2097",
            "2098", "2099", "2015",
            "2016", "2017", "2018",
            "2019", "2020", "2021",
            "2022", "2023", "2024",
            "2025", "2026", "2027",
            "2028", "2029", "2030",
            "2031", "2032", "2033",
            "2034", "2035", "2036",
            "2037", "2038", "2039",
            "2040", "2041", "2042",
            "2043", "2044", "2045",
            "2046", "2047", "2048",
            "2049"
        ],
        "area": [nbound, ebound, sbound, wbound]
    }

    client = cdsapi.Client()
    client.retrieve(dataset, request).download()
