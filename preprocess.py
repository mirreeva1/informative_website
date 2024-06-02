import pandas as pd
from pathlib import Path
from loguru import logger
from tqdm import tqdm
from geopy.geocoders import Nominatim

data_folder =  Path("data")
dataset_path = Path('data/raw/your_dataset.csv')
df = pd.read_csv(dataset_path, sep=';')
logger.info(f"Column names: {df.columns}")

# Get a unique list of countries and regions
unique_countries = df[['Country', 'Region']].drop_duplicates().reset_index(drop=True)

# Geocode unique countries and regions
geolocator = Nominatim(user_agent="your_app_name")

def get_location(country, region):
    try:
        query = f"{country}, {region}"
        location = geolocator.geocode(query)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except:
        return None, None
    
locations = []
for _, row in tqdm(unique_countries.iterrows(), total=len(unique_countries), desc="Geocoding"):
    country = row['Country']
    region = row['Region']
    location = get_location(country, region)
    locations.append(location)

unique_countries['location'] = locations
unique_countries['latitude'] = [loc[0] if loc else None for loc in unique_countries['location']]
unique_countries['longitude'] = [loc[1] if loc else None for loc in unique_countries['location']]

# Merge the geocoded locations back into the original dataset
df = df.merge(unique_countries[['Country', 'Region', 'latitude', 'longitude']], how='left', on=['Country', 'Region'])
df.to_csv(data_folder / "processed/data.csv", index=False)