"""
Work with a REST API data source.   read (fetch + parse) -> inspect -> clean

Example: Open-Meteo weather API (free, no auth). Needs an internet connection.
"""
import requests
import pandas as pd

LAT, LON, TZ = 13.75, 100.52, "Asia/Bangkok"


def read(days: int = 7) -> pd.DataFrame:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LAT, "longitude": LON, "timezone": TZ,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "forecast_days": days,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()           # raises on 4xx/5xx
    daily = resp.json()["daily"]
    return pd.DataFrame({
        "date": daily["time"],
        "temp_max": daily["temperature_2m_max"],
        "temp_min": daily["temperature_2m_min"],
        "rainfall_mm": daily["precipitation_sum"],
    })


def inspect(df: pd.DataFrame) -> None:
    print(f"[inspect] shape={df.shape}")
    print(df.head())
    print("\ndtypes:")
    print(df.dtypes)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["temp_avg"] = (df["temp_max"] + df["temp_min"]) / 2
    return df


if __name__ == "__main__":
    try:
        df = read()
        inspect(df)
        cleaned = clean(df)
        print("\n[clean] forecast rows:", len(cleaned))
    except requests.RequestException as e:
        print(f"API call failed (need internet): {e}")
