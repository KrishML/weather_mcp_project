# Weather MCP Agent 🌤️

A Python-based LLM weather fetcher agent using the Model Context Protocol (MCP). This agent provides real-time weather data and forecasts to Large Language Models through a standardized MCP interface.

## Features

- 🌡️ **Current Weather Data**: Get real-time weather information for any location
- 📅 **Weather Forecasts**: Retrieve 5-day weather forecasts with detailed information
- 🤖 **MCP Integration**: Seamless integration with LLMs through the Model Context Protocol
- 🔄 **Async Support**: Built with asyncio for efficient concurrent operations
- 📊 **Rich Data**: Comprehensive weather data including temperature, humidity, wind speed, pressure, and visibility
- 🛡️ **Error Handling**: Robust error handling and logging

## Prerequisites

- Python 3.8+
- OpenWeather API key (free at [OpenWeatherMap](https://openweathermap.org/api))

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd cursor_projects/weather_mcp_project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenWeather API key:**
   ```bash
   export OPENWEATHER_API_KEY='your_api_key_here'
   ```
   
   Or create a `.env` file:
   ```bash
   echo "OPENWEATHER_API_KEY=your_api_key_here" > .env
   ```

## Usage

### 1. Testing the Weather Agent

Run the test script to verify everything is working:

```bash
python test_weather_agent.py
```

This will test both current weather and forecast functionality.

### 2. Running the MCP Server

Start the MCP server:

```bash
python weather_mcp_agent.py
```

The server will start and be ready to accept MCP connections.

### 3. MCP Configuration

The `mcp-config.json` file contains the configuration for the MCP server:

```json
{
  "mcpServers": {
    "weather-agent": {
      "command": "python",
      "args": ["weather_mcp_agent.py"],
      "env": {
        "OPENWEATHER_API_KEY": "${OPENWEATHER_API_KEY}"
      }
    }
  }
}
```

## Available MCP Tools

### 1. `get_current_weather`
Get current weather data for a location.

**Parameters:**
- `location` (string): City name or coordinates

**Returns:**
```json
{
  "location": "London",
  "temperature": "18.5°C",
  "feels_like": "17.2°C",
  "humidity": "65%",
  "description": "scattered clouds",
  "wind_speed": "3.2 m/s",
  "pressure": "1013 hPa",
  "visibility": "10000 m",
  "timestamp": "2024-01-15T14:30:00"
}
```

### 2. `get_weather_forecast`
Get weather forecast for a location.

**Parameters:**
- `location` (string): City name or coordinates
- `days` (integer, optional): Number of days (default: 5)

**Returns:**
```json
{
  "location": "New York",
  "forecast": [
    {
      "timestamp": "2024-01-15T12:00:00",
      "temperature": "22.1°C",
      "description": "clear sky",
      "humidity": "45%",
      "wind_speed": "2.1 m/s"
    }
  ]
}
```

## Architecture

```
Weather MCP Agent
├── WeatherMCPAgent          # Core weather data fetcher
│   ├── get_current_weather() # Fetch current weather
│   └── get_forecast()       # Fetch weather forecast
├── WeatherMCPServer         # MCP server implementation
│   ├── get_current_weather_tool() # MCP tool wrapper
│   └── get_forecast_tool()  # MCP tool wrapper
└── WeatherData              # Pydantic data model
```

## Data Model

The `WeatherData` model includes:

- **location**: City name
- **temperature**: Current temperature in Celsius
- **feels_like**: Apparent temperature
- **humidity**: Relative humidity percentage
- **description**: Weather condition description
- **wind_speed**: Wind speed in m/s
- **pressure**: Atmospheric pressure in hPa
- **visibility**: Visibility in meters
- **timestamp**: Data timestamp

## Error Handling

The agent includes comprehensive error handling:

- API key validation
- Network request error handling
- Invalid location handling
- Rate limiting consideration
- Graceful degradation

## Logging

The agent uses Python's logging module with INFO level by default. Logs include:

- Agent initialization
- Successful data fetches
- Error conditions
- Server startup/shutdown

## Environment Variables

- `OPENWEATHER_API_KEY`: Your OpenWeather API key (required)

## Dependencies

- `mcp`: Model Context Protocol implementation
- `aiohttp`: Async HTTP client
- `requests`: HTTP library
- `python-dotenv`: Environment variable management
- `pydantic`: Data validation
- `fastapi`: Web framework (for potential web interface)
- `uvicorn`: ASGI server

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the logs for error messages
2. Verify your API key is set correctly
3. Ensure you have a stable internet connection
4. Check the OpenWeather API status

---

**Happy Weather Fetching! 🌤️**
