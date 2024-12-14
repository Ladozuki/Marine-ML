import joblib
import pandas as pd
import json

# Load the trained model
model = joblib.load('model.joblib')

# Load configuration from external file
with open('vessel_config.json', 'r') as f:
    config = json.load(f)

# Calculation Functions
def calculate_fuel_consumption(distance_nm, speed_knots, consumption_rate):
    voyage_days = distance_nm / (speed_knots * 24)
    return voyage_days * consumption_rate

def calculate_voyage_cost(distance_nm, speed_knots, consumption_rate, fuel_price, port_fees, canal_fees):
    fuel_required = calculate_fuel_consumption(distance_nm, speed_knots, consumption_rate)
    fuel_cost = fuel_required * fuel_price
    return fuel_cost + port_fees + canal_fees

def adjust_freight_rate(base_rate, seasonality=1.0, congestion=1.0, weather=1.0):
    return base_rate * seasonality * congestion * weather

def calculate_voyage_insights(route, vessel_type, fuel_price, base_rate, seasonality=1.0, congestion=1.0, weather=1.0):
    distance_nm = config["routes"][route]["distance_nm"]
    port_fees = config["routes"][route]["port_fees"]
    canal_fees = config["routes"][route]["canal_fees"]

    consumption_rate = config["vessel_types"][vessel_type]["daily_consumption"]
    speed_knots = config["vessel_types"][vessel_type]["average_speed_knots"]

    fuel_required = calculate_fuel_consumption(distance_nm, speed_knots, consumption_rate)
    voyage_cost = calculate_voyage_cost(distance_nm, speed_knots, consumption_rate, fuel_price, port_fees, canal_fees)
    adjusted_rate = adjust_freight_rate(base_rate, seasonality, congestion, weather)

    return {
        "fuel_required_tons": fuel_required,
        "voyage_cost": voyage_cost,
        "adjusted_freight_rate": adjusted_rate
    }

# Prediction Function
def predict(data):
    df = pd.DataFrame(data)
    predictions = model.predict(df)
    return predictions
