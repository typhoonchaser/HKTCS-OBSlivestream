import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh
st.set_page_config(layout="wide")

st_autorefresh(interval=10 * 60 * 1000, key="temp_refresh")

# Function to load CSS from a file
def load_css(file_path):
    with open(file_path) as f:
        return f.read()

# Load the external CSS file
css = load_css("Python.css")  # Make sure the path is correct
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Add custom CSS for the box styling
st.markdown("""
    <style>
    .rainstation-box {
        background-color: #ADD8E6;
        border: 2px solid #ccc;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        padding: 15px 15px 25px 15px;  /* Adjusted padding */
        margin: 5px;
        text-align: left;
        width: 100%;
        height: 100px;
        font-weight: bold;
    }
    .rainstation-box .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: bold;
        font-size: 24px;  /* Station name size */
        margin-bottom: 5px;
    }
    .rainstation-box strong {
        margin-bottom: 0px;
        display: block;
        line-height: 1.2;
        font-size: 30px;  /* Rainfall value size */
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Function to determine border color based on rainfall
def get_rainfall_border_color(rainfall_value):
    rainfall_value = float(rainfall_value)  # Ensure value is a float
    if rainfall_value < 30:
        return '#00008B'  # Dark blue
    elif 30 <= rainfall_value < 50:
        return '#FFBF00'  # Amber
    elif 50 <= rainfall_value < 70:
        return '#FF4B4B'  # Red
    else:
        return '#000000'  # Black for > 70mm

# Fetch rainfall data from the Hong Kong Weather API
api_url = "https://data.weather.gov.hk/weatherAPI/opendata/hourlyRainfall.php?lang=tc"
st.title('降雨')

try:
    response = requests.get(api_url)
    response.raise_for_status()  # Raise an error for bad responses
    data = response.json()

    # Extract rainfall data (place, value, unit)
    rainfall_data = data['hourlyRainfall']  # Get the rainfall data

    # Check if we have rainfall data before processing
    if rainfall_data:
        num_columns = 4  # Number of columns to display
        st.title("香港實時降雨量")  # Title for Rainfall data

        # Loop through the rainfall data and display each location's rainfall
        for i in range(0, len(rainfall_data), num_columns):
            cols = st.columns(num_columns)  # Create columns for each row

            for j, rain in enumerate(rainfall_data[i:i + num_columns]):
                place = rain['automaticWeatherStation']  # Station name
                value = rain['value']  # Rainfall value
                unit = rain['unit']  # Unit (e.g., mm)

                

                # Skip non-numeric values
                try:
                    # Convert to float and get border color
                    border_color = get_rainfall_border_color(value)
                except ValueError:
                    st.write(f"Invalid rainfall value at {place}: {value}")
                    continue  # Skip this entry if conversion fails

                # Display each location's rainfall with custom box styling
                with cols[j]:
                    st.markdown(f'''
                        <div class="rainstation-box" style="border-left: 9px solid {border_color};">
                            <div class="header">
                                <strong>{place}</strong>
                            </div>
                            <strong>{value} {unit}</strong>
                        </div>
                    ''', unsafe_allow_html=True)

    else:
        st.error("沒有可用的降雨量數據")  # Message if there are no rainfall values

except requests.exceptions.RequestException as e:
    st.error(f"獲取數據時出錯1：{e}")  # Catch any request-related errors
except Exception as e:
    st.error(f"獲取數據時出錯：{e}")  # Catch all other errors
