from models import Tool, ToolParameter
import requests

def get_weather(location: str) -> str:
    """Get the weather for a given location using Open-Meteo API"""
    try:
        # Step 1: Geocode the location to get coordinates
        geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
        geocode_params = {
            "name": location,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        
        geocode_response = requests.get(geocode_url, params=geocode_params, timeout=5)
        geocode_response.raise_for_status()
        geocode_data = geocode_response.json()
        
        if not geocode_data.get("results"):
            return f"Location '{location}' not found. Please try a different location name."
        
        result = geocode_data["results"][0]
        latitude = result["latitude"]
        longitude = result["longitude"]
        found_location = result.get("name", location)
        country = result.get("country", "")
        
        # Step 2: Get current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            "timezone": "auto"
        }
        
        weather_response = requests.get(weather_url, params=weather_params, timeout=5)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        current = weather_data["current"]
        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        wind_speed = current["wind_speed_10m"]
        weather_code = current["weather_code"]
        
        # Map weather codes to descriptions (WMO Weather interpretation codes)
        weather_descriptions = {
            0: "clear sky",
            1: "mainly clear",
            2: "partly cloudy",
            3: "overcast",
            45: "foggy",
            48: "depositing rime fog",
            51: "light drizzle",
            53: "moderate drizzle",
            55: "dense drizzle",
            56: "light freezing drizzle",
            57: "dense freezing drizzle",
            61: "slight rain",
            63: "moderate rain",
            65: "heavy rain",
            66: "light freezing rain",
            67: "heavy freezing rain",
            71: "slight snow",
            73: "moderate snow",
            75: "heavy snow",
            77: "snow grains",
            80: "slight rain showers",
            81: "moderate rain showers",
            82: "violent rain showers",
            85: "slight snow showers",
            86: "heavy snow showers",
            95: "thunderstorm",
            96: "thunderstorm with slight hail",
            99: "thunderstorm with heavy hail"
        }
        
        weather_desc = weather_descriptions.get(weather_code, "unknown conditions")
        unit = weather_data["current_units"]["temperature_2m"]
        
        location_str = f"{found_location}, {country}" if country else found_location
        
        return (f"Current weather in {location_str}: "
                f"{temperature}{unit}, {weather_desc}, "
                f"humidity {humidity}%, wind {wind_speed} km/h")
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"
    except (KeyError, IndexError) as e:
        return f"Error parsing weather data: {str(e)}"

GET_WEATHER_TOOL = Tool(
    name="get_weather",
    description="Get the weather for a given location",
    parameters=[ToolParameter(name="location", type="string")],
)
