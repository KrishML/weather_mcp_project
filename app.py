#!/usr/bin/env python3
"""
Weather MCP Agent - Web Frontend
A simple Flask web application for the weather agent
"""

import asyncio
import json
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from weather_mcp_agent import WeatherMCPAgent

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize weather agent
weather_agent = None

async def get_weather_agent():
    """Get or create weather agent instance"""
    global weather_agent
    if weather_agent is None:
        weather_agent = WeatherMCPAgent()
        await weather_agent.initialize()
    return weather_agent

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/weather/current', methods=['POST'])
def get_current_weather():
    """API endpoint for current weather"""
    try:
        data = request.get_json()
        location = data.get('location', 'London')
        
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def fetch_weather():
            agent = await get_weather_agent()
            return await agent.get_current_weather(location)
        
        weather_data = loop.run_until_complete(fetch_weather())
        loop.close()
        
        if weather_data:
            return jsonify({
                'success': True,
                'data': {
                    'location': weather_data.location,
                    'temperature': f"{weather_data.temperature}°C",
                    'feels_like': f"{weather_data.feels_like}°C",
                    'humidity': f"{weather_data.humidity}%",
                    'description': weather_data.description,
                    'wind_speed': f"{weather_data.wind_speed} m/s",
                    'pressure': f"{weather_data.pressure} hPa",
                    'visibility': f"{weather_data.visibility} m",
                    'timestamp': weather_data.timestamp.isoformat()
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to fetch weather data for {location}'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/weather/forecast', methods=['POST'])
def get_weather_forecast():
    """API endpoint for weather forecast"""
    try:
        data = request.get_json()
        location = data.get('location', 'London')
        days = data.get('days', 5)
        
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def fetch_forecast():
            agent = await get_weather_agent()
            return await agent.get_forecast(location, days)
        
        forecasts = loop.run_until_complete(fetch_forecast())
        loop.close()
        
        if forecasts:
            forecast_data = []
            for forecast in forecasts:
                forecast_data.append({
                    'timestamp': forecast.timestamp.isoformat(),
                    'temperature': f"{forecast.temperature}°C",
                    'description': forecast.description,
                    'humidity': f"{forecast.humidity}%",
                    'wind_speed': f"{forecast.wind_speed} m/s"
                })
            
            return jsonify({
                'success': True,
                'data': {
                    'location': location,
                    'forecast': forecast_data
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to fetch forecast for {location}'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/status')
def status():
    """API endpoint to check if API key is configured"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    return jsonify({
        'api_key_configured': bool(api_key),
        'api_key_length': len(api_key) if api_key else 0
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
