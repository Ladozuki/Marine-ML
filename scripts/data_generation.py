import pandas as pd
import random
from datetime import date, timedelta

#functions to generate data
def charter_prices(vessel_type):
    prices = {
        "Container Ship": (10000, 35000),
        "Tanker": (15000, 50000),
        "LNG Carrier": (25000, 60000),
        "Bulk Carrier": (10000, 30000),
        "LPG Carrier": (20000, 43000)
    }
    result = random.randint(*prices[vessel_type])
    return result
    
def random_capacity(vessel_type):
    capacities = {
        "Container Ship": (3000, 14000),
        "Tanker": (50000, 400000),
        "LNG Carrier": (100000, 150000),
        "Bulk Carrier": (10000, 200000),
        "LPG Carrier": (5000, 80000)
    }
    choice = random.randint(*capacities[vessel_type])
    return choice 

def random_category(vessel_type):
    categories = {
        "Container Ship": ["Feeder Ships", "Feedermax Ships", "Panamax Ships", "Post-Panamax Ships", "New Panamax (Neo-Panamax) Ships"],
        "Tanker": ["Handysize", "Panamax", "Aframax", "Suezmax", "VLCC", "ULCC", "MR", "LR1", "LR2"],
        "LNG Carrier": ["Typical LNG Carrier"],
        "Bulk Carrier": ["Handysize", "Handymax/Supramax", "Panamax", "Capesize"],
        "LPG Carrier": ["Typical LPG Carrier"]
    }
    categories = random.choice(categories[vessel_type])
    return categories

def random_cargo_type(vessel_type):
    cargo_types = {"Container Ship": ["Electronics", "Apparel", "Machinery", "Chemicals", "Consumer Goods"],
    "Tanker": ["Refined Products", "Crude Oil"],
    "LNG Carrier": ["Liquified Natural Gas"],
    "Bulk Carrier": ["Iron Ore", "Coal", "Grain"],
    "LPG Carrier": ["Liquified Petroleum Gas"]}
    return random.choice(cargo_types[vessel_type])

def random_dimensions(vessel_type):
    dimensions = {
    "Container Ship": (random.randint(70, 400), random.randint(14, 60)),
    "Tanker": (random.randint(70, 350), random.randint(20, 65)),
    "LNG Carrier": (random.randint(200, 300), random.randint(40, 50)),
    "Bulk Carrier": (random.randint(100, 300), random.randint(20, 60)),
    "LPG Carrier": (random.randint(100, 230), random.randint(14, 40))}
    return dimensions[vessel_type]

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))
 
def random_duration():
    return random.randint(45, 450)

def random_fuel_costs():
    return round(random.uniform(0.5, 0.8), 2)

def random_fees():
    return random.randint(1000, 4500), random.randint(28000, 45000), random.randint(400, 800)


samples = 2500
start_date = date(2021, 1, 1)
end_date = date(2024, 2, 1)

ship_type = ['Container Ship', 'Tanker', 'LNG Carrier', 'Bulk Carrier',
             'LPG Carrier']

data = {"Charter Date": [random_date(start_date, end_date) for _ in range(samples)],
        "Vessel Type": [random.choice(ship_type) for i in range(samples)]
 }



data['Charter Price ($/day)'] = [charter_prices(v) for v in data['Vessel Type']]
data['Duration (days)'] = [random_duration() for i in range(samples)]
# data['Route'] = 
# data['Departure Route'] 
# data['Destination Port']
data['LNG Capacity (m)'] = [random_capacity('LNG Carrier') if v == 'LNG Carrier' else None for v in data['Vessel Type']]
data['LPG Capacity (m)'] = [random_capacity('LPG Carrier') if v == 'LPG Carrier' else None for v in data['Vessel Type']]
data['Cargo Capacity (DWT)'] = [random_capacity(v) if v in ['Tanker', 'Bulk Carrier'] else None for v in data['Vessel Type']]
data['Container Capacity (TEU)'] = [random_capacity(v) if v == 'Container Ship' else None for v in data['Vessel Type']]
data['Size Category'] = [random_category(v) for v in data['Vessel Type']]
data['Cargo Type'] = [random_cargo_type(v) for v in data["Vessel Type"]]
data['Vessel Length (m)'], data['Vessel breadth (m)'] = zip(*[random_dimensions(v) for v in data["Vessel Type"]])
data['Fuel Cost ($/liter)'] = [random_fuel_costs() for i in range(samples)]

df = pd.DataFrame(data)


file = '/Users/ladipo/Desktop/Charter/charter_pricepred/data/processed/data_generation.csv'
df.to_csv(file, index =False)

print(df)