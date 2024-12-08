import json
import pandas as pd
import os
import random
from datetime import date, timedelta

# Load config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, "../config/vessel_config.json")

# Debug print to verify the file path
print(f"Config file path: {config_path}")  # Step 1

# Load the JSON file with error handling
try:
    with open(config_path, "r") as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {config_path}")  # Handles missing file
    raise  # Re-raise the error after logging
except json.JSONDecodeError as e:
    print(f"Error: JSON file at {config_path} is invalid. Details: {e}")  # Handles invalid JSON
    raise

def random_value(range_tuple):
    """Generate a random value within the given range."""
    return random.uniform(*range_tuple) if isinstance(range_tuple[0], float) else random.randint(*range_tuple)

def random_date(start_date, end_date):
    """Generate a random date between start_date and end_date."""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# Output path for processed data
data_path = os.path.join(BASE_DIR, "processed", "df_gen.csv")
os.makedirs(os.path.dirname(data_path), exist_ok=True)

def generate_data(samples, start_date, end_date):
    """Generate random vessel data based on the configuration."""
    # Base data
    data = {
        "Charter Date": [random_date(start_date, end_date) for _ in range(samples)],
        "Vessel Type": [random.choice(list(config['vessel_types'].keys())) for _ in range(samples)]
    }
    
    # Add features based on vessel type
    charter_prices = []
    durations = []
    cargo_types = []
    capacities = []

    for v in data["Vessel Type"]:
        vessel_config = config["vessel_types"][v]
        
        # Charter Price or Freight Rate
        if "charter_price_range" in vessel_config:
            charter_prices.append(random_value(vessel_config["charter_price_range"]))
        elif "freight_rate_range" in vessel_config:
            charter_prices.append(random_value(vessel_config["freight_rate_range"]))

        # Duration (general assumption for charters)
        durations.append(random.randint(45, 450))

        # Cargo Type or Use Case
        if "cargo_types" in vessel_config:
            cargo_types.append(random.choice(vessel_config["cargo_types"]))
        elif "use_cases" in vessel_config:
            cargo_types.append(random.choice(vessel_config["use_cases"]))

        # Capacity or Bollard Pull
        if "capacity_range" in vessel_config:
            capacities.append(random_value(vessel_config["capacity_range"]))
        elif "bollard_pull_range" in vessel_config:
            capacities.append(random_value(vessel_config["bollard_pull_range"]))

    # Add generated data to the dictionary
    data["Charter Price ($/day)"] = charter_prices
    data["Duration (days)"] = durations
    data["Cargo Type/Use Case"] = cargo_types
    data["Capacity/Bollard Pull"] = capacities
    
    # Convert to DataFrame
    return pd.DataFrame(data)

# Generate data and save to CSV
df = generate_data(samples=2500, start_date=date(2021, 1, 1), end_date=date(2024, 2, 1))
df.to_csv(data_path, index=False)

print(f"Data generated successfully!\nFile saved to: {data_path}\nSample data:\n")
print(df.head())
