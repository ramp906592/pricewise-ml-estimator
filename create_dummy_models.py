import joblib
import numpy as np
import os
from sklearn.linear_model import LinearRegression

# Ensure models directory exists
if not os.path.exists("models"):
    os.makedirs("models")

print("Generating dummy models...")

# ===============================
# 1. CAR MODEL
# ===============================
# Features: [year, present_price, kms, fuel, seller, transmission, owner]
# Shape: (1, 7)
print("Creating Car Model...")
X_car = np.array([
    [2015, 5.0, 50000, 0, 0, 0, 0],
    [2020, 10.0, 10000, 1, 1, 1, 0]
])
y_car = np.array([3.5, 8.5]) # Dummy target values

car_model = LinearRegression()
car_model.fit(X_car, y_car)

joblib.dump(car_model, "models/car_model.pkl")

# ===============================
# 2. HOUSE MODEL
# ===============================
# Columns: total_sqft, bath, bhk, locations...
print("Creating House Model...")
house_columns = ['total_sqft', 'bath', 'bhk', 'location_Whitefield', 'location_Sarjapur Road', 'location_Electronic City']
# Input vector must match length of columns
# Let's verify input vector logic in app.py
# X[cols.index("total_sqft")] = ...
# So we just need a model trained on len(house_columns) features.

X_house = np.zeros((5, len(house_columns)))
# Fill with some random data
X_house[:, 0] = [1000, 1200, 1500, 2000, 2500] # sqft
X_house[:, 1] = [2, 2, 3, 3, 4] # bath
X_house[:, 2] = [2, 2, 3, 3, 4] # bhk
X_house[:, 3] = [1, 0, 0, 0, 0] # Whitefield
y_house = np.array([40.0, 50.0, 75.0, 100.0, 150.0])

house_model = LinearRegression()
house_model.fit(X_house, y_house)

joblib.dump(house_model, "models/bangalore_house_model.pkl")
joblib.dump(house_columns, "models/house_columns.pkl")

# ===============================
# 3. LAPTOP MODEL
# ===============================
# Features: Ram, Weight, Inches
print("Creating Laptop Model...")
laptop_columns = ['Ram', 'Weight', 'Inches']

X_laptop = np.array([
    [8, 1.5, 15.6],
    [16, 2.0, 15.6],
    [4, 1.2, 13.3],
    [32, 2.5, 17.3]
])
y_laptop = np.array([800.0, 1200.0, 400.0, 2000.0]) # Price in EUR

laptop_model = LinearRegression()
laptop_model.fit(X_laptop, y_laptop)

joblib.dump(laptop_model, "models/laptop_price_model.pkl")
joblib.dump(laptop_columns, "models/laptop_columns.pkl")

print("Done! Dummy models saved to 'models/'")
