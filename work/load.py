import os
import s3fs
import pandas as pd
import pyarrow.parquet as pq

fs = s3fs.S3FileSystem(
    key="access_key",
    secret="secret_key",
    client_kwargs={'endpoint_url': "http://lakefs-dev:8000"}
)

def load_data():
    lakefs_path = "s3://air-quality/main/airquality.parquet/year=2025"
    # เก็บ path ทั้งหมดใน directory นี้
    data_list = fs.glob(f"{lakefs_path}/**")
    print("Discovered files:", data_list)  # Debug เพื่อตรวจสอบ path

    # อ่านและรวมไฟล์ทั้งหมด
    df_list = []
    for file_path in data_list:
        print(f"Reading file: {file_path}")
        try:
            table = pq.read_table(file_path, filesystem=fs)
            df = table.to_pandas()
            df_list.append(df)
        except Exception as e:
            print(f"Failed to read {file_path}: {e}")

    # รวม DataFrame ทั้งหมด
    if not df_list:
        raise ValueError("No valid Parquet files found.")

    df_all = pd.concat(df_list, ignore_index=True)

    # Cleaning and preprocessing
    df_all['lat'] = pd.to_numeric(df_all.get('lat'), errors='coerce')
    df_all['long'] = pd.to_numeric(df_all.get('long'), errors='coerce')
    df_all['year'] = pd.to_numeric(df_all.get('year'), errors='coerce').astype('Int64')
    df_all['month'] = pd.to_numeric(df_all.get('month'), errors='coerce').astype('Int64')
    df_all['PM25.value'] = pd.to_numeric(df_all.get('PM25.value'), errors='coerce')

    # Adjust AQI values
    df_all['PM25.aqi'] = df_all['PM25.value'].mask(df_all['PM25.value'] < 0, pd.NA)
    df_all['PM25.aqi'] = df_all.groupby('stationID')['PM25.aqi'].transform(lambda x: x.ffill())

    # Convert text columns
    text_columns = ['stationID', 'nameTH', 'nameEN', 'areaTH', 'areaEN', 'stationType']
    for col in text_columns:
        df_all[col] = df_all[col].astype('string')

    return df_all

# โหลดข้อมูล
df = load_data()

# บันทึก DataFrame ลงไฟล์ Parquet
output_dir = "/home/jovyan/work/output"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "airquality_data.parquet")
df.to_parquet(output_path, engine="pyarrow", index=False)

print(f"Data saved to: {output_path}")
