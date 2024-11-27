import boto3

AWS_ACCESS_KEY = 'AKIA5WLTTGEGUSAWI4N4'
AWS_SECRET_KEY = '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'
BUCKET_NAME = 'weatherdataprojectetlcicd'
FILE_NAME = 'transformed_weather_data.csv'

def upload_to_s3():
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    try:
        s3.upload_file(FILE_NAME, BUCKET_NAME, FILE_NAME)
        print(f"{FILE_NAME} uploaded to S3 bucket {BUCKET_NAME}")
    except Exception as e:
        print(f"Failed to upload file: {e}")

if __name__ == "__main__":
    upload_to_s3()
