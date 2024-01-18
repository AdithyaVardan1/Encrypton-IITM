import streamlit as st
import pandas as pd
import joblib

# Function to calculate wind speed score
def wind_speed_score(wind_speed):
    return (wind_speed / 20) * 10  # Assuming maximum wind speed is 20 m/s

# Function to predict wind energy suitability
def predict_wind_suitability(loaded_wind_model, wind_speed):
    wind_score = wind_speed_score(wind_speed)
    prediction = loaded_wind_model.predict([[wind_score]])
    return prediction[0]

# Scoring logic for solar data
def solar_score(sunlightTime, dayLength, GHI):
    sunlight_score = 0
    if dayLength > 0:
        ratio = sunlightTime / dayLength
        sunlight_score = ratio * 10  # Half weight to sunlight time

    # Scoring based on GHI - assuming GHI > 300 is good for solar energy
    ghi_score = (GHI / 300) * 10 if GHI <= 300 else 10

    return sunlight_score + ghi_score

# Function to predict solar energy suitability
def predict_solar_suitability(loaded_solar_model, sunlightTime, dayLength, GHI):
    solar_score_value = solar_score(sunlightTime, dayLength, GHI)
    prediction = loaded_solar_model.predict([[sunlightTime, dayLength, GHI]])
    return prediction[0]

# Load the models
loaded_wind_model = joblib.load('wind_speed_prediction_model.joblib')
loaded_solar_model = joblib.load('solar_score_prediction_model.joblib')

# Streamlit interface
st.title('Wind and Solar Energy Suitability Prediction')

st.header('Wind Energy Prediction')
wind_speed = st.number_input("Enter wind speed at the location (m/s):", min_value=0.0, max_value=100.0, step=0.1)
if st.button('Predict Wind Energy Suitability'):
    wind_suitability = predict_wind_suitability(loaded_wind_model, wind_speed)
    st.write(f"Wind Energy Suitability: {wind_suitability:.2f}/10")

st.header('Solar Energy Prediction')
solar_sunlightTime = st.number_input("Enter sunlight time at the location (hours):", min_value=0.0, max_value=24.0, step=0.1)
solar_dayLength = st.number_input("Enter day length at the location (hours):", min_value=0.0, max_value=24.0, step=0.1)
solar_GHI = st.number_input("Enter Global Horizontal Irradiance (GHI) at the location:", min_value=0.0, max_value=1000.0, step=1.0)
if st.button('Predict Solar Energy Suitability'):
    solar_suitability = predict_solar_suitability(loaded_solar_model, solar_sunlightTime, solar_dayLength, solar_GHI)
    st.write(f"Solar Energy Suitability: {solar_suitability:.2f}/10")
