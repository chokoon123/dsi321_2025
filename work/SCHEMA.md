```json
{
  "columns": [
    "timestamp", "stationID", "nameTH", "nameEN", "areaTH",
    "areaEN", "stationType", "lat", "long", "PM25.color_id",
    "PM25.aqi", "year", "month", "day", "hour"
  ],
  "types": [
    "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT",
    "TEXT", "REAL", "REAL", "INTEGER", "INTEGER",
    "INTEGER", "INTEGER", "INTEGER", "INTEGER"
  ],
  "key_columns": [
    "timestamp", "stationID", "lat", "long", "PM25.aqi"
  ]
}
```