"""
Ingest data from a REST API.
Example: Open-Meteo weather API (free, no auth required).
"""
import requests
import pandas as pd
from datetime import datetime

# Bangkok coordinates
LATITUDE = 13.75
LONGITUDE = 100.52
TIMEZONE = "Asia/Bangkok"


def fetch_weather_forecast(days: int = 7) -> dict:
    """Fetch weather forecast from Open-Meteo API."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": TIMEZONE,
        "forecast_days": days,
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()    # raises HTTPError on 4xx/5xx
    print(f"[api] GET {response.url}")
    print(f"[api] Status: {response.status_code}, Size: {len(response.content)} bytes")
    return response.json()


def parse_weather_response(data: dict) -> pd.DataFrame:
    daily = data["daily"]
    df = pd.DataFrame({
        "date":        pd.to_datetime(daily["time"]),
        "temp_max":    daily["temperature_2m_max"],
        "temp_min":    daily["temperature_2m_min"],
        "rainfall_mm": daily["precipitation_sum"],
    })
    df["temp_avg"] = (df["temp_max"] + df["temp_min"]) / 2
    print(f"[parse] {len(df)} daily records")
    return df


def fetch_with_retry(fn, retries: int = 3):
    for attempt in range(1, retries + 1):
        try:
            return fn()
        except requests.RequestException as e:
            print(f"[retry] Attempt {attempt} failed: {e}")
            if attempt == retries:
                raise
    return None


if __name__ == "__main__":
    try:
        raw = fetch_with_retry(fetch_weather_forecast)
        df = parse_weather_response(raw)
        print("\n--- Bangkok Weather Forecast ---")
        print(df.to_string(index=False))

        out = "/tmp/weather_forecast.parquet"
        df.to_parquet(out, index=False)
        print(f"\nSaved to {out}")
    except requests.RequestException as e:
        print(f"API call failed: {e}")
        print("Make sure you have an internet connection.")
