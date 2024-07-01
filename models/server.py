from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

#Loading the model using joblib

model =joblib.load('model.joblib')

@app.route('/predict', methods = ['POST'])

def predict_route():
    data = request.json
    df = pd.DataFrame(data)
    predictions = model.predict(df)
    return jsonify(predictions.tolist())

#Alternate method of writing the above 
# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json()  # Get the JSON data
#     features = np.array([data['vessel_size'], data['vessel_age'], data['distance'], data['fuel_cost'], data['vessel_type'], data['cargo_type']])
#     prediction = model.predict([features])  # Make prediction
#     return jsonify({'prediction': prediction[0]})  # Return prediction as JSON


if __name__ == '__main__':
    app.run(debug = True)
