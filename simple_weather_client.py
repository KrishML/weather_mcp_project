#!/usr/bin/env python3
"""
Simple Weather Client - Use the weather agent without frontend
"""

import asyncio
import requests
import json
from weather_mcp_agent import WeatherMCPAgent

class SimpleWeatherClient:
    """Simple client for weather data"""
    
    def __init__(self):
        self.agent = None
        
    async def initialize(self):
        """Initialize the weather agent"""
        self.agent = WeatherMCPAgent()
        await self.agent.initialize()
        
    async def get_weather(self, location: str):
        """Get current weather for a location"""
        if not self.agent:
            await self.initialize()
            
        weather = await self.agent.get_current_weather(location)
        return weather
        
    async def get_forecast(self, location: str, days: int = 5):
        """Get weather forecast for a location"""
        if not self.agent:
            await self.initialize()
            
        forecast = await self.agent.get_forecast(location, days)
        return forecast
        
    async def cleanup(self):
        """Cleanup resources"""
        if self.agent:
            await self.agent.cleanup()

def print_weather(weather):
    """Print weather data nicely"""
    if weather:
        print(f"🌤️ Weather in {weather.location}:")
        print(f"   Temperature: {weather.temperature}°C")
        print(f"   Feels like: {weather.feels_like}°C")
        print(f"   Humidity: {weather.humidity}%")
        print(f"   Conditions: {weather.description}")
        print(f"   Wind: {weather.wind_speed} m/s")
        print(f"   Pressure: {weather.pressure} hPa")
        print(f"   Visibility: {weather.visibility} m")
        print(f"   Updated: {weather.timestamp}")
    else:
        print("❌ Failed to fetch weather data")

def print_forecast(forecasts):
    """Print forecast data nicely"""
    if forecasts:
        print(f"📅 5-Day Forecast for {forecasts[0].location}:")
        for i, forecast in enumerate(forecasts[:8]):
            print(f"   {i+1}. {forecast.timestamp.strftime('%m/%d %H:%M')}: "
                  f"{forecast.temperature}°C, {forecast.description}")
    else:
        print("❌ Failed to fetch forecast")

async def main():
    """Main function"""
    client = SimpleWeatherClient()
    
    try:
        await client.initialize()
        
        # Test different cities
        cities = ["Kolkata", "Delhi", "Mumbai", "Bangalore", "Chennai"]
        
        for city in cities:
            print(f"\n{'='*50}")
            print(f"📍 Getting weather for {city}")
            print('='*50)
            
            # Get current weather
            weather = await client.get_weather(city)
            print_weather(weather)
            
            # Get forecast
            print(f"\n📅 Getting forecast for {city}...")
            forecast = await client.get_forecast(city, 3)
            print_forecast(forecast)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
