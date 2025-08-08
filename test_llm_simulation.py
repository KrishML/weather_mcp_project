#!/usr/bin/env python3
"""
LLM Integration Simulation
This script simulates how an LLM would use the weather agent
"""

import asyncio
import json
from datetime import datetime
from weather_mcp_agent import WeatherMCPAgent

class LLMSimulation:
    """Simulates LLM interaction with weather agent"""
    
    def __init__(self):
        self.weather_agent = None
        
    async def initialize(self):
        """Initialize the weather agent"""
        self.weather_agent = WeatherMCPAgent()
        await self.weather_agent.initialize()
        
    async def simulate_llm_conversation(self):
        """Simulate a conversation between user, LLM, and weather agent"""
        
        print("🤖 LLM Integration Simulation")
        print("=" * 50)
        print()
        
        # Simulate user asking about weather
        user_question = "What's the weather like in London today?"
        print(f"👤 User: {user_question}")
        print()
        
        # LLM decides to use weather agent
        print("🤖 LLM: I need to check the current weather for London.")
        print("🤖 LLM: Calling weather agent...")
        
        # LLM calls weather agent
        weather_data = await self.weather_agent.get_current_weather("London")
        
        if weather_data:
            # LLM processes the data and responds to user
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
            print("🤖 LLM: Here's the current weather information:")
            print(response)
        else:
            print("❌ LLM: Sorry, I couldn't fetch the weather data for London.")
            
        print("-" * 50)
        
        # Simulate user asking for forecast
        user_question2 = "What's the weather forecast for Tokyo this week?"
        print(f"👤 User: {user_question2}")
        print()
        
        print("🤖 LLM: I'll get the weather forecast for Tokyo.")
        print("🤖 LLM: Calling weather agent for forecast...")
        
        # LLM calls weather agent for forecast
        forecasts = await self.weather_agent.get_forecast("Tokyo", days=5)
        
        if forecasts:
            response = f"""
📅 5-Day Weather Forecast for {forecasts[0].location}:

"""
            # Group forecasts by day
            daily_forecasts = {}
            for forecast in forecasts:
                date_key = forecast.timestamp.strftime('%Y-%m-%d')
                if date_key not in daily_forecasts:
                    daily_forecasts[date_key] = []
                daily_forecasts[date_key].append(forecast)
            
            for date, day_forecasts in list(daily_forecasts.items())[:5]:
                avg_temp = sum(f.temperature for f in day_forecasts) / len(day_forecasts)
                most_common_desc = max(set(f.description for f in day_forecasts), 
                                     key=lambda x: sum(1 for f in day_forecasts if f.description == x))
                
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                day_name = date_obj.strftime('%A')
                
                response += f"📅 {day_name} ({date_obj.strftime('%m/%d')}): {avg_temp:.1f}°C, {most_common_desc}\n"
            
            print("🤖 LLM: Here's the weather forecast:")
            print(response)
        else:
            print("❌ LLM: Sorry, I couldn't fetch the forecast for Tokyo.")
            
        print("-" * 50)
        
        # Simulate MCP tool calls
        print("🔧 MCP Tool Integration Examples:")
        print()
        
        # Example 1: Current weather tool call
        print("1. LLM calls get_current_weather tool:")
        tool_call_1 = {
            "tool": "get_current_weather",
            "arguments": {
                "location": "San Francisco"
            }
        }
        print(json.dumps(tool_call_1, indent=2))
        print()
        
        # Example 2: Forecast tool call
        print("2. LLM calls get_weather_forecast tool:")
        tool_call_2 = {
            "tool": "get_weather_forecast",
            "arguments": {
                "location": "New York",
                "days": 3
            }
        }
        print(json.dumps(tool_call_2, indent=2))
        print()
        
        # Example 3: Tool response
        print("3. Weather agent responds with data:")
        tool_response = {
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
        print(json.dumps(tool_response, indent=2))
        print()
        
        print("✅ LLM Integration Simulation Complete!")
        print()
        print("📝 Key Benefits:")
        print("• LLMs can access real-time weather data")
        print("• Structured data format for easy processing")
        print("• Standardized MCP interface")
        print("• Async support for efficient operations")
        print("• Error handling and fallbacks")

async def main():
    """Main function"""
    simulation = LLMSimulation()
    
    try:
        await simulation.initialize()
        await simulation.simulate_llm_conversation()
    except Exception as e:
        print(f"❌ Error during simulation: {e}")
    finally:
        if simulation.weather_agent:
            await simulation.weather_agent.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
