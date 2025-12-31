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

# Comprehensive list of Bangalore locations
locations = [
    'Electronic City', 'Sarjapur Road', 'Whitefield', 'Koramangala', 'Indiranagar', 
    'Marathahalli', 'HSR Layout', 'Hebbal', 'Yelahanka', 'Bellandur', 
    'Bannerghatta Road', 'Jayanagar', 'JP Nagar', 'Kanakapura Road', 'Thanisandra',
    'Harlur', 'Hennur Road', 'Raja Rajeshwari Nagar', 'Uttarahalli', 'Banashankari',
    'Malleshwaram', 'Basavanagudi', 'BTM Layout', 'KR Puram', 'Ramamurthy Nagar',
    'Vijayanagar', 'Rajaji Nagar', 'Frazer Town', 'Cooke Town', 'Ulsoor',
    'Richmond Town', 'Benson Town', 'Kalyan Nagar', 'Kammanahalli', 'Sahakara Nagar',
    'Vidyaranyapura', 'Hoodi', 'Varthur', 'Gunjur', 'Panathur',
    'Begur Road', 'Bommanahalli', 'Hosa Road', 'Kasavanahalli', 'Kudlu Gate',
    'Singasandra', 'Chandapura', 'Attibele', 'Anekal', 'Jigani',
    'Brookefield', 'Kundalahalli', 'Mahadevapura', 'Doddanekundi', 'Domlur',
    'Old Airport Road', 'New Tippasandra', 'CV Raman Nagar', 'Kaggadasapura',
    'Nagavarapalya', 'GM Palya', 'Thubarahalli', 'Munnekollal', 'Seegehalli',
    'Kadugodi', 'Channasandra', 'Hegde Nagar', 'Jakkur', 'Kodigehalli',
    'Yeshwanthpur', 'Peenya', 'Dasarahalli', 'Nagasandra', 'Jalahalli',
    'Mathikere', 'Sanjay Nagar', 'RT Nagar', 'Ganganagar', 'Sadashivnagar',
    'Vasanth Nagar', 'Shivajinagar', 'Cunningham Road', 'Lavelle Road', 'Shanthi Nagar',
    'Wilson Garden', 'Adugodi', 'Ejipura', 'Vivek Nagar', 'Austin Town',
    'Cox Town', 'Richards Town', 'Lingarajapuram', 'Banaswadi', 'Horamavu',
    'T C Palya', 'K R Puram', 'Devasandra', 'Battarahalli', 'Medahalli',
    'Avalahalli', 'Bidarahalli', 'Hoskote', 'Budigere Cross', 'Devanahalli',
    'Bagalur', 'Yelahanka New Town', 'Vidyaranyapura', 'Doddaballapur Road',
    'Tumkur Road', 'Magadi Road', 'Mysore Road', 'Kengeri', 'Rajarajeshwari Nagar'
]

# Create location columns (one-hot encoded style)
location_cols = [f"location_{loc}" for loc in locations]
house_columns = ['total_sqft', 'bath', 'bhk'] + location_cols

# Input vector must match length of columns
# So we just need a model trained on len(house_columns) features.

num_samples = 5
num_features = len(house_columns)
X_house = np.zeros((num_samples, num_features))

# Fill with some random data for basic features
X_house[:, 0] = [1000, 1200, 1500, 2000, 2500] # sqft
X_house[:, 1] = [2, 2, 3, 3, 4] # bath
X_house[:, 2] = [2, 2, 3, 3, 4] # bhk

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

print(f"Done! Dummy models saved to 'models/' with {len(locations)} locations.")
