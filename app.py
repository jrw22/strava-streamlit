import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from get_data import ApiConnection, AthleteProfile, CredentialsLoader

from get_plots import StravaPlots

st.title("Strava Dashboard")

creds = CredentialsLoader()
credentials = creds.load_credentials(file='credentials.json')
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

if st.session_state.get('authorised'):

    ### Get athlete profile ###

    st.session_state.athlete = AthleteProfile(strava_connector)
    st.session_state.profile = st.session_state.athlete.get_athlete_profile()
    st.write("Connection successful")
    st.write(st.session_state.profile)  # Display some details from the profile

    st.session_state.activities = st.session_state.athlete.fetch_all_activities()
    st.dataframe(st.session_state.activities)

    ### Create plots ###
    df = pd.DataFrame(st.session_state.activities)
    st.session_state.plots = StravaPlots(df)


    # Monthly training time
    monthly_training_time = st.session_state.plots.monthly_training_time()
    st.pyplot(monthly_training_time)

    # Monthly training time grouped
    fig, ax = st.session_state.plots.monthly_training_time_grouped()
    st.pyplot(fig)

    





