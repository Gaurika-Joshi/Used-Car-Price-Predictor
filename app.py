import streamlit as st
import pickle
import pandas as pd
import datetime

# 1. Loading models
with open('car_price_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('model_columns.pkl', 'rb') as file:
    model_columns = pickle.load(file)

# The Website Design
st.title("🚗 Used Car Price Predictor")
st.write("Enter the car's details below to instantly calculate its fair market value.")

# Car Brand Dropdown
brand = st.selectbox(
    "Car Brand", 
    options=[
        ("Maruti Suzuki", 20), ("Hyundai", 10), ("Honda", 8), 
        ("Tata", 25), ("Mahindra", 19), ("Toyota", 27), 
        ("Kia", 15), ("Renault", 23), ("Ford", 7), ("Volkswagen", 28)
    ], 
    format_func=lambda x: x[0]
)

# Year Dropdown
year = st.selectbox("Manufacturing Year", options=list(range(2026, 1999, -1)))

km = st.number_input("Kilometers Driven", min_value=0, value=20000, step=5000)
fuel = st.selectbox("Fuel Type", options=[("Petrol", 4), ("Diesel", 3), ("CNG", 0), ("LPG", 1), ("Electric", 2)], format_func=lambda x: x[0])
transmission = st.selectbox("Transmission", options=[("Manual", 0), ("Automatic", 1)], format_func=lambda x: x[0])
owner = st.selectbox("Ownership", options=[("1st Owner", 1), ("2nd Owner", 2), ("3rd Owner", 3), ("4th Owner", 4)], format_func=lambda x: x[0])

# Predict Button
if st.button("Predict Price"):
    # Calculate age BTS for the ML model
    current_year = datetime.datetime.now().year
    calculated_age = current_year - year
    
    input_data = pd.DataFrame([[brand[1], km, fuel[1], transmission[1], owner[1], calculated_age]], columns=model_columns)
    
    # Get prediction
    prediction = model.predict(input_data)[0]
    
    # Display the result
    st.success(f"Estimated Selling Price: ₹{prediction:,.0f}")
