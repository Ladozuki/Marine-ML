import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


df = pd.read_csv("/Users/ladipo/Desktop/Charter/charter_pricepred/data/processed/data_generation.csv")

#turning categorical variables numerical for ease of modelling
df = pd.get_dummies(df, columns=['Vessel Type', 'Cargo Type'])

# Ensure all categorical variables are properly encoded
# If there are still categorical variables left unencoded, handle them here

# Scale numerical features
scaler = MinMaxScaler()
df[['Duration (days)', 'Fuel Cost ($/liter)']] = scaler.fit_transform(df[['Duration (days)', 'Fuel Cost ($/liter)']])

# Drop columns to avoid multicollinearity (if needed)
columns_to_drop = ['Vessel Type_Bulk Carrier', 'Cargo Type_Grain', 'Vessel breadth (m)', 'Charter Date', 'Size Category']
df = df.drop(columns=columns_to_drop, axis=1)

# Identify the X and y variables
X = df.drop(columns='Charter Price ($/day)')
y = df['Charter Price ($/day)']

#error message due to NaN values
#Fill with 0's
columns_to_fill = ['Container Capacity (TEU)', 'Cargo Capacity (DWT)', 'LPG Capacity (m)', 'LNG Capacity (m)']
df[columns_to_fill] = df[columns_to_fill].fillna(value= 0)

print(df.isna().sum())

# # Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train.fillna(value = 0, inplace = True)
y_train.fillna(value = 0, inplace = True)
X_test.fillna(value = 0, inplace = True)
y_test.fillna(value = 0, inplace = True)

# # Initialize the model
LR = LinearRegression()
RF = RandomForestRegressor()
SVR = SVR()

# Train the models
LR.fit(X_train, y_train)
RF.fit(X_train, y_train)
SVR.fit(X_train, y_train)

# Make predictions
y_pred_Lr = LR.predict(X_test)
y_pred_rf = RF.predict(X_test)
y_pred_svr = SVR.predict(X_test)



# Calculate evaluation metrics
mae = mean_absolute_error(y_test, y_pred_Lr)
mse = mean_squared_error(y_test, y_pred_Lr)
r2 = r2_score(y_test, y_pred_Lr)

print(f'Mean Absolute Error: {mae}')
print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

from sklearn.model_selection import GridSearchCV
