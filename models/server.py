from flask import Flask, request, jsonify
import joblib
import pandas as pd
import json
from models.predict import calculate_voyage_insights

# Initialize Flask app
app = Flask(__name__)

# Load the model
model = joblib.load('model.joblib')

# Load configuration from external file
with open('vessel_config.json', 'r') as f:
    config = json.load(f)

@app.route('/predict', methods=['POST'])
def predict_route():
    data = request.json
    df = pd.DataFrame(data)
    predictions = model.predict(df)
    return jsonify(predictions.tolist())

@app.route('/voyage-insights', methods=['POST'])
def voyage_insights():
    data = request.json
    route = data["route"]
    vessel_type = data["vessel_type"]
    fuel_price = data["fuel_price"]
    base_rate = data["base_rate"]
    seasonality = data.get("seasonality", 1.0)
    congestion = data.get("congestion", 1.0)
    weather = data.get("weather", 1.0)

    insights = calculate_voyage_insights(route, vessel_type, fuel_price, base_rate, seasonality, congestion, weather)
    return jsonify(insights)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
