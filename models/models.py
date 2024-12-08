import os
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Set BASE_DIR to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR, "data", "processed", "df_gen.csv")

# Debug print
print(f"Looking for file at: {data_path}")

# Check if file exists
if not os.path.exists(data_path):
    raise FileNotFoundError(f"File not found: {data_path}")

# Load the CSV
df = pd.read_csv(data_path)

# Debug print to inspect the data structure
print(f"Columns in the dataset:\n{df.columns}")

# Handle missing values for relevant columns
columns_to_fill = ['Capacity/Bollard Pull', 'Duration (days)']
df[columns_to_fill] = df[columns_to_fill].fillna(value=0)

# One-hot encode categorical variables
df = pd.get_dummies(df, columns=['Vessel Type', 'Cargo Type/Use Case'], drop_first=True)

# Scale numerical features
scaler = MinMaxScaler()
numerical_features = ['Duration (days)', 'Capacity/Bollard Pull']
df[numerical_features] = scaler.fit_transform(df[numerical_features])

# Drop irrelevant or multicollinear columns
columns_to_drop = ['Charter Date', 'Size Category', 'Vessel breadth (m)']  # Adjust based on your data
df = df.drop(columns=columns_to_drop, axis=1, errors='ignore')

# Separate features and target
X = df.drop(columns='Charter Price ($/day)', errors='ignore')
y = df['Charter Price ($/day)']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the models
models = {
    "LinearRegression": LinearRegression(),
    "RandomForest": RandomForestRegressor(),
    "SVR": SVR()
}

# Train models
for model_name, model in models.items():
    model.fit(X_train, y_train)

# Evaluate models
def evaluate_models(models, X_test, y_test):
    results = []
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

results = evaluate_models(models, X_test, y_test)

# Example: Hyperparameter tuning for RandomForest using GridSearchCV
# Uncomment and modify as needed
# param_grid = {
#     'n_estimators': [50, 100, 200],
#     'max_depth': [None, 10, 20],
#     'min_samples_split': [2, 5, 10]
# }
# grid_search = GridSearchCV(RandomForestRegressor(), param_grid, cv=3, scoring='neg_mean_squared_error', verbose=1)
# grid_search.fit(X_train, y_train)
# print(f"Best Parameters for RandomForest: {grid_search.best_params_}")
# print(f"Best Score: {grid_search.best_score_}")
