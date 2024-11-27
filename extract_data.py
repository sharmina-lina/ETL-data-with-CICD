import requests
import json

API_KEY = '9a1883ede133db713c9cccb8f52434d7'
CITIES = ['Oslo', 'Dhaka', 'New York', 'Bergen', 'Khulna', 'Shanghai']
OUTPUT_FILE = 'raw_weather_data.json'

def fetch_weather_data():
    weather_data = []
    for city in CITIES:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        )
        if response.status_code == 200:
            weather_data.append(response.json())
        else:
            print(f"Failed to fetch data for {city}")
    return weather_data

if __name__ == "__main__":
    data = fetch_weather_data()
    with open(OUTPUT_FILE, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data extracted and saved to {OUTPUT_FILE}")
