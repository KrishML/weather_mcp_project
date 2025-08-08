#!/usr/bin/env python3
"""
Weather CLI - Command line interface for weather app
"""

import asyncio
import argparse
import sys
from weather_mcp_agent import WeatherMCPAgent

class WeatherCLI:
    """Command line interface for weather"""
    
    def __init__(self):
        self.agent = None
        
    async def initialize(self):
        """Initialize weather agent"""
        self.agent = WeatherMCPAgent()
        await self.agent.initialize()
        
    async def get_weather(self, location: str):
        """Get current weather"""
        if not self.agent:
            await self.initialize()
        return await self.agent.get_current_weather(location)
        
    async def get_forecast(self, location: str, days: int = 5):
        """Get weather forecast"""
        if not self.agent:
            await self.initialize()
        return await self.agent.get_forecast(location, days)
        
    async def cleanup(self):
        """Cleanup resources"""
        if self.agent:
            await self.agent.cleanup()
            
    def print_weather(self, weather):
        """Print weather data"""
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
            
    def print_forecast(self, forecasts):
        """Print forecast data"""
        if forecasts:
            print(f"📅 {len(forecasts)}-Day Forecast for {forecasts[0].location}:")
            for i, forecast in enumerate(forecasts[:8]):
                print(f"   {i+1}. {forecast.timestamp.strftime('%m/%d %H:%M')}: "
                      f"{forecast.temperature}°C, {forecast.description}")
        else:
            print("❌ Failed to fetch forecast")

async def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="Weather CLI - Get weather information")
    parser.add_argument("location", help="City name or location")
    parser.add_argument("--forecast", "-f", action="store_true", help="Get weather forecast")
    parser.add_argument("--days", "-d", type=int, default=5, help="Number of days for forecast (default: 5)")
    
    args = parser.parse_args()
    
    cli = WeatherCLI()
    
    try:
        await cli.initialize()
        
        if args.forecast:
            print(f"📅 Getting {args.days}-day forecast for {args.location}...")
            forecast = await cli.get_forecast(args.location, args.days)
            cli.print_forecast(forecast)
        else:
            print(f"🌤️ Getting current weather for {args.location}...")
            weather = await cli.get_weather(args.location)
            cli.print_weather(weather)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        await cli.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
