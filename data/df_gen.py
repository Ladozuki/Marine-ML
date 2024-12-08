import json 
import pandas as pd
import os 
import random 
from datetime import date, timedelta

#Load config
with open("vessel_config.json", "r") as f:
    config = json.load(f)

def random_value(range_tuple):
    return random.randint(*range_tuple)

def random_date(start_date, end_date):

    delta = end_date -start_date
    random_days = random.randint(0, delta.days)
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days = random_days)

#Define base Dir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Output path for processed data
data_path = os.path.join(BASE_DIR, "data", "processed", "df_gen.csv")

os.makedirs(os.path.dirname(data_path), exist_ok = True)

def generate_data(samples, start_date, end_date):
    """Generate Random Vessel data"""
    data = {"Charter Date": [random_date(start_date, end_date) for _ in range(samples)],
            "Vessel Type": [random.choice(list(config['vessel_types'].keys())) for _ in range(samples)]
            }
    #Add Charter Price and Duration
    data['Charter Price ($/day)'] = [random_value(config['vessel_types'][v]['charter_price_range']) for v in data['Vessel Type']]
    data['Duration (days)'] = [random.randint(45, 450) for _ in range (samples)]

    #Add other features dynamically based on vessel type
    return pd.DataFrame

#Generate and save to csv
df = generate_data(samples = 2500, start_date=date(2021, 1, 1), end_date = date(2024, 2, 1))
df.to_csv(data_path, index = False)
    
print(f"Data Generate and Saved to {data_path}")