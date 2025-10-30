import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")
st_autorefresh(interval=10 * 60 * 1000, key="temp_refresh")

# Fetch the 9-day weather forecast data
url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=tc"
response = requests.get(url)
forecast_list = []

if response.status_code == 200:
    data = response.json()
    forecasts = data['weatherForecast']
    
    for forecast in forecasts:
        week = forecast['week']
        forecast_date = forecast['forecastDate']
        wind = forecast['forecastWind']
        temp_min = forecast['forecastMintemp']['value']
        temp_max = forecast['forecastMaxtemp']['value']
        rh_min = forecast['forecastMinrh']['value']
        rh_max = forecast['forecastMaxrh']['value']
        
        # Extract wind level and add descriptors with color
        wind_display = wind
        wind_highlighted = ""
        if wind:
            # Extract numbers from wind string
            import re
            numbers = re.findall(r'\d+', wind)
            if numbers:
                wind_level = int(numbers[-1])  # Get the last number (max level)
                
                # Find the part with the high wind level
                parts = re.split(r'[，。]', wind)
                highlight_part = ""
                for part in parts:
                    if re.search(r'\d+', part):
                        part_numbers = re.findall(r'\d+', part)
                        if part_numbers and int(part_numbers[-1]) >= 6:
                            highlight_part = part
                            break
                
                if wind_level in [6, 7]:
                    descriptor = " (強風)"
                    color = "#FFD700"  # Yellow
                    if highlight_part:
                        wind_highlighted = wind.replace(highlight_part, f'<span style="color: {color}">{highlight_part}{descriptor}</span>')
                    else:
                        wind_highlighted = f'{wind} <span style="color: {color}">{descriptor}</span>'
                elif wind_level in [8, 9]:
                    descriptor = " (烈風)"
                    color = "#FF8C00"  # Orange
                    if highlight_part:
                        wind_highlighted = wind.replace(highlight_part, f'<span style="color: {color}">{highlight_part}{descriptor}</span>')
                    else:
                        wind_highlighted = f'{wind} <span style="color: {color}">{descriptor}</span>'
                elif wind_level in [10, 11]:
                    descriptor = " (暴風)"
                    color = "#FF0000"  # Red
                    if highlight_part:
                        wind_highlighted = wind.replace(highlight_part, f'<span style="color: {color}">{highlight_part}{descriptor}</span>')
                    else:
                        wind_highlighted = f'{wind} <span style="color: {color}">{descriptor}</span>'
                elif wind_level == 12:
                    descriptor = " (颶風)"
                    color = "#800080"  # Purple
                    if highlight_part:
                        wind_highlighted = wind.replace(highlight_part, f'<span style="color: {color}">{highlight_part}{descriptor}</span>')
                    else:
                        wind_highlighted = f'{wind} <span style="color: {color}">{descriptor}</span>'
                else:
                    wind_highlighted = wind
            else:
                wind_highlighted = wind
        else:
            wind_highlighted = wind
        
        forecast_list.append({
            'week': week,
            'date': forecast_date,
            'wind': wind_highlighted if wind_highlighted else wind,
            'temp_range': f"{temp_min}°C - {temp_max}°C",
            'rh_range': f"{rh_min}% - {rh_max}%"
        })

st.title("🌦️ 9-Day Weather Forecast")

# Use Streamlit columns instead of CSS grid
for i in range(0, len(forecast_list), 3):
    cols = st.columns(3)
    for j, col in enumerate(cols):
        if i + j < len(forecast_list):
            forecast = forecast_list[i + j]
            with col:
                st.markdown(f"""
                    <div style="
                        background-color: #e6f2ff;
                        border: 2px solid #0099ff;
                        border-radius: 15px;
                        border-left: 8px solid #ff4b4b;
                        padding: 20px;
                        box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
                        text-align: center;
                        height: 100%;
                        min-height: 250px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                    ">
                        <div style="font-size: 32px; color: #003366; font-weight: bold; margin-bottom: 5px;">
                            {forecast['week']}
                        </div>
                        <div style="font-size: 18px; color: #666; margin-bottom: 15px;">
                            {forecast['date']}
                        </div>
                        <div style="font-size: 35px; font-weight: bold; line-height: 1.8;">
                            <div>💨 風力: {forecast['wind']}</div>
                            <div>🌡️ 溫度: {forecast['temp_range']}</div>
                            <div>💧 濕度: {forecast['rh_range']}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
