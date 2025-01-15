import requests
import math

def fetch_weather_data(lat, lon):
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'temperature_2m,relative_humidity_2m,rain,wind_speed_10m',
        'current_weather': True,
    }

    try:
        response = requests.get(base_url, params = params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    
def calculate_heat_index(temperature, humidity):
    temp_f = (temperature * 9 / 5) + 32

    constants = [-42.379, 2.04901523, 10.14333127, -0.22475541, -0.00683783, -0.05481717, 0.00122874, 0.00085282, -0.00000199]

    temp_f_sq = temp_f ** 2
    humidity_sq = humidity ** 2
    heat_index_f = (
        constants[0] +
        constants[1] * temp_f +
        constants[2] * humidity +
        constants[3] * temp_f * humidity +
        constants[4] * temp_f_sq +
        constants[5] * humidity_sq +
        constants[6] * temp_f_sq * humidity +
        constants[7] * temp_f * humidity_sq +
        constants[8] * temp_f_sq * humidity_sq
    )
    
    heat_index_c = (heat_index_f - 32) * 5/9
    return round(heat_index_c, 2)

def display_weather(lat, lon):
    weather_data = fetch_weather_data(lat, lon)

    if not weather_data:
        return

    try:
        current_weather = weather_data['current_weather']
        temperature = current_weather['temperature']
        humidity = weather_data['hourly']['relative_humidity_2m'][0]
        wind_speed = current_weather['windspeed']
        rainfall = weather_data['hourly']['rain'][0]

        heat_index = calculate_heat_index(temperature, humidity)

        print(f"Weather at coordinates ({lat}, {lon}):")
        print(f"Temperature: {temperature} °C")
        print(f"Humidity: {humidity} %")
        print(f"Rainfall (current hour): {rainfall} mm")
        print(f"Wind Speed: {wind_speed} m/s")
        print(f"Heat Index: {heat_index} °C")

    except KeyError as e:
        print(f"Error parsing data: Missing key {e}")

if __name__ == "__main__":
    LATITUDE = 10.3157
    LONGITUDE = 123.8854

    display_weather(LATITUDE, LONGITUDE)
