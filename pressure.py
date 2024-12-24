import streamlit as st
import requests
import pandas as pd
from io import StringIO
st.set_page_config(layout="wide")

from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=10 * 60 * 1000, key="temp_refresh")

# Function to load CSS from a file
def load_css(file_path):
    try:
        with open(file_path) as f:
            return f.read()
    except FileNotFoundError:
        st.warning(f"CSS file '{file_path}' not found. Skipping CSS loading.")
        return ""

# Fetch the CSV data
url = "https://data.weather.gov.hk/weatherAPI/hko_data/regional-weather/latest_1min_pressure_uc.csv"
response = requests.get(url)

# Clean the response text by removing BOM if it exists
cleaned_text = response.content.decode('utf-8-sig')

# Read the cleaned CSV content
csv_data = StringIO(cleaned_text)
df = pd.read_csv(csv_data, encoding='utf-8')

# Keep only relevant columns for display
df_filtered = df[['自動氣象站', '平均海平面氣壓（百帕斯卡）']]

# Convert the pressure data to numeric (in case there are non-numeric values)
df_filtered['平均海平面氣壓（百帕斯卡）'] = pd.to_numeric(df_filtered['平均海平面氣壓（百帕斯卡）'], errors='coerce')

# Load external CSS file
css = load_css("Python.css")  # Make sure the path is correct
if css:
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Add custom CSS for the box styling
st.markdown("""
    <style>
   .station-box {
        background-color: #ADD8E6;
        border: 2px solid #ccc;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); 
        border-left: 9px solid #ff4b4b;
        padding: 5px 15px 25px 15px;  /* Adjusted padding: top, right, bottom, left */
        margin: 10px;
        text-align: left;
        width: 100%;
        height: 100px;
    }
    .station-box .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: bold;
        font-size: 28px;  /* Adjust this size for the station name */
        margin-bottom: 10px;
    }
    .station-box strong {
        margin-bottom: 0px; /* Reduce the bottom margin */
        display: block;
                    font-weight: bold;

        line-height: 1.2; /* Adjust the space between name and pressure */
        font-size: 30px;  /* Adjust this size for pressure */
    }
    </style>
""", unsafe_allow_html=True)

# Display the data in rows of 5 boxes per row
st.title("Atmospheric Pressure Data from Automatic Weather Stations")

# Create a layout with 5 columns per row
cols_per_row = 3
stations = df_filtered.iterrows()

# Iterate through the data in chunks of 5 for each row
for i in range(0, len(df_filtered), cols_per_row):
    cols = st.columns(cols_per_row)  # Create 5 columns
    for j, (index, row) in enumerate(df_filtered.iloc[i:i+cols_per_row].iterrows()):
        with cols[j]:  # Access the j-th column
            station_name = row['自動氣象站']
            pressure = row['平均海平面氣壓（百帕斯卡）']

            # Display each station's data in a fixed box
            st.markdown(f"""
                <div class="station-box">
                    <div class="header">{station_name}</div>
                   <strong>{pressure} hPa</strong>
                </div>
            """, unsafe_allow_html=True)
