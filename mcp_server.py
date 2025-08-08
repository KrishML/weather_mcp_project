#!/usr/bin/env python3
"""
MCP Server for Weather Agent
Provides standardized MCP interface for LLMs to access weather data
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from weather_mcp_agent import WeatherMCPAgent

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPServer:
    """Simple MCP Server for Weather Agent"""
    
    def __init__(self):
        self.weather_agent = WeatherMCPAgent()
        self.initialized = False
        
    async def initialize(self):
        """Initialize the MCP server"""
        await self.weather_agent.initialize()
        self.initialized = True
        logger.info("MCP Server initialized")
        
    async def cleanup(self):
        """Cleanup resources"""
        await self.weather_agent.cleanup()
        
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get available tools"""
        return [
            {
                "name": "get_current_weather",
                "description": "Get current weather data for a location",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City name or coordinates"
                        }
                    },
                    "required": ["location"]
                }
            },
            {
                "name": "get_weather_forecast",
                "description": "Get weather forecast for a location",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City name or coordinates"
                        },
                        "days": {
                            "type": "integer",
                            "description": "Number of days (default: 5)",
                            "default": 5
                        }
                    },
                    "required": ["location"]
                }
            }
        ]
        
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool with arguments"""
        if not self.initialized:
            await self.initialize()
            
        if tool_name == "get_current_weather":
            location = arguments.get("location")
            if not location:
                return {"error": "Location is required"}
                
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
                
        elif tool_name == "get_weather_forecast":
            location = arguments.get("location")
            days = arguments.get("days", 5)
            
            if not location:
                return {"error": "Location is required"}
                
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
        else:
            return {"error": f"Unknown tool: {tool_name}"}
            
    async def handle_mcp_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP messages"""
        message_type = message.get("jsonrpc")
        method = message.get("method")
        params = message.get("params", {})
        request_id = message.get("id")
        
        if method == "initialize":
            await self.initialize()
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "weather-mcp-agent",
                        "version": "1.0.0"
                    }
                }
            }
            
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": self.get_tools()
                }
            }
            
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            result = await self.call_tool(tool_name, arguments)
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            }
            
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }

async def main():
    """Main function - simple MCP server over stdio"""
    server = MCPServer()
    
    try:
        # Simple stdio-based MCP server
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                    
                message = json.loads(line.strip())
                response = await server.handle_mcp_message(message)
                
                print(json.dumps(response))
                sys.stdout.flush()
                
            except json.JSONDecodeError:
                logger.error("Invalid JSON received")
            except Exception as e:
                logger.error(f"Error handling message: {e}")
                
    except KeyboardInterrupt:
        logger.info("Shutting down MCP Server...")
    finally:
        await server.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
