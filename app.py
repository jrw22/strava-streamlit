import streamlit as st
import pandas as pd
import numpy as np
import json

from get_data import ApiConnection

st.title("Strava Dashboard")

# Read credentials from JSON file
def load_credentials():
    with open('credentials.json', 'r') as file:
        return json.load(file)

credentials = load_credentials()
client_id = credentials['client_id']
client_secret = credentials['client_secret']
redirect_uri = credentials['redirect_uri']

# Create an instance of ConnectToApi
strava_connector = ApiConnection(client_id, client_secret, redirect_uri)

# Generate the authorization URL
if 'auth_url' not in st.session_state:
    st.session_state.auth_url = strava_connector.get_authorisation_url(scope="read_all,activity:read_all")

# Display the authorisation URL
button_html = f"<a href='{st.session_state.auth_url}' target='_blank'><button style='color: white; background-color: blue; padding: 10px 20px; border-radius: 5px; border: none;'>Authorize with Strava</button></a>"
st.markdown(button_html, unsafe_allow_html=True)

# Ask user to enter the code
authorisation_code = st.text_input("Copy the code from the url and paste here:")

if authorisation_code:
    # Exchange the code for a token
    strava_connector.exchange_code_for_token(authorisation_code)
    st.session_state['authorised'] = True

# Get athlete profile
if st.session_state.get('authorised'):
    profile = strava_connector.get_athlete_profile()
    st.write("Connection successful")
    st.write(profile)  # Display some details from the profile



