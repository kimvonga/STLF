import numpy as np
import requests
import pandas as pd
import argparse

def getHourlyForecast(lat: float, long: float) -> pd.DataFrame:
    '''
    Gets hourly forecast data using weather.gov gridpoints forecast hourly api call.
    Inputs:
        lat - latitude in decimal; float
        long - longitude in decimal; float
    Returns:
        forecast_df - hourly weather forecast; pd.DataFrame
    '''
    # api call to points provides api call for hourly forecast so will use that as our primary endpoint
    api='https://api.weather.gov/points/'
    url = api+str(lat)+','+str(long)

    points_response = requests.get(url)

    if points_response.status_code != 200:
        print('ERROR in points request: status code ',points_response.status_code)
        print('latitude: ', lat, '; longitude: ', long)
        return

    hourly_forecast_url = points_response.json()['properties']['forecastHourly']

    forecast_response = requests.get(hourly_forecast_url)

    if forecast_response.status_code != 200:
        print('ERROR in forecast request: status code ', forecast_response.status_code)
        print('latitude: ', lat, '; longitude: ', long)
        return

    forecast_df = pd.DataFrame(forecast_response.json()['properties']['periods'])

    # adding position data
    forecast_df['Latitude'] = lat
    forecast_df['Longitude'] = long

    # converting startTime to date and local time
    forecast_df['Date'] = pd.to_datetime(forecast_df['startTime']).dt.date
    forecast_df['Local Time'] = pd.to_datetime(forecast_df['startTime']).dt.time
    forecast_df['UTC Offset'] = forecast_df['startTime'].str[-6:]

    # unpacking wind speed, prob of precipitation, dewpoint, and rel humidity
    forecast_df['Wind Speed'] = list(map(lambda x: int(x.split()[0]), forecast_df['windSpeed']))
    forecast_df['Wind Speed Unit'] = list(map(lambda x: x.split()[1], forecast_df['windSpeed']))
    forecast_df['Prob Precipitation'] = list(map(lambda x: x['value'], forecast_df['probabilityOfPrecipitation']))
    forecast_df['Dewpoint'] = list(map(lambda x: x['value'], forecast_df['dewpoint']))
    forecast_df['Dewpoint Unit'] = list(map(lambda x: x['unitCode'][-1], forecast_df['dewpoint']))
    forecast_df['Relative Humidity'] = list(map(lambda x: x['value'], forecast_df['relativeHumidity']))

    # dropping unnecessary columns
    drop_cols = ['number', 'name', 'startTime', 'endTime', 'temperatureTrend', 'probabilityOfPrecipitation',
                 'dewpoint', 'relativeHumidity', 'windSpeed', 'icon']
    forecast_df = forecast_df.drop(columns=drop_cols).copy()

    # renaming and reorganizing columns
    rename_cols = {'isDaytime':'Daytime', 'temperature':'Temperature', 'temperatureUnit':'Temperature Unit',
                   'windDirection':'Wind Direction', 'shortForecast':'Short Forecast', 'detailedForecast':'Detailed Forecast'}
    forecast_df.rename(columns=rename_cols, inplace=True)
    neworder = ['Latitude', 'Longitude', 'Date', 'Local Time', 'UTC Offset', 'Daytime', 'Temperature', 'Temperature Unit',
                'Wind Speed', 'Wind Speed Unit', 'Wind Direction', 'Prob Precipitation', 'Dewpoint', 'Dewpoint Unit',
                'Relative Humidity', 'Short Forecast', 'Detailed Forecast']
    forecast_df = forecast_df[neworder]

    return forecast_df


def main(args):
    forecast = getHourlyForecast(args.lat, args.long)

    forecast.to_csv(args.o_dir+'/'+args.save_file, index=True)

    return

if __name__ == '__main__':
    # writing command-line interface
    desc = """Script for pulling weather forecast data from weather.gov. Saves to csv"""

    parser = argparse.ArgumentParser(prog='weather forecast', 
                                     description=desc)

    parser.add_argument('-o', '--o_dir', help='directory for storing output', default='./')
    parser.add_argument('-s', '--save_file', help='name of file to save weather forecast data to',
                        default='weather_forecast.csv')
    parser.add_argument('--lat', help='latitude position of weather forecast', default=0.0)
    parser.add_argument('--long', help='longitude position of weather forecast', default=0.0)
    
    args = parser.parse_args()
    
    main(args)
