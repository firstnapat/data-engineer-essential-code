"""
Exercise: REST APIs — Fetch, Parse, Clean, and Summarise
Practice the read (fetch + parse) → inspect → clean pattern from work_with_api.py

Uses the Open-Meteo weather API (free, no auth). Requires internet.
Run: uv run 03_data_sources/02_apis/exercise/exercise.py
"""
import requests
import pandas as pd

# Chiang Mai coordinates (different city from the teaching script's Bangkok)
LAT, LON, TZ = 18.79, 98.98, "Asia/Bangkok"

try:
    # ------------------------------------------------------------------
    # Task 1: Fetch a 3-day forecast and parse into a DataFrame
    # ------------------------------------------------------------------
    print("--- Task 1: Fetch weather forecast for Chiang Mai ---")

    # TODO: Use requests.get() to call the Open-Meteo forecast API.
    #   URL:    https://api.open-meteo.com/v1/forecast
    #   Params: latitude, longitude, timezone, forecast_days=3,
    #           daily="temperature_2m_max,temperature_2m_min,precipitation_sum"
    #   Don't forget timeout=10 and resp.raise_for_status().
    #
    # Then parse resp.json()["daily"] into a DataFrame with columns:
    #   date, temp_max, temp_min, rainfall_mm
    # Hint: Look at the read() function in work_with_api.py.

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        # TODO: fill in the params dict
    }

    # TODO: Make the request and parse the response
    # resp = ...
    # daily = ...

    forecast_df = ...  # TODO: build the DataFrame from 'daily'

    print(forecast_df)
    print(f"dtypes:\n{forecast_df.dtypes}\n")

    # Verification
    assert forecast_df.shape == (3, 4), f"Expected (3, 4), got {forecast_df.shape}"
    assert list(forecast_df.columns) == ["date", "temp_max", "temp_min", "rainfall_mm"], \
        f"Unexpected columns: {list(forecast_df.columns)}"
    print("✓ Task 1 passed\n")

    # ------------------------------------------------------------------
    # Task 2: Add error handling
    # ------------------------------------------------------------------
    print("--- Task 2: Error handling with try/except ---")

    # TODO: Write a fetch_forecast() function that wraps your Task 1 code
    #       in a try/except block. Catch requests.RequestException.
    #       On success, return the DataFrame.
    #       On failure, print an error message and return an empty DataFrame.
    # Hint: Follow the pattern from the __main__ block in work_with_api.py.

    def fetch_forecast(lat: float, lon: float, days: int = 3) -> pd.DataFrame:
        """Fetch weather forecast; return empty DataFrame on failure."""
        # TODO: implement this function
        ...

    # Test with valid coordinates
    result = fetch_forecast(LAT, LON, days=3)
    assert not result.empty, "Expected non-empty DataFrame for valid coordinates"
    print(f"fetch_forecast() returned {len(result)} rows")

    # Test with intentionally bad URL to verify error handling
    print("Testing error handling with bad request...")
    bad_result = fetch_forecast(999, 999, days=3)  # invalid coordinates
    # Note: Open-Meteo may still return data for out-of-range coords or
    # return a 400 error — either way, your function should handle it gracefully.
    print("✓ Task 2 passed (error handling works)\n")

    # ------------------------------------------------------------------
    # Task 3: Clean the forecast data
    # ------------------------------------------------------------------
    print("--- Task 3: Clean function — datetime + temp_range ---")

    # TODO: Write a clean() function that:
    #   1. Copies the DataFrame
    #   2. Converts 'date' column to datetime using pd.to_datetime()
    #   3. Adds a 'temp_range' column = temp_max - temp_min
    #   4. Returns the cleaned DataFrame
    # Hint: Same pattern as clean() in work_with_api.py (which adds temp_avg).

    def clean(df: pd.DataFrame) -> pd.DataFrame:
        # TODO: implement this function
        ...

    cleaned = clean(forecast_df)
    print(cleaned)
    print(f"\ndtypes:\n{cleaned.dtypes}")

    # Verification
    assert str(cleaned["date"].dtype).startswith("datetime64"), \
        f"Expected datetime64 for date, got {cleaned['date'].dtype}"
    assert "temp_range" in cleaned.columns, "Missing 'temp_range' column"
    expected_range = cleaned["temp_max"] - cleaned["temp_min"]
    assert (cleaned["temp_range"] == expected_range).all(), "temp_range values are incorrect"
    print("✓ Task 3 passed\n")

    # ------------------------------------------------------------------
    # Task 4: Print a summary
    # ------------------------------------------------------------------
    print("--- Task 4: Summary statistics ---")

    # TODO: Using the cleaned DataFrame, print:
    #   1. Average temp_max (rounded to 1 decimal)
    #   2. Total rainfall in mm (rounded to 1 decimal)
    # Hint: Use .mean() and .sum()

    avg_temp_max = ...   # TODO: calculate average of temp_max
    total_rain = ...     # TODO: calculate sum of rainfall_mm

    print(f"Chiang Mai 3-day forecast summary:")
    print(f"  Average high temperature: {avg_temp_max}°C")
    print(f"  Total rainfall:           {total_rain} mm")

    # Verification
    assert isinstance(avg_temp_max, float), "avg_temp_max should be a float"
    assert isinstance(total_rain, float), "total_rain should be a float"
    print("✓ Task 4 passed\n")

    print("=" * 50)
    print("All tasks passed! 🎉")

except requests.RequestException as e:
    print(f"\n⚠️  Could not complete exercise — network error: {e}")
    print("This exercise requires an internet connection to call the Open-Meteo API.")
    print("Please check your connection and try again.")
