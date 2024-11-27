import json
import pandas as pd

INPUT_FILE = 'raw_weather_data.json'
OUTPUT_FILE = 'transformed_weather_data.csv'

def transform_weather_data():
    with open(INPUT_FILE, 'r') as file:
        raw_data = json.load(file)
    
    transformed_data = []
    for entry in raw_data:
        transformed_data.append({
            'City': entry['name'],
            'Temperature (C)': entry['main']['temp'] - 273.15,
            'Humidity (%)': entry['main']['humidity'],
            'Weather': entry['weather'][0]['description']
        })
    
    df = pd.DataFrame(transformed_data)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Data transformed and saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    transform_weather_data()
