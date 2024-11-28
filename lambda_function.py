import boto3
from pip._vendor import requests
import json
import os

def lambda_handler(event, context):
    # Example API to extract weather data
    API_KEY = "9a1883ede133db713c9cccb8f52434d7"
    API_URL = "https://api.openweathermap.org/data/2.5/weather?q=oslo&appid="+API_KEY
    
    
    response = requests.get(API_URL)
    if response.status_code == 200:
        weather_data = response.json()
    else:
        return {"status": "Failed", "message": "Error fetching data"}
    
    # Transform data
    transformed_data = {
        "city": weather_data["name"],
        "temperature": weather_data["main"]["temp"],
        "humidity": weather_data["main"]["humidity"],
        "weather": weather_data["weather"][0]["description"]
    }
    
    # Load data to S3
    s3 = boto3.client("s3")
    bucket_name = os.environ["BUCKET_NAME"]
    file_name = "transformed_weather_data.json"
    
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=json.dumps(transformed_data),
        ContentType="application/json"
    )
    
    return {"status": "Success", "message": f"Data uploaded to {bucket_name}/{file_name}"}
