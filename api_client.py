#!/usr/bin/env python3
"""
API Client - Use weather app via REST API
"""

import requests
import json

class WeatherAPIClient:
    """Client for weather REST API"""
    
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        
    def get_current_weather(self, location: str):
        """Get current weather via API"""
        url = f"{self.base_url}/api/weather/current"
        data = {"location": location}
        
        try:
            response = requests.post(url, json=data)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
            
    def get_weather_forecast(self, location: str, days: int = 5):
        """Get weather forecast via API"""
        url = f"{self.base_url}/api/weather/forecast"
        data = {"location": location, "days": days}
        
        try:
            response = requests.post(url, json=data)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
            
    def check_status(self):
        """Check API status"""
        url = f"{self.base_url}/api/status"
        
        try:
            response = requests.get(url)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

def print_api_response(response, title):
    """Print API response nicely"""
    print(f"\n{title}")
    print("=" * 50)
    
    if response.get("success"):
        data = response.get("data", {})
        if "location" in data:
            print(f"📍 Location: {data['location']}")
            print(f"🌡️ Temperature: {data.get('temperature', 'N/A')}")
            print(f"💨 Feels like: {data.get('feels_like', 'N/A')}")
            print(f"💧 Humidity: {data.get('humidity', 'N/A')}")
            print(f"☁️ Conditions: {data.get('description', 'N/A')}")
            print(f"🌪️ Wind: {data.get('wind_speed', 'N/A')}")
            print(f"📊 Pressure: {data.get('pressure', 'N/A')}")
            print(f"👁️ Visibility: {data.get('visibility', 'N/A')}")
            print(f"⏰ Updated: {data.get('timestamp', 'N/A')}")
        elif "forecast" in data:
            print(f"📅 Forecast for {data['location']}:")
            for i, item in enumerate(data['forecast'][:6]):
                print(f"   {i+1}. {item['timestamp']}: {item['temperature']}, {item['description']}")
    else:
        print(f"❌ Error: {response.get('error', 'Unknown error')}")

def main():
    """Main function"""
    client = WeatherAPIClient()
    
    print("🌤️ Weather API Client")
    print("=" * 30)
    
    # Check API status
    status = client.check_status()
    print(f"🔧 API Status: {status}")
    
    # Test cities
    cities = ["Kolkata", "Delhi", "Mumbai"]
    
    for city in cities:
        print(f"\n{'='*60}")
        print(f"📍 Testing {city}")
        print('='*60)
        
        # Get current weather
        weather_response = client.get_current_weather(city)
        print_api_response(weather_response, f"Current Weather for {city}")
        
        # Get forecast
        forecast_response = client.get_weather_forecast(city, 3)
        print_api_response(forecast_response, f"3-Day Forecast for {city}")

if __name__ == "__main__":
    main()
