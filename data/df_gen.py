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
        "Vessel Type": [],
        "Route ID": []
    }

    charter_prices = []
    durations = []
    cargo_types = []
    capacities = []
    distances = []
    port_fees = []
    daily_consumption = []
    average_speeds = []  # New list to store average speeds

    for _ in range(samples):
        # Select Route ID and Vessel Type
        route_id = random.choice(list(config["routes"].keys()))
        route_config = config["routes"][route_id]
        vessel_type = random.choice(route_config["frequent_vessels"])

        # Append to data once per sample
        data["Vessel Type"].append(vessel_type)
        data["Route ID"].append(route_id)

        # Vessel-specific configuration
        vessel_config = config["vessel_types"][vessel_type]
        charter_prices.append(random_value(vessel_config.get("charter_price_range", (5000, 10000))))
        capacities.append(random_value(vessel_config.get("capacity_range", (1000, 5000))))
        cargo_types.append(random.choice(vessel_config.get("cargo_types", ["Unknown"])))
        daily_consumption.append(vessel_config.get("daily_consumption", 0))
        average_speeds.append(vessel_config.get("average_speed_knots", 0))  # Add average_speed_knots

        # Route-specific configuration
        distances.append(route_config["distance_nm"])
        port_fees.append(route_config["port_fees"])

        # Voyage duration calculation
        duration = route_config["distance_nm"] / vessel_config["average_speed_knots"] / 24
        durations.append(duration)

    # Add generated data to the dictionary
    data["Charter Price ($/day)"] = charter_prices
    data["Duration (days)"] = durations
    data["Cargo Type/Use Case"] = cargo_types
    data["Capacity/Bollard Pull"] = capacities
    data["daily_consumption"] = daily_consumption
    data["Distance (nm)"] = distances
    data["Port Fees ($)"] = port_fees
    data["Average Speed (knots)"] = average_speeds  # Add the new column

    # Debug: Ensure all arrays have the same length
    print({k: len(v) for k, v in data.items()})
    lengths = {k: len(v) for k, v in data.items()}
    assert len(set(lengths.values())) == 1, f"Array lengths are inconsistent: {lengths}"

    return pd.DataFrame(data)



# Generate data and save to CSV
df = generate_data(samples=2500, start_date=date(2021, 1, 1), end_date=date(2024, 2, 1))
df.to_csv(data_path, index=False)

print(f"Data generated successfully!\nFile saved to: {data_path}\nSample data:\n")
print(df.head())
