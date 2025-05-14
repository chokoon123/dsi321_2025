# Real-Time Data Pipeline & Visualization

📊 **A real-time data pipeline with visualization using Prefect, LakeFS, and Streamlit – all containerized with Docker Compose**

This project was developed as part of the DSI321: Big Data Infrastructure course, focusing on building automated data pipelines for real-time analytics. It uses Prefect.io to manage task orchestration, and the entire system runs in Docker containers. Data insights are visualized using Python-based tools, making it easy to monitor and analyze the incoming data stream.

## 🔍 Overview

This project is a hands-on implementation of a real-time data pipeline. It fetches data from an Air4Thai API on an hourly basis, stores it in a versioned data lake , and visualizes insights through an interactive web dashboard.

The workflow uses **Python** as the main programming language, leverages **Prefect** for scheduling, **LakeFS** for data versioning, and **Streamlit** for front-end visualization. Everything runs seamlessly via **Docker Compose**.


## 🔁 Workflow

1. **Scheduled API Fetching with Prefect**  
   Prefect is used to schedule a function that pulls data from an API every hour.

2. **Data Storage with LakeFS**  
   The fetched data is stored as Parquet files in LakeFS for version control and reproducibility.

3. **Mounting Data Locally**  
   The LakeFS repository is mounted locally to enable reading Parquet files directly.

4. **Visualization with Streamlit**  
   A Python-based Streamlit app reads the Parquet data and displays interactive charts and insights.

5. **Containerized with Docker Compose**  
   All services are containerized for consistent and reproducible deployment.


