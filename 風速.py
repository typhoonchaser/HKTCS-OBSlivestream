import streamlit as st
import requests
import pandas as pd
from io import StringIO
from streamlit_autorefresh import st_autorefresh

# Set the page layout to use full width
st.set_page_config(layout="wide")
st_autorefresh(interval=10 * 60 * 1000, key="temp_refresh")

# Function to load CSS from a file
def load_css(file_path):
    try:
        with open(file_path) as f:
            return f.read()
    except FileNotFoundError:
        st.warning(f"CSS file '{file_path}' not found. Skipping CSS loading.")
        return ""

# Load external CSS file
css = load_css("Python.css")  # Make sure the path is correct
if css:
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Fetch the CSV data
url = "https://data.weather.gov.hk/weatherAPI/hko_data/regional-weather/latest_10min_wind_uc.csv"
response = requests.get(url)

# Clean the response text by removing BOM if it exists
cleaned_text = response.content.decode('utf-8-sig')

# Read the cleaned CSV content
csv_data = StringIO(cleaned_text)
df = pd.read_csv(csv_data, encoding='utf-8')

# Keep only relevant columns
df_filtered = df[['自動氣象站', '十分鐘平均風速（公里/小時）', '十分鐘平均風向（方位點）', '日期時間']]

# Convert the wind speed to numeric
df_filtered['十分鐘平均風速（公里/小時）'] = pd.to_numeric(df_filtered['十分鐘平均風速（公里/小時）'], errors='coerce')

# Convert the date-time to correct format
df_filtered['日期時間'] = pd.to_datetime(df_filtered['日期時間'], format='%Y%m%d%H%M')

# Function to convert wind direction to arrows
def get_wind_arrow(direction):
    arrow_map = {
        '北': '↓', '東北': '↙', '東': '←', '東南': '↖', '南': '↑', '西南': '↗', '西': '→', '西北': '↘', '無風': '-'
    }
    return arrow_map.get(direction, '')

# Add arrow to wind direction
df_filtered['風向箭頭'] = df_filtered['十分鐘平均風向（方位點）'].apply(get_wind_arrow)

# Function to assign color based on wind speed
def get_border_color(wind_speed):
    if wind_speed >= 118:
        return '#800080'  # Purple for Hurricane
    elif wind_speed >= 87:
        return '#8B0000'  # Dark Red for Storm
    elif wind_speed >= 63:
        return '#FF0000'  # Red for Gale
    elif wind_speed >= 41:
        return '#FFA500'  # Orange for Strong Wind
    else:
        return '#ADD8E6'  # Default color for lighter winds

# Display the data in rows of 5 boxes per row
st.title("Wind Speed and Direction from Automatic Weather Stations")

# Create a layout with 5 columns per row
cols_per_row = 5

# Iterate through the data in chunks of 5 for each row
for i in range(0, len(df_filtered), cols_per_row):
    cols = st.columns([1, 1, 1, 1, 1])  # Create 5 equal-width columns
    for j, (index, row) in enumerate(df_filtered.iloc[i:i+cols_per_row].iterrows()):
        with cols[j]:  # Access the j-th column
            station_name = row['自動氣象站']
            wind_speed = row['十分鐘平均風速（公里/小時）']
            wind_arrow = row['風向箭頭']
            border_color = get_border_color(wind_speed)

            # Display each station's data in a fixed box with only wind arrows and dynamic border color
            st.markdown(f"""
                <div class="station-box" style="border-left: 9px solid {border_color};">
                    <div class="header">
                        <span>{station_name}</span>
                        <span>{wind_arrow}</span>
                    </div>
                    <strong>{wind_speed} km/h</strong>
                </div>
            """, unsafe_allow_html=True)

# CSS for station box styling
st.markdown("""
    <style>
    .station-box {
        background-color: #ADD8E6;
        border: 2px solid #ccc;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); 
        padding: 10px 15px 25px 15px;
        margin: 10px;
        text-align: left;
        width: 100%;
        height: 100px;
        font-weight: bold;
    }
    .station-box .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: bold;
        font-size: 24px;
        margin-bottom: 10px;
    }
    .station-box strong {
        margin-bottom: 0px;
        display: block;
        line-height: 1.2;
        font-size: 30px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)
