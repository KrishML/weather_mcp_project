// Weather MCP Agent Frontend JavaScript

class WeatherApp {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.checkApiStatus();
    }

    initializeElements() {
        // Search elements
        this.locationInput = document.getElementById('locationInput');
        this.searchBtn = document.getElementById('searchBtn');
        this.apiStatus = document.getElementById('apiStatus');

        // Weather display elements
        this.weatherSection = document.getElementById('weatherSection');
        this.currentWeather = document.getElementById('currentWeather');
        this.forecastCard = document.getElementById('forecastCard');
        this.forecastContainer = document.getElementById('forecastContainer');

        // Current weather elements
        this.currentTemp = document.getElementById('currentTemp');
        this.currentLocation = document.getElementById('currentLocation');
        this.currentDescription = document.getElementById('currentDescription');
        this.feelsLike = document.getElementById('feelsLike');
        this.humidity = document.getElementById('humidity');
        this.windSpeed = document.getElementById('windSpeed');
        this.pressure = document.getElementById('pressure');
        this.visibility = document.getElementById('visibility');
        this.timestamp = document.getElementById('timestamp');

        // Error and loading elements
        this.errorSection = document.getElementById('errorSection');
        this.errorMessage = document.getElementById('errorMessage');
        this.loadingSection = document.getElementById('loadingSection');
    }

    bindEvents() {
        // Search button click
        this.searchBtn.addEventListener('click', () => this.searchWeather());
        
        // Enter key in input
        this.locationInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.searchWeather();
            }
        });

        // Auto-search on input change (debounced)
        let searchTimeout;
        this.locationInput.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.locationInput.value.trim()) {
                    this.searchWeather();
                }
            }, 1000);
        });
    }

    async checkApiStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            if (data.api_key_configured) {
                this.apiStatus.innerHTML = '<i class="fas fa-circle"></i> API Key Configured';
                this.apiStatus.classList.add('connected');
            } else {
                this.apiStatus.innerHTML = '<i class="fas fa-circle"></i> API Key Not Configured';
                this.apiStatus.classList.add('error');
            }
        } catch (error) {
            this.apiStatus.innerHTML = '<i class="fas fa-circle"></i> Connection Error';
            this.apiStatus.classList.add('error');
        }
    }

    async searchWeather() {
        const location = this.locationInput.value.trim();
        
        if (!location) {
            this.showError('Please enter a location');
            return;
        }

        this.showLoading();
        this.hideError();
        this.hideWeather();

        try {
            // Fetch current weather
            const currentWeatherResponse = await fetch('/api/weather/current', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ location })
            });

            const currentWeatherData = await currentWeatherResponse.json();

            // Fetch forecast
            const forecastResponse = await fetch('/api/weather/forecast', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ location, days: 5 })
            });

            const forecastData = await forecastResponse.json();

            this.hideLoading();

            if (currentWeatherData.success && forecastData.success) {
                this.displayWeather(currentWeatherData.data, forecastData.data);
            } else {
                const error = currentWeatherData.error || forecastData.error || 'Failed to fetch weather data';
                this.showError(error);
            }

        } catch (error) {
            this.hideLoading();
            this.showError('Network error: ' + error.message);
        }
    }

    displayWeather(currentWeather, forecast) {
        // Update current weather
        this.currentTemp.textContent = currentWeather.temperature;
        this.currentLocation.textContent = currentWeather.location;
        this.currentDescription.textContent = currentWeather.description;
        this.feelsLike.textContent = currentWeather.feels_like;
        this.humidity.textContent = currentWeather.humidity;
        this.windSpeed.textContent = currentWeather.wind_speed;
        this.pressure.textContent = currentWeather.pressure;
        this.visibility.textContent = currentWeather.visibility;
        
        // Format timestamp
        const timestamp = new Date(currentWeather.timestamp);
        this.timestamp.textContent = timestamp.toLocaleString();

        // Update forecast
        this.displayForecast(forecast.forecast);

        // Show weather section
        this.showWeather();
    }

    displayForecast(forecastData) {
        this.forecastContainer.innerHTML = '';

        // Group forecast by day and show daily averages
        const dailyForecasts = this.groupForecastByDay(forecastData);

        dailyForecasts.forEach(day => {
            const forecastItem = document.createElement('div');
            forecastItem.className = 'forecast-item';
            
            const date = new Date(day.date);
            const dayName = date.toLocaleDateString('en-US', { weekday: 'short' });
            const monthDay = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });

            forecastItem.innerHTML = `
                <div class="forecast-date">${dayName}, ${monthDay}</div>
                <div class="forecast-temp">${day.avgTemp}</div>
                <div class="forecast-desc">${day.mostCommonDesc}</div>
            `;

            this.forecastContainer.appendChild(forecastItem);
        });
    }

    groupForecastByDay(forecastData) {
        const dailyGroups = {};

        forecastData.forEach(forecast => {
            const date = new Date(forecast.timestamp);
            const dayKey = date.toDateString();
            
            if (!dailyGroups[dayKey]) {
                dailyGroups[dayKey] = {
                    date: date,
                    temps: [],
                    descriptions: []
                };
            }

            // Extract temperature value
            const tempValue = parseFloat(forecast.temperature.replace('°C', ''));
            dailyGroups[dayKey].temps.push(tempValue);
            dailyGroups[dayKey].descriptions.push(forecast.description);
        });

        return Object.values(dailyGroups).map(day => {
            const avgTemp = Math.round(day.temps.reduce((a, b) => a + b, 0) / day.temps.length);
            const mostCommonDesc = this.getMostCommon(day.descriptions);
            
            return {
                date: day.date,
                avgTemp: `${avgTemp}°C`,
                mostCommonDesc: mostCommonDesc
            };
        });
    }

    getMostCommon(array) {
        const counts = {};
        let maxCount = 0;
        let mostCommon = array[0];

        array.forEach(item => {
            counts[item] = (counts[item] || 0) + 1;
            if (counts[item] > maxCount) {
                maxCount = counts[item];
                mostCommon = item;
            }
        });

        return mostCommon;
    }

    showLoading() {
        this.loadingSection.style.display = 'block';
    }

    hideLoading() {
        this.loadingSection.style.display = 'none';
    }

    showWeather() {
        this.weatherSection.style.display = 'block';
    }

    hideWeather() {
        this.weatherSection.style.display = 'none';
    }

    showError(message) {
        this.errorMessage.textContent = message;
        this.errorSection.style.display = 'block';
    }

    hideError() {
        this.errorSection.style.display = 'none';
    }

    // Utility method to format weather descriptions
    formatWeatherDescription(description) {
        return description.charAt(0).toUpperCase() + description.slice(1);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new WeatherApp();
});

// Add some nice animations and interactions
document.addEventListener('DOMContentLoaded', () => {
    // Add smooth scrolling
    const smoothScroll = (target) => {
        target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    };

    // Add keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            // Hide error messages on escape
            const errorSection = document.getElementById('errorSection');
            if (errorSection.style.display === 'block') {
                errorSection.style.display = 'none';
            }
        }
    });

    // Add loading states for buttons
    const searchBtn = document.getElementById('searchBtn');
    const originalBtnText = searchBtn.innerHTML;

    // Override the searchWeather method to show loading state
    const originalSearchWeather = WeatherApp.prototype.searchWeather;
    WeatherApp.prototype.searchWeather = async function() {
        searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
        searchBtn.disabled = true;
        
        try {
            await originalSearchWeather.call(this);
        } finally {
            searchBtn.innerHTML = originalBtnText;
            searchBtn.disabled = false;
        }
    };
});
