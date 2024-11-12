import pandas as pd
import requests
import time
from requests.exceptions import RequestException

# Function to get game details from Steam API
def get_game_details(appid, api_key, max_retries=3, retry_interval=5):
    url = f"http://store.steampowered.com/api/appdetails?appids={appid}&key={api_key}"
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data[str(appid)]['success']:
                return data[str(appid)]['data']
        except (RequestException, ValueError) as e:
            print(f"Error fetching details for appid {appid}: {e}")
            retries += 1
            time.sleep(retry_interval)
    return None

# Function to extract genre from game details
def get_genres(appid, api_key, max_retries=3, retry_interval=5):
    details = get_game_details(appid, api_key, max_retries, retry_interval)
    if details and 'genres' in details:
        return [genre['description'] for genre in details['genres']]
    return []

# Monitoring function to track progress
def monitor_progress(current, total, interval):
    progress = (current / total) * 100
    print(f"Processed {current}/{total} games. Progress: {progress:.2f}%")
    time.sleep(interval)

# Example usage with your dataset
api_key = '158A1E44349937AF71058C746E2A8B1D'  # Replace with your actual Steam API key
interval = 0.5  # Interval in seconds between requests (adjusted for safety)

# Load the new data file with specified encoding
new_df = pd.read_csv('combined_steamspy_data1.csv', encoding='ISO-8859-1')

# Identify the column that contains the Steam app IDs
print(new_df.columns)  # Print columns to identify the correct column name

# Replace 'appid_column' with the actual column name that contains the Steam app IDs
appid_column = 'appid'  # Change this to the correct column name after inspection

# Add genres to the dataframe
total_games = len(new_df)
new_df['Genres'] = ''

for i, appid in enumerate(new_df[appid_column]):
    new_df.at[i, 'Genres'] = get_genres(appid, api_key)
    monitor_progress(i + 1, total_games, interval)

# Save the updated dataframe
new_df.to_csv('updated_combined_steamspy_data.csv', index=False)

# Inspect the updated dataframe
print(new_df.head())