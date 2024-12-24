import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh
st.set_page_config(layout="wide")

# Title of the page
st.title('特別天氣提示')

st_autorefresh(interval=10 * 60 * 1000, key="temp_refresh")

# Fetch advisory text from the Hong Kong Weather API
api_url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=swt&lang=tc"

try:
    response = requests.get(api_url)
    response.raise_for_status()  # Raise an error for bad responses
    data = response.json()

    # Extract advisory text from the "desc" field
    advisory_text = data['swt'][0]['desc'] if 'swt' in data else None

    # Check if there's any advisory text available
    if advisory_text:
        # Use the box_style to display the advisory text
        box_style = """
        <div style="
            background-color: #f0f0f0; 
            padding: 20px; 
            border-radius: 10px; 
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); 
            border-left: 4px solid #ff4b4b;
            font-weight: bold
        ">
            <p style="font-size: 16px;"><strong>{}</strong></p>

        </div>
        """.format(advisory_text)

        # Display the advisory text in a box with the custom style
        st.markdown(box_style, unsafe_allow_html=True)
    else:
        st.error("目前沒有特別天氣提示")  # Message if there are no advisories

except requests.exceptions.RequestException as e:
    st.error(f"獲取數據時出錯：{e}")  # Catch any request-related errors
except Exception as e:
    st.error(f"獲取數據時出錯：{e}")  # Catch all other errors
