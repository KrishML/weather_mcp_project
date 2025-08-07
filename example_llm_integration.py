#!/usr/bin/env python3
"""
Example: Weather MCP Agent Integration with LLM
This script demonstrates how to use the weather agent with an LLM
"""

import asyncio
import json
import os
from dotenv import load_dotenv
from weather_mcp_agent import WeatherMCPAgent

async def weather_llm_example():
    """Example of how an LLM might use the weather agent"""
    load_dotenv()
    
    # Initialize the weather agent
    agent = WeatherMCPAgent()
    await agent.initialize()
    
    try:
        # Simulate LLM requesting weather information
        print("🤖 LLM: I need to know the weather in Tokyo for my user.")
        
        # LLM calls the weather agent
        weather_data = await agent.get_current_weather("Tokyo")
        
        if weather_data:
            # LLM receives structured data and can format it for the user
            response = f"""
🌤️ Current Weather in {weather_data.location}:

🌡️ Temperature: {weather_data.temperature}°C
💨 Feels like: {weather_data.feels_like}°C
💧 Humidity: {weather_data.humidity}%
☁️ Conditions: {weather_data.description}
🌪️ Wind Speed: {weather_data.wind_speed} m/s
📊 Pressure: {weather_data.pressure} hPa
👁️ Visibility: {weather_data.visibility} m
⏰ Last updated: {weather_data.timestamp.strftime('%Y-%m-%d %H:%M')}
            """
            print(response)
        else:
            print("❌ LLM: Sorry, I couldn't fetch the weather data for Tokyo.")
        
        # Simulate LLM requesting forecast
        print("\n🤖 LLM: My user also wants a 3-day forecast for Paris.")
        
        forecasts = await agent.get_forecast("Paris", days=3)
        
        if forecasts:
            response = f"""
📅 3-Day Weather Forecast for {forecasts[0].location}:

"""
            for i, forecast in enumerate(forecasts[:8]):  # Show 8 forecasts (about 1 day)
                response += f"📅 {forecast.timestamp.strftime('%m/%d %H:%M')}: "
                response += f"{forecast.temperature}°C, {forecast.description}\n"
            
            print(response)
        else:
            print("❌ LLM: Sorry, I couldn't fetch the forecast for Paris.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        await agent.cleanup()

async def mcp_tool_example():
    """Example of how the MCP tools would be called"""
    print("\n🔧 MCP Tool Usage Examples:")
    
    # Example 1: Current weather tool call
    print("\n1. get_current_weather tool call:")
    print("""
    {
      "tool": "get_current_weather",
      "arguments": {
        "location": "San Francisco"
      }
    }
    """)
    
    # Example 2: Forecast tool call
    print("2. get_weather_forecast tool call:")
    print("""
    {
      "tool": "get_weather_forecast",
      "arguments": {
        "location": "London",
        "days": 5
      }
    }
    """)
    
    print("3. Expected response format:")
    print("""
    {
      "location": "San Francisco",
      "temperature": "18.5°C",
      "feels_like": "17.2°C",
      "humidity": "65%",
      "description": "scattered clouds",
      "wind_speed": "3.2 m/s",
      "pressure": "1013 hPa",
      "visibility": "10000 m",
      "timestamp": "2024-01-15T14:30:00"
    }
    """)

if __name__ == "__main__":
    print("🌤️ Weather MCP Agent - LLM Integration Example")
    print("=" * 50)
    
    # Run the LLM integration example
    asyncio.run(weather_llm_example())
    
    # Show MCP tool examples
    asyncio.run(mcp_tool_example())
    
    print("\n✅ Example completed!")
    print("\nTo use this with an actual LLM:")
    print("1. Start the MCP server: python weather_mcp_agent.py")
    print("2. Configure your LLM to use the MCP tools")
    print("3. The LLM can now fetch weather data through the MCP interface")
