import os
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "")


# Ensure all categorical variables are properly encoded

# Load data
df = pd.read_csv(data_path)

#Handle missing values
columns_to_fill = ['Container Capacity (TEU)', 'Cargo Capacity (DWT)', 'LPG Capacity (m)', 'LNG Capacity (m)']
df[columns_to_fill] = df[columns_to_fill].fillna(value= 0)

#turning categorical variables numerical for ease of modelling
#One-hot encode categorical variables
df = pd.get_dummies(df, columns=['Vessel Type', 'Cargo Type'])

# Scale numerical features
scaler = MinMaxScaler()
df[['Duration (days)', 'Fuel Cost ($/liter)']] = scaler.fit_transform(df[['Duration (days)', 'Fuel Cost ($/liter)']])

# Drop columns to avoid multicollinearity (if needed)
columns_to_drop = ['Vessel Type_Bulk Carrier', 'Cargo Type_Grain', 'Vessel breadth (m)', 'Charter Date', 'Size Category']
df = df.drop(columns=columns_to_drop, axis=1)

#Seperate features and target
X = df.drop(columns='Charter Price ($/day)')
y = df['Charter Price ($/day)']

# # Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Initialize the model
LR = LinearRegression()
RF = RandomForestRegressor()
SVR = SVR()

model = { "LineaRegression":LR,
          "RandomForest": RF,
          "SVR": SVR}

def evaluate_models(models, X_test, y_test):
    results = []
    #iterate over each model
    for model_name, model in models.items():
        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        results.append({
            "Model": model_name,
            "MAE": mae,
            "MSE": mse,
            "R2": r2
        })

       # Print metrics
        print(f"{model_name}:")
        print(f"  Mean Absolute Error: {mae}")
        print(f"  Mean Squared Error: {mse}")
        print(f"  R^2 Score: {r2}")
        print("-" * 30)
    return results

#Training
for model_name, model in model.items():
    model.fit(X_train, y_train)

results = evaluate_models(model, X_test, y_test)




# Example: Hyperparameter tuning for RandomForest using GridSearchCV
#Create a function that will evaluate multuple regeression models on the test set
#prints out evaluation metrics

# param_grid = {
#     'n_estimators': [50, 100, 200],
#     'max_depth': [None, 10, 20],
#     'min_samples_split': [2, 5, 10]
# }
# grid_search = GridSearchCV(RandomForestRegressor(), param_grid, cv=3, scoring='neg_mean_squared_error', verbose=1)
# grid_search.fit(X_train, y_train)

# print(f"Best Parameters for RandomForest: {grid_search.best_params_}")
# print(f"Best Score: {grid_search.best_score_}")




