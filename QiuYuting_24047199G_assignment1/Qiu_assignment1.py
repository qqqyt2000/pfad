import requests
import pandas as pd
import datetime
import os
from scraping_utils import get_url

URL = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
year = int(os.getenv('YEAR', 2024))
filename = os.getenv('FILENAME', "crawled-page-{year}.html").format(year=year)

prs = {
    'format': 'geojson',
    'starttime': '2023-01-01',
    'endtime': '2024-09-18',
    'minmagnitude': 5,
    'orderby': 'time'
}


response = get_url(URL,filename,prs)

if response.status_code == 200:
    data = response.json()
    earthquakes = data['features']

    earthquake_data = []

    for eq in earthquakes:
        properties = eq['properties']
        geometry = eq['geometry']
        depth = geometry['coordinates'][2]
        timestamp_ms = properties['time']

        timestamp_s = timestamp_ms / 1000
        dt_object = datetime.datetime.fromtimestamp(timestamp_s)

        earthquake_data.append([
            dt_object,
            properties['place'],
            properties['mag'],
            depth,
            properties['url']
        ])

    df = pd.DataFrame(earthquake_data, columns=['Time', 'Location', 'Magnitude', 'Depth', 'URL'])

    df.to_csv('usgs_earthquake_data.csv', index=False)
    print("successfully into 'usgs_earthquake_data.csv'")

else:
    print(f"fail：{response.status_code}")