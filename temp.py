import streamlit as st
from streamlit_option_menu import option_menu
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
    .station-box {
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
    .station-box .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: bold;
        font-size: 24px;  /* Station name size */
        margin-bottom: 5px;
    }
    .station-box strong {
        margin-bottom: 0px;
        display: block;
        line-height: 1.2;
        font-size: 30px;  /* Temperature value size */
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Function to determine border color based on temperature
def get_border_color(temp_value):
    if temp_value <= 7:
        return '#800080'  # Purple (嚴寒)
    elif 8 <= temp_value <= 12:
        return '#00008B'  # Dark Blue (寒冷)
    elif 13 <= temp_value <= 17:
        return '#90EE90'  # Light Green (清涼)
    elif 20 <= temp_value <= 25:
        return '#F28C28'  # Orange
    elif 26 <= temp_value <= 31:
        return '#ff4b4b'  # Red
    else:
        return '#cccccc'  # Default grey for other temperatures


# Fetch data from the Hong Kong Weather API
api_url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=tc"
st.title('溫度')

try:
    response = requests.get(api_url)
    response.raise_for_status()  # Raise an error for bad responses
    data = response.json()
    
    # Extract temperature data (place, value, unit)
    temperature_data = data['temperature']['data']

    # Check if we have temperature data before processing
    if temperature_data:
        num_columns = 4  # Number of columns to display
        # Loop through the temperature data and display each location's temperature
        for i in range(0, len(temperature_data), num_columns):
            cols = st.columns(num_columns)  # Create columns for each row

            # Loop through the temperature data and display each location's temperature
            for j, temp in enumerate(temperature_data[i:i+num_columns]):
                place = temp['place']
                value = temp['value']
                unit = temp['unit']  # Should be "C" for Celsius

                # Get border color based on temperature
                border_color = get_border_color(value)

                # Display each location's temperature with custom box styling
                with cols[j]:
                    st.markdown(f'''
                        <div class="station-box" style="border-left: 9px solid {border_color};">
                            <div class="header">
                                <strong>{place}</strong>
                            </div>
                            <strong>{value}°{unit}</strong>
                        </div>
                    ''', unsafe_allow_html=True)

    else:
        st.error("沒有可用的溫度數據")  # Message if there are no temperature values

except requests.exceptions.RequestException as e:
    st.error(f"獲取數據時出錯：{e}")  # Catch any request-related errors
except Exception as e:
    st.error(f"獲取數據時出錯：{e}")  # Catch all other errors
