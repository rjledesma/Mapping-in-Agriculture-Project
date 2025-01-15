# returns risk levels for each predicted future weather conditions to be used for success_rate_prediction and harvest_date_estimation

import requests
from typing import List, Dict

latitude = 10.3157
longitude = 123.8854
api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max&timezone=Asia/Manila"

response = requests.get(api_url)
weather_data = response.json()

daily_forecasts = weather_data.get('daily', {})
dates = daily_forecasts.get('time', [])
max_temps = daily_forecasts.get('temperature_2m_max', [])
min_temps = daily_forecasts.get('temperature_2m_min', [])
precipitations = daily_forecasts.get('precipitation_sum', [])
max_wind_speeds = daily_forecasts.get('windspeed_10m_max', [])

weather_forecast = [
    {
        "day": dates[i],
        "temperature_max": max_temps[i],
        "temperature_min": min_temps[i],
        "precipitation": precipitations[i],
        "wind_speed": max_wind_speeds[i]
    }
    for i in range(len(dates))
]

def weather_impact_estimation(weather_forecast: List[Dict[str, float]]) -> List[Dict[str, str]]:
    def get_risk(value: float, thresholds: Dict[str, tuple]) -> str:
        return next((risk for risk, (low, high) in thresholds.items() if low <= value <= high), "Low")
    
    results = []

    temperature_thresholds = {
        "High": (-float("inf"), 0),
        "Medium": (0, 5),
        "Low": (5, 30),
        "Medium": (30, 35),
        "High": (35, float("inf"))
    }

    precipitation_thresholds = {
        "High": (50, float("inf")),
        "Medium": (20, 50),
        "Low": (0, 20)
    }

    wind_speed_thresholds = {
        "High": (20, float("inf")),
        "Medium": (10, 20),
        "Low": (0, 10)
    }

    risk_priority = {"Low": 0, "Medium": 1, "High": 2}

    for day in weather_forecast:
        temperature_risk = get_risk(day.get("temperature", 20), temperature_thresholds)
        precipitation_risk = get_risk(day.get("precipitation", 0), precipitation_thresholds)
        wind_risk = get_risk(day.get("wind_speed", 5), wind_speed_thresholds)

        overall_risk = max(
            {temperature_risk, precipitation_risk, wind_risk},
            key=lambda risk: risk_priority[risk]
        )

        results.append({
            "day": day.get("day", "Unknown"),
            "temperature_risk": temperature_risk,
            "precipitation_risk": precipitation_risk,
            "wind_risk": wind_risk,
            "overall_risk": overall_risk
        })

    return results
    
"""weather_forecast = [
    {"day": "2025-01-16", "temperature": 22, "precipitation": 10, "wind_speed": 5},
    {"day": "2025-01-17", "temperature": -5, "precipitation": 0, "wind_speed": 15},
    {"day": "2025-01-18", "temperature": 40, "precipitation": 60, "wind_speed": 25},
]"""

risk_estimation = weather_impact_estimation(weather_forecast)
for day_risk in risk_estimation:
    print(day_risk)
