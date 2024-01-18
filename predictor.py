import joblib

def wind_speed_score(wind_speed):
    return (wind_speed / 20) * 10  # Assuming maximum wind speed is 20 m/s

# Load the wind model
loaded_wind_model = joblib.load('wind_speed_prediction_model.joblib')

# Function to predict wind energy suitability
def predict_wind_suitability(wind_speed):
    wind_score = wind_speed_score(wind_speed)
    prediction = loaded_wind_model.predict([[wind_score]])
    return prediction[0]

# Load the solar model
loaded_solar_model = joblib.load('solar_score_prediction_model.joblib')

# Scoring logic for solar data
# Adjust the column names and scoring logic as per your dataset and requirements
def solar_score(sunlightTime, dayLength, GHI):
    sunlight_score = 0
    if dayLength > 0:
        ratio = sunlightTime / dayLength
        sunlight_score = ratio * 10  # Half weight to sunlight time

    # Scoring based on GHI - assuming GHI > 300 is good for solar energy
    ghi_score = (GHI / 300) * 10 if GHI <= 300 else 10

    return sunlight_score + ghi_score

# Function to predict solar energy suitability
def predict_solar_suitability(sunlightTime, dayLength, GHI):
    solar_score_value = solar_score(sunlightTime, dayLength, GHI)
    # Provide all three features expected by the solar model
    prediction = loaded_solar_model.predict([[sunlightTime, dayLength, GHI]])
    return prediction[0]

# Example Usage
wind_speed = float(input("Enter wind speed at the location (m/s): "))
solar_sunlightTime = float(input("Enter sunlight time at the location (hours): "))
solar_dayLength = float(input("Enter day length at the location (hours): "))
solar_GHI = float(input("Enter Global Horizontal Irradiance (GHI) at the location: "))

wind_suitability = predict_wind_suitability(wind_speed)
solar_suitability = predict_solar_suitability(solar_sunlightTime, solar_dayLength, solar_GHI)

print(f"Wind Energy Suitability: {wind_suitability:.2f}/10")
print(f"Solar Energy Suitability: {solar_suitability:.2f}/10")
