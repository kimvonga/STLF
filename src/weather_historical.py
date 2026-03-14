import numpy as np
import requests
import pandas as pd
import argparse

def getHourlyHistorical(lat: float, long: float, start_date: str, end_date: str) -> pd.DataFrame:
    '''
    Gets hourly historical data using open-meteo.com hourly api call.
    Inputs:
        lat - latitude in decimal; float
        long - longitude in decimal; float
        start_date - start date in format yyyy-mm-dd (%Y-%m-%d); str
        end_date - end date in format yyyy-mm-dd (%Y-%m-%d); str
    Returns:
        historical_df - hourly historical weather; pd.DataFrame
    '''
    url = 'https://archive-api.open-meteo.com/v1/archive'
    hourly_params = ','.join(['temperature_2m', 'relativehumidity_2m', 'apparent_temperature',
                              'precipitation', 'rain', 'snowfall', 'weathercode', 'surface_pressure',
                              'windspeed_10m', 'winddirection_10m', 'dew_point_2m'])
    params = {"latitude": lat,
              "longitude": long,
              "start_date": start_date,
              "end_date": end_date,
              "hourly": hourly_params}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print('ERROR in request: status code ',response.status_code)
        print('latitude: ', lat, '; longitude: ', long)
        print('start_date: ', start_date, '; end_date: ', end_date)
        return

    data = response.json()

    historical_df = pd.DataFrame(data['hourly'])

    # adding lat, long, times, and measurement units
    historical_df['Latitude'] = lat
    historical_df['Longitude'] = long

    my_dt = pd.to_datetime(historical_df['time'], utc=True)
    historical_df['Date'] = my_dt.dt.date
    historical_df['UTC Time'] = my_dt.dt.time

    historical_df['Temperature Unit'] = data['hourly_units']['temperature_2m']
    historical_df['Wind Speed Unit'] = data['hourly_units']['windspeed_10m']
    historical_df['Precipitation Unit'] = data['hourly_units']['precipitation']
    historical_df['Dewpoint Unit'] = data['hourly_units']['dew_point_2m']

    # renaming and reorganizing columns
    rename_cols = {'temperature_2m':'Temperature', 'windspeed_10m':'Wind Speed',
                   'winddirection_10m':'Wind Direction', 'precipitation':'Precipitation',
                   'relativehumidity_2m':'Relative Humidity', 'weathercode':'Weather Code',
                   'dew_point_2m':'Dewpoint'}
    historical_df.rename(columns=rename_cols, inplace=True)

    neworder = ['Latitude', 'Longitude', 'Date', 'UTC Time', 'Temperature', 'Temperature Unit',
                'Wind Speed', 'Wind Speed Unit', 'Wind Direction', 'Precipitation', 'Precipitation Unit',
                'Dewpoint', 'Dewpoint Unit', 'Relative Humidity', 'Weather Code']
    historical_df = historical_df[neworder]

    return historical_df

def main(args):
    historical = getHourlyHistorical(args.lat, args.long, args.start, args.end)

    historical.to_csv(args.o_dir+'/'+args.save_file, index=True)

    return

if __name__ == '__main__':
    # writing command-line interface
    desc = """Script for pulling historical weather data from open-meteo. Saves to csv"""

    parser = argparse.ArgumentParser(prog='weather historical', 
                                     description=desc)

    parser.add_argument('-o', '--o_dir', help='directory for storing output', default='./')
    parser.add_argument('-s', '--save_file', help='name of file to save historical weather data to',
                        default='weather_historical.csv')
    parser.add_argument('--lat', help='latitude position of historical weather', default=0.0)
    parser.add_argument('--long', help='longitude position of historical weather', default=0.0)
    parser.add_argument('--start', help='start date for historical data. yyyy-mm-dd format', default='2019-01-01')
    parser.add_argument('--end', help='end date for historical data. yyyy-mm-dd format', default='2019-01-02')

    args = parser.parse_args()

    # running main()
    main(args)
