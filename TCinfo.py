import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")

st_autorefresh(interval=10 * 60 * 1000, key="temp_refresh")
# Fetch the 9-day weather forecast data
url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=tc"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()

    # Extract relevant information (e.g., week, wind, temperature, humidity)
    forecasts = data['weatherForecast']
    forecast_list = []
    
    for forecast in forecasts:
        week = forecast['week']  # Only keep the week (weekday)
        wind = forecast['forecastWind']  # Wind forecast
        temp_min = forecast['forecastMintemp']['value']
        temp_max = forecast['forecastMaxtemp']['value']
        rh_min = forecast['forecastMinrh']['value']
        rh_max = forecast['forecastMaxrh']['value']

        # Create a dictionary to store forecast data
        forecast_list.append({
            'week': week,
            'wind': wind,
            'temp_range': f"{temp_min}°C - {temp_max}°C",
            'rh_range': f"{rh_min}% - {rh_max}%"
        })

# Apply custom CSS for box layout with specific alignment and larger text size
st.markdown("""
    <style>
    .forecast-box {
        background-color: #e6f2ff;
        border: 1px solid #0099ff;
        border-radius: 10px;
        border-left: 7px solid #ff4b4b;
        padding: 15px;
        margin: 10px 0;
        width: 100%;
        display: flex;
        justify-content: space-between;  
        align-items: center;  
    }
    .forecast-box strong {
        font-size: 30px;  /* Increased size for week name */
        color: #003366;
        font-weight: bold;
        flex-basis: 100px;  
    }
    .forecast-box .info {
        font-size: 28px;  /* Increased size for info */
        font-weight: bold;
    }
    .wind-info {
        flex: 1;  
        font-size: 30px;  /* Increased size for info */
        font-weight: bold;


    }
    .temp-info {
        text-align: center;  
        flex: 1;  
        font-size: 30px;  /* Increased size for info */
        font-weight: bold;


    }
    .rh-info {
        text-align: right;  
        flex: 1;  
        font-size: 30px;  /* Increased size for info */
        font-weight: bold;


    }
    </style>
""", unsafe_allow_html=True)

# Display forecast data for each day in a long rectangular box with aligned elements
st.title("9-Day Weather Forecast")

for forecast in forecast_list:
    st.markdown(f"""
        <div class="forecast-box">
            <strong>{forecast['week']}</strong>
            <span class="wind-info">🌬️ 風力: {forecast['wind']}</span>
            <span class="temp-info">🌡️ 溫度: {forecast['temp_range']}</span>
            <span class="rh-info">💧 濕度: {forecast['rh_range']}</span>
        </div>
    """, unsafe_allow_html=True)

