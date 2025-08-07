#!/usr/bin/env python3
"""
Test script for the Weather MCP Agent
"""

import asyncio
import os
from dotenv import load_dotenv
from weather_mcp_agent import WeatherMCPAgent

async def test_weather_agent():
    """Test the weather agent functionality"""
    load_dotenv()
    
    # Check if API key is set
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("❌ OPENWEATHER_API_KEY not found in environment variables")
        print("Please set your OpenWeather API key:")
        print("export OPENWEATHER_API_KEY='your_api_key_here'")
        return
    
    print("🌤️  Testing Weather MCP Agent...")
    
    # Initialize the agent
    agent = WeatherMCPAgent()
    await agent.initialize()
    
    try:
        # Test current weather
        print("\n📍 Testing current weather for London...")
        weather = await agent.get_current_weather("London")
        
        if weather:
            print(f"✅ Current weather for {weather.location}:")
            print(f"   Temperature: {weather.temperature}°C")
            print(f"   Feels like: {weather.feels_like}°C")
            print(f"   Humidity: {weather.humidity}%")
            print(f"   Description: {weather.description}")
            print(f"   Wind Speed: {weather.wind_speed} m/s")
            print(f"   Pressure: {weather.pressure} hPa")
            print(f"   Visibility: {weather.visibility} m")
            print(f"   Timestamp: {weather.timestamp}")
        else:
            print("❌ Failed to fetch current weather")
        
        # Test forecast
        print("\n📅 Testing weather forecast for New York...")
        forecasts = await agent.get_forecast("New York", days=3)
        
        if forecasts:
            print(f"✅ Weather forecast for {forecasts[0].location}:")
            for i, forecast in enumerate(forecasts[:6]):  # Show first 6 forecasts
                print(f"   {i+1}. {forecast.timestamp.strftime('%Y-%m-%d %H:%M')}: "
                      f"{forecast.temperature}°C, {forecast.description}")
        else:
            print("❌ Failed to fetch weather forecast")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        
    finally:
        await agent.cleanup()
        print("\n🏁 Test completed!")

if __name__ == "__main__":
    asyncio.run(test_weather_agent())
