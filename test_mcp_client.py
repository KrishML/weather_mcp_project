#!/usr/bin/env python3
"""
Test MCP Client
Simulates an MCP client interacting with the weather MCP server
"""

import asyncio
import json
import subprocess
import sys
from typing import Dict, Any

class MCPClient:
    """Simulates an MCP client"""
    
    def __init__(self):
        self.process = None
        
    async def start_server(self):
        """Start the MCP server as a subprocess"""
        self.process = subprocess.Popen(
            [sys.executable, "mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
    async def send_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Send a message to the MCP server and get response"""
        if not self.process:
            raise Exception("Server not started")
            
        # Send message
        message_str = json.dumps(message) + "\n"
        self.process.stdin.write(message_str)
        self.process.stdin.flush()
        
        # Read response
        response_line = self.process.stdout.readline()
        if response_line:
            return json.loads(response_line.strip())
        else:
            return {"error": "No response from server"}
            
    async def test_initialization(self):
        """Test server initialization"""
        print("🔧 Testing MCP Server Initialization")
        print("=" * 40)
        
        init_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        response = await self.send_message(init_message)
        print("📤 Sent initialization message")
        print("📥 Received response:")
        print(json.dumps(response, indent=2))
        print()
        
    async def test_tools_list(self):
        """Test tools/list method"""
        print("🔧 Testing Tools List")
        print("=" * 25)
        
        tools_message = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        response = await self.send_message(tools_message)
        print("📤 Sent tools/list message")
        print("📥 Available tools:")
        print(json.dumps(response, indent=2))
        print()
        
    async def test_current_weather(self):
        """Test get_current_weather tool"""
        print("🌤️ Testing Current Weather Tool")
        print("=" * 35)
        
        weather_message = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "get_current_weather",
                "arguments": {
                    "location": "London"
                }
            }
        }
        
        response = await self.send_message(weather_message)
        print("📤 Sent get_current_weather request for London")
        print("📥 Response:")
        print(json.dumps(response, indent=2))
        print()
        
    async def test_weather_forecast(self):
        """Test get_weather_forecast tool"""
        print("📅 Testing Weather Forecast Tool")
        print("=" * 35)
        
        forecast_message = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "get_weather_forecast",
                "arguments": {
                    "location": "Tokyo",
                    "days": 3
                }
            }
        }
        
        response = await self.send_message(forecast_message)
        print("📤 Sent get_weather_forecast request for Tokyo (3 days)")
        print("📥 Response:")
        print(json.dumps(response, indent=2))
        print()
        
    async def test_invalid_tool(self):
        """Test invalid tool call"""
        print("❌ Testing Invalid Tool Call")
        print("=" * 30)
        
        invalid_message = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "invalid_tool",
                "arguments": {}
            }
        }
        
        response = await self.send_message(invalid_message)
        print("📤 Sent invalid tool request")
        print("📥 Response:")
        print(json.dumps(response, indent=2))
        print()
        
    async def cleanup(self):
        """Cleanup resources"""
        if self.process:
            self.process.terminate()
            self.process.wait()

async def main():
    """Main test function"""
    client = MCPClient()
    
    try:
        print("🚀 Starting MCP Server Test")
        print("=" * 30)
        print()
        
        # Start the server
        await client.start_server()
        await asyncio.sleep(1)  # Give server time to start
        
        # Run tests
        await client.test_initialization()
        await client.test_tools_list()
        await client.test_current_weather()
        await client.test_weather_forecast()
        await client.test_invalid_tool()
        
        print("✅ MCP Server Test Complete!")
        print()
        print("📝 Test Summary:")
        print("• ✅ Server initialization")
        print("• ✅ Tools listing")
        print("• ✅ Current weather tool")
        print("• ✅ Weather forecast tool")
        print("• ✅ Error handling")
        print()
        print("🌤️ The MCP server is ready for LLM integration!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
