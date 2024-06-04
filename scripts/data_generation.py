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
        "Chemical Tanker": (15000, 25000),
        "LPG Carrier": (20000, 43000),
        "Product Tanker": (12000, 30000)
    }
    result = random.randint(*prices[vessel_type])
    return result
    
def random_capacity(vessel_type):
    capacities = {
        "Container Ship": (3000, 14000),
        "Tanker": (50000, 4000000),
        "LNG Carrier": (125000, 150000),
        "Bulk Carrier": (10000, 200000),
        "Chemical Tanker": (10000, 40000),
        "LPG Carrier": (5000, 80000),
        "Product Tanker": (25000, 160000)
    }
    choice = random.randint(*capacities[vessel_type])
    return choice 

def random_category(vessel_type):
    categories = {
        "Container Ship": ["Feeder Ships", "Feedermax Ships", "Panamax Ships", "Post-Panamax Ships", "New Panamax (Neo-Panamax) Ships", "Ultra Large Container Ships (ULCS)"],
        "Tanker": ["Handysize", "Panamax", "Aframax", "Suezmax", "VLCC", "ULCC"],
        "LNG Carrier": ["Typical LNG Carrier"],
        "Bulk Carrier": ["Handysize", "Handymax/Supramax", "Panamax", "Capesize"],
        "Chemical Tanker": ["IMO Type 3"],
        "LPG Carrier": ["Typical LPG Carrier"],
        "Product Tanker": ["MR", "LR1", "LR2"]
    }
    categories = random.choice(categories[vessel_type])
    return categories

def random_dimensions(vessel_type):
    dimensions = {
        "Container Ship": (random.randint(70, 400), random.randint(14, 60)),
    "Tanker": (random.randint(70, 350), random.randint(20, 65)),
    "LNG Carrier": (random.randint(200, 300), random.randint(40, 50)),
    "Bulk Carrier": (random.randint(100, 300), random.randint(20, 60)),
    "Chemical Tanker": (random.randint(100, 250), random.randint(14, 40)),
    "LPG Carrier": (random.randint(100, 230), random.randint(14, 40)),
    "Product Tanker": (random.randint(125, 280), random.randint(25, 50))}
    return dimensions[vessel_type]

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))
 
def random_duration():
    return random.randint(45, 450)

def random_fuel_costs():
    return random.uniform(0.5, 0.8)

def random_fees():
    return random.randint(1000, 4500), random.randint(28000, 45000), random.randint(400, 800)


samples = 2500
start_date = date(2021, 1, 1)
end_date = date(2024, 2, 1)

ship_type = ['Container Ship', 'Tanker', 'LNG Carrier', 'Bulk Carrier', 'Chemical Tanker',
             'LPG Carrier', 'Product Tanker']
goods = ["Electronics", "Crude Oil", "Apparel", "Iron Ore", "Coal", "Machinery", 
         "Refined Products", "Chemicals", "LNG", "LPG", "Grain", "Consumer Goods"]

data = {"Charter Date": [random_date(start_date, end_date) for _ in range(samples)],
        "Vessel Type": [random.choice(ship_type) for i in range(samples)]
 }

data['Cargo Capacity (DWT)'] = [random_capacity(v) if v != 'Container Ship' else None for v in data['Vessel Type']]
data['Container Capacity (TEU)'] = [random_capacity(v) if v == 'Container Ship' else None for v in data['Vessel Type']]
data['Vessel Length (m)'], data['Vessel breadth (m)'] = zip(*[random_dimensions(v) for v in data["Vessel Type"]])
data['Charter Price ($/day)'] = [charter_prices(v) for v in data['Vessel Type']]
data['Duration (days)'] = [random_duration for i in range(samples)]
# data['Route'] = 
# data['Departure Route'] 
# data['Destination Port']
data['Fuel Cost ($/liter)'] = [random_fuel_costs() for i in range(samples)]
data['LNG Capacity (m)'] = [random_capacity('LNG Carrier') if v == 'LNG Carrier' else None for v in data['Vessel Type']]
data['LPG Capacity (m)'] = [random_capacity('LPG Carrier') if v == 'LPG Carrier' else None for v in data['Vessel Type']]
data['Size Category'] = [random_category(v) for v in data['Vessel Type']]
data['Cargo Type'] = [random.choice(goods) for i in range(samples)]

df = pd.DataFrame(data)

print(df) 