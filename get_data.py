import requests
from urllib.parse import urlencode, urlparse, parse_qs
import streamlit as st
import json
import pandas as pd

class CredentialsLoader:

    def load_credentials(self, file):
        with open(file, 'r') as file:
            return json.load(file)
        
class ApiConnection:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.authorization_url = "https://www.strava.com/oauth/authorize"
        self.token_url = "https://www.strava.com/oauth/token"
        self.access_token = None

    def get_authorisation_url(self, scope="read"):
        """
        Generate the authorisation URL for the user to grant access.
        """
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": scope,
            "approval_prompt": "auto"
        }
        url = f"{self.authorization_url}?{urlencode(params)}"
        return url

    def exchange_code_for_token(self, code):
        """
        Exchange the authorisation code for an access token.
        """
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code"
        }
        response = requests.post(self.token_url, data=payload)
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
        else:
            raise Exception("Failed to get access token")

    def make_api_call(self, endpoint, params=None):
        """
        Make an API call using the obtained access token.
        """
        if self.access_token is None:
            raise Exception("Access token is not available")

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(f"https://www.strava.com/api/v3/{endpoint}", headers=headers, params=params)
        return response.json()
    
    
    
class AthleteProfile:
    def __init__(self, api_connection):
        self.api_connection = api_connection

    def get_athlete_profile(self):
        return self.api_connection.make_api_call("athlete")
    
    def fetch_all_activities(self):
        activities = []
        page = 1
        while True:
            response = self.api_connection.make_api_call('athlete/activities', params={'per_page': 200, 'page': page})
            if not response:
                break  # No more activities to fetch
            activities.extend(response)
            page += 1
        return activities
