#!/usr/bin/env python3
"""
Test LLM Weather Integration
Simulates how an LLM would use the weather agent
"""

import asyncio
import json
from weather_mcp_agent import WeatherMCPAgent

class LLMWeatherTester:
    """Test LLM integration with weather agent"""
    
    def __init__(self):
        self.agent = None
        
    async def initialize(self):
        """Initialize weather agent"""
        self.agent = WeatherMCPAgent()
        await self.agent.initialize()
        
    async def simulate_llm_conversation(self):
        """Simulate LLM conversation with weather queries"""
        
        print("🤖 LLM Weather Integration Test")
        print("=" * 40)
        print()
        
        # Test 1: Simple weather query
        print("👤 User: What's the weather in Paris?")
        print("🤖 LLM: Let me check the current weather for Paris...")
        
        weather = await self.agent.get_current_weather("Paris")
        if weather:
            print(f"🤖 LLM: The weather in Paris is {weather.temperature}°C with {weather.description}.")
            print(f"   It feels like {weather.feels_like}°C with {weather.humidity}% humidity.")
        else:
            print("🤖 LLM: Sorry, I couldn't get the weather for Paris.")
        print()
        
        # Test 2: Weather comparison
        print("👤 User: Compare weather in London and Tokyo")
        print("🤖 LLM: I'll check the weather in both cities...")
        
        london_weather = await self.agent.get_current_weather("London")
        tokyo_weather = await self.agent.get_current_weather("Tokyo")
        
        if london_weather and tokyo_weather:
            print(f"🤖 LLM: Here's the comparison:")
            print(f"   London: {london_weather.temperature}°C, {london_weather.description}")
            print(f"   Tokyo: {tokyo_weather.temperature}°C, {tokyo_weather.description}")
            
            if london_weather.temperature > tokyo_weather.temperature:
                print(f"   London is {london_weather.temperature - tokyo_weather.temperature:.1f}°C warmer than Tokyo.")
            else:
                print(f"   Tokyo is {tokyo_weather.temperature - london_weather.temperature:.1f}°C warmer than London.")
        else:
            print("🤖 LLM: Sorry, I couldn't get weather data for comparison.")
        print()
        
        # Test 3: Forecast planning
        print("👤 User: I'm planning a trip to New York next week. What's the forecast?")
        print("🤖 LLM: Let me get the 5-day forecast for New York...")
        
        forecast = await self.agent.get_forecast("New York", 5)
        if forecast:
            print(f"🤖 LLM: Here's the 5-day forecast for New York:")
            daily_forecasts = {}
            for f in forecast:
                date_key = f.timestamp.strftime('%Y-%m-%d')
                if date_key not in daily_forecasts:
                    daily_forecasts[date_key] = []
                daily_forecasts[date_key].append(f)
            
            for date, forecasts in list(daily_forecasts.items())[:5]:
                avg_temp = sum(f.temperature for f in forecasts) / len(forecasts)
                most_common = max(set(f.description for f in forecasts), 
                                key=lambda x: sum(1 for f in forecasts if f.description == x))
                date_obj = f.timestamp.strptime(date, '%Y-%m-%d')
                day_name = date_obj.strftime('%A')
                print(f"   {day_name}: {avg_temp:.1f}°C, {most_common}")
        else:
            print("🤖 LLM: Sorry, I couldn't get the forecast for New York.")
        print()
        
        # Test 4: Weather recommendation
        print("👤 User: Should I bring an umbrella to Mumbai today?")
        print("🤖 LLM: Let me check the current weather in Mumbai...")
        
        mumbai_weather = await self.agent.get_current_weather("Mumbai")
        if mumbai_weather:
            if "rain" in mumbai_weather.description.lower():
                print(f"🤖 LLM: Yes, bring an umbrella! It's currently {mumbai_weather.description} in Mumbai.")
            elif mumbai_weather.humidity > 80:
                print(f"🤖 LLM: Maybe bring an umbrella. It's {mumbai_weather.humidity}% humidity with {mumbai_weather.description}.")
            else:
                print(f"🤖 LLM: Probably not needed. It's {mumbai_weather.description} with {mumbai_weather.humidity}% humidity.")
        else:
            print("🤖 LLM: Sorry, I couldn't check the weather for Mumbai.")
        print()
        
        # Test 5: MCP tool format
        print("🔧 MCP Tool Examples:")
        print("When an LLM uses the weather agent, it would call:")
        print()
        print("1. Current weather tool:")
        tool_call = {
            "tool": "get_current_weather",
            "arguments": {"location": "San Francisco"}
        }
        print(json.dumps(tool_call, indent=2))
        print()
        print("2. Forecast tool:")
        forecast_call = {
            "tool": "get_weather_forecast", 
            "arguments": {"location": "London", "days": 3}
        }
        print(json.dumps(forecast_call, indent=2))
        print()
        
        print("✅ LLM Integration Test Complete!")
        
    async def cleanup(self):
        """Cleanup resources"""
        if self.agent:
            await self.agent.cleanup()

async def main():
    """Main function"""
    tester = LLMWeatherTester()
    
    try:
        await tester.initialize()
        await tester.simulate_llm_conversation()
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await tester.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
