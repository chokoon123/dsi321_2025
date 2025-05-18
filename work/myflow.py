import requests
import pandas as pd
from prefect import flow, task

@task
def fetch_data() -> list[dict]:
    try:
        url = 'http://air4thai.pcd.go.th/services/getNewAQI_JSON.php'
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        data = response.json()
        data = data['stations']

        return data
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

@task
def data_processing(data: list[dict]) -> pd.DataFrame:
    
    df = pd.DataFrame(data)
    expanded_aqi = pd.json_normalize(df['AQILast'])
    df = pd.concat([df, expanded_aqi], axis=1)

    numeric_cols = ['PM25.color_id', 'PM25.value']

    df[numeric_cols] = df[numeric_cols].astype(float)
    df['time'] = df['time'].mode()[0]
    df['date'] = df['date'].mode()[0]
    df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'])

    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month
    df['day'] = df['timestamp'].dt.day
    df['hour'] = df['timestamp'].dt.hour

    datetime_attibute_cols = ['timestamp', 'year', 'month', 'day', 'hour']
    location_attribute_cols = ['stationID', 'nameTH', 'nameEN', 'areaTH', 'areaEN', 'stationType', 'lat', 'long']
    df = df[datetime_attibute_cols + location_attribute_cols + numeric_cols]

    return df

@task
def load_to_lakefs(df: pd.DataFrame, lakefs_s3_path: str, storage_options: dict):
    df.to_parquet(
        lakefs_s3_path,
        storage_options=storage_options,
        partition_cols=['year','month','day','hour'],
        engine='pyarrow'
    )

@flow(name='main-flow', log_prints=True)
def main_flow():

    data = fetch_data()
    
    df = data_processing(data)

    ACCESS_KEY = "access_key"
    SECRET_KEY = "secret_key"

    lakefs_endpoint = "http://lakefs-dev:8000/"

    repo = "air-quality"
    branch = "main"
    path = "airquality.parquet"

    lakefs_s3_path = f"s3a://{repo}/{branch}/{path}"

    storage_options = {
        "key": ACCESS_KEY,
        "secret": SECRET_KEY,
        "client_kwargs": {
            "endpoint_url": lakefs_endpoint
        }
    }

    load_to_lakefs(df=df, lakefs_s3_path=lakefs_s3_path, storage_options=storage_options)

