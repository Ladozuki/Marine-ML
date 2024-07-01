import joblib
import pandas as pd

#Load the trained model
model = joblib.load('...')


def predict(data):
    df = pd.DataFrame(data)
    predictions = model.predict(df)
    return predictions