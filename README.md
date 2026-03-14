# Data Collection for Training Short-Term Load Forecasting Models

**Purpose:**

Collect data that could be used to train a short-term load forecasting model. Dataset contains census data, historical and forecasted weather, and historical and forecasted demand.

**Context:**

One of the core challenges of an energy provider is to generate and distribute enough energy to meet demand while not overgenerating to accrue loss. Existing forecasting models can struggle to predict demand during extreme weather conditions leading to waste, potential equipment damage, or possibly blackouts. By improving predictions during extreme weather conditions, which can be done by training forecasting models on weather data, energy providers can limit waste, reduce the possibility of equipment damage, and reduce the possibility of blackout.

**Data Sources:**
- census.gov (https://data.census.gov/) for census data including geographic position
- open-meteo (https://open-meteo.com/en/docs) for historical weather data
- weather.gov (https://www.weather.gov/documentation/services-web-api) for forecasted weather data
- eia.gov (https://www.eia.gov/opendata/browser/) for historical energy grid demand and forecasted demand

**Usage:**

Census data was downloaded from census.gov and can be found in data/raw/. Users can also navigate data.census.gov to find additional data. 

Users are expected to collect their own data from weather.gov, open-meteo.com, and eia.gov using provided python scripts. The provided python scripts are located under src/. The scripts utilize APIs provided by the national weather service, open-meteo, and the EIA. Documentation for APIs can be found on the respective hosting service. 

The provided python scripts can be called from the command line. To use, check the --help flag. The scripts can also be loaded as functions.

Examples of use can be found in a Jupyter notebook located under notebooks/.

**Access:**

APIs from the national weather service and open-meteo do not require an access key and are free to use.

The EIA requires users to register for an API key which can be done at https://www.eia.gov/opendata/register.php. Registering for an API key is free.

For access rights, check the respective data souces.

The provided code are free to use.
