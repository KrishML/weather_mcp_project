#!/usr/bin/env python3
"""
Weather MCP Agent - A Python-based LLM weather fetcher agent using MCP
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

import aiohttp
import requests
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherData(BaseModel):
    """Weather data model"""
    location: str
    temperature: float
    feels_like: float
    humidity: int
    description: str
    wind_speed: float
    pressure: int
    visibility: int
    timestamp: datetime

class WeatherMCPAgent:
    """MCP Weather Agent for fetching and providing weather data to LLMs"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.session = None
        
    async def initialize(self):
        """Initialize the agent"""
        self.session = aiohttp.ClientSession()
        logger.info("Weather MCP Agent initialized")
        
    async def cleanup(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()
            
    async def get_current_weather(self, location: str) -> Optional[WeatherData]:
        """Fetch current weather data for a location"""
        if not self.api_key:
            logger.error("OpenWeather API key not found. Please set OPENWEATHER_API_KEY environment variable.")
            return None
            
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    weather_data = WeatherData(
                        location=location,
                        temperature=data["main"]["temp"],
                        feels_like=data["main"]["feels_like"],
                        humidity=data["main"]["humidity"],
                        description=data["weather"][0]["description"],
                        wind_speed=data["wind"]["speed"],
                        pressure=data["main"]["pressure"],
                        visibility=data.get("visibility", 0),
                        timestamp=datetime.fromtimestamp(data["dt"])
                    )
                    
                    logger.info(f"Weather data fetched for {location}")
                    return weather_data
                else:
                    logger.error(f"Failed to fetch weather data for {location}: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            return None
            
    async def get_forecast(self, location: str, days: int = 5) -> List[WeatherData]:
        """Fetch weather forecast for a location"""
        if not self.api_key:
            logger.error("OpenWeather API key not found")
            return []
            
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    forecasts = []
                    
                    for item in data["list"][:days * 8]:  # 8 forecasts per day
                        forecast = WeatherData(
                            location=location,
                            temperature=item["main"]["temp"],
                            feels_like=item["main"]["feels_like"],
                            humidity=item["main"]["humidity"],
                            description=item["weather"][0]["description"],
                            wind_speed=item["wind"]["speed"],
                            pressure=item["main"]["pressure"],
                            visibility=item.get("visibility", 0),
                            timestamp=datetime.fromtimestamp(item["dt"])
                        )
                        forecasts.append(forecast)
                    
                    logger.info(f"Forecast data fetched for {location}")
                    return forecasts
                else:
                    logger.error(f"Failed to fetch forecast for {location}: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error fetching forecast: {e}")
            return []

class WeatherMCPServer:
    """MCP Server for weather data"""
    
    def __init__(self):
        self.weather_agent = WeatherMCPAgent()
        self.server = Server("weather-mcp-agent")
        
    async def initialize(self):
        """Initialize the MCP server"""
        await self.weather_agent.initialize()
        
        # Register tools
        self.server.tool(
            "get_current_weather",
            "Get current weather data for a location",
            self.get_current_weather_tool
        )
        
        self.server.tool(
            "get_weather_forecast",
            "Get weather forecast for a location",
            self.get_forecast_tool
        )
        
        logger.info("Weather MCP Server initialized")
        
    async def get_current_weather_tool(self, location: str) -> Dict[str, Any]:
        """MCP tool for getting current weather"""
        weather_data = await self.weather_agent.get_current_weather(location)
        
        if weather_data:
            return {
                "location": weather_data.location,
                "temperature": f"{weather_data.temperature}°C",
                "feels_like": f"{weather_data.feels_like}°C",
                "humidity": f"{weather_data.humidity}%",
                "description": weather_data.description,
                "wind_speed": f"{weather_data.wind_speed} m/s",
                "pressure": f"{weather_data.pressure} hPa",
                "visibility": f"{weather_data.visibility} m",
                "timestamp": weather_data.timestamp.isoformat()
            }
        else:
            return {"error": f"Failed to fetch weather data for {location}"}
            
    async def get_forecast_tool(self, location: str, days: int = 5) -> Dict[str, Any]:
        """MCP tool for getting weather forecast"""
        forecasts = await self.weather_agent.get_forecast(location, days)
        
        if forecasts:
            forecast_data = []
            for forecast in forecasts:
                forecast_data.append({
                    "timestamp": forecast.timestamp.isoformat(),
                    "temperature": f"{forecast.temperature}°C",
                    "description": forecast.description,
                    "humidity": f"{forecast.humidity}%",
                    "wind_speed": f"{forecast.wind_speed} m/s"
                })
            
            return {
                "location": location,
                "forecast": forecast_data
            }
        else:
            return {"error": f"Failed to fetch forecast for {location}"}
            
    async def run(self):
        """Run the MCP server"""
        await self.initialize()
        
        async with stdio_server() as (read_stream, write_stream):
            async with ClientSession(
                StdioServerParameters(
                    read_stream=read_stream,
                    write_stream=write_stream
                )
            ) as session:
                await self.server.run(session)
                
    async def cleanup(self):
        """Cleanup resources"""
        await self.weather_agent.cleanup()

async def main():
    """Main function"""
    server = WeatherMCPServer()
    
    try:
        await server.run()
    except KeyboardInterrupt:
        logger.info("Shutting down Weather MCP Agent...")
    finally:
        await server.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
