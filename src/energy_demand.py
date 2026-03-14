import numpy as np
import pandas as pd
import requests
import argparse

def getDemandForecastRegion(start: str, end: str, region: str, api_key: str, limit=5000) -> pd.DataFrame:
    '''
    Fetches electricity demand, demand forecast, generation, and interchange from eia.gov api
    Region codes available ["CAL", "CAR", "CENT", "FLA", "MIDA", "MIDW", "NE",
                            "NW", "NY", "SE", "SW", "TEN", "TEX", "US48"]
    Inputs:
        start: date in YYYY-MM-DD; str
        end: date in YYYY-MM-DD; str
        region: region code; str
        api_key: api_key for eia.gov, check email; str
    Returns:
        demand_forecast_df: electricity demand, forecast, generation, and interchange; pd.DataFrame
    '''
    url = 'https://api.eia.gov/v2/electricity/rto/region-data/data/?'
    start = start+'T00'
    if end != '':
        end = end+'T00'
        params = {'frequency':'hourly', 'facets[respondent][]':region, 'data[0]':'value',
                  'start':start, 'end':end, 'length':limit, 'api_key':api_key}
    else:
        params = {'frequency':'hourly', 'facets[respondent][]':region, 'data[0]':'value',
                  'start':start, 'length':limit, 'api_key':api_key}

    demand = requests.get(url, params=params)

    if demand.status_code != 200:
        print('ERROR status code: ', demand.status_code)
        return

    demand_df = pd.DataFrame(demand.json()['response']['data'])

    # standardizing date, time format across datasets
    demand_df['Date'] = pd.to_datetime(demand_df['period']).dt.date
    demand_df['Time UTC'] = pd.to_datetime(demand_df['period']).dt.time

    demand_df['value'] = demand_df['value'].astype(float)

    # renaming and reordering
    demand_df.rename(columns={'respondent':'Region', 'type':'Type',
                              'value':'Value', 'value-units':'Value Units'}, inplace=True)
    cols = ['Date', 'Time UTC', 'Region', 'Type', 'Value', 'Value Units']
    demand_df = demand_df[cols]

    return demand_df

def main(args):
    energy = getDemandForecastRegion(args.start,
                                     args.end,
                                     args.region,
                                     args.key,
                                     args.limit)

    energy.to_csv(args.o_dir+'/'+args.save_file, index=True)

    return

if __name__ == '__main__':
    # writing command-line interface
    desc = """Script for pulling energy demand and forecast data from eia.gov. Saves to csv.
              Requires api key. Go to eia.gov/opendata/register.php or goole search to acquire free key.
              To run, either supply key after --key flag or edit default value in script.
              
              region codes for region argument are
              ["CAL", "CAR", "CENT", "FLA", "MIDA", "MIDW", "NE", "NW", "NY", "SE", "SW", "TEN", "TEX", "US48"]
              """

    parser = argparse.ArgumentParser(prog='demand forecast', 
                                     description=desc)

    parser.add_argument('-o', '--o_dir', help='directory for storing output', default='./')
    parser.add_argument('-s', '--save_file', help='name of file to save demand forecast data to',
                        default='demand_forecast.csv')
    parser.add_argument('--start', help='start date for energy demand data. format yyyy-mm-dd',
                        default='2000-01-01')
    parser.add_argument('--end', help='Optional. end date for energy demand data. format yyyyy-mm-dd',
                        default='')
    parser.add_argument('--region', help='Region code for energy demand, demand forecast, etc.',
                        default='US48')
    parser.add_argument('--key', help='api key to access eia.goc',
                        default='')
    parser.add_argument('--limit', help='Optional. Limits amount of data requested from eia.gov',
                        default=5000)

    args = parser.parse_args()

    main(args)
