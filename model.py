import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import streamlit as st

@st.cache_data
def train_model(data):
    # Features and target
    features = ['GDP per capita', 'headcount_ratio_upper_mid_income_povline', 'year']
    target = 'Life Expectancy (IHME)'
    
    # Drop NaNs
    model_data = data[features + [target]].dropna()
    
    X = model_data[features]
    y = model_data[target]
    
    # Train model
    model = RandomForestRegressor(random_state=42)
    model.fit(X, y)
    
    return model, features

def predict_life_expectancy(model, features, gdp, headcount, year):
    input_data = pd.DataFrame([[gdp, headcount, year]], columns=features)
    prediction = model.predict(input_data)[0]
    return prediction