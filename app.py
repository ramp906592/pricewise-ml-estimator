from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# ===============================
# LOAD MODELS
# ===============================
def load_assets():
    assets = {}
    
    # HOUSE MODEL
    if os.path.exists("models/bangalore_house_model.pkl"):
        assets["house"] = {
            "model": joblib.load("models/bangalore_house_model.pkl"),
            "columns": joblib.load("models/house_columns.pkl")
        }
    
    # LAPTOP MODEL
    if os.path.exists("models/laptop_price_model.pkl"):
        assets["laptop"] = {
            "model": joblib.load("models/laptop_price_model.pkl"),
            "columns": joblib.load("models/laptop_columns.pkl")
        }
    
    # CAR MODEL
    if os.path.exists("models/car_model.pkl"):
        assets["car"] = joblib.load("models/car_model.pkl")
    
    return assets

# Load models at startup
print("Loading ML models...")
assets = load_assets()
print(f"Loaded models: {list(assets.keys())}")
# ===============================
# ROUTES
# ===============================

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

# ===============================
# API ENDPOINTS
# ===============================

@app.route('/api/predict/car', methods=['POST'])
def predict_car():
    """Car price prediction endpoint"""
    try:
        data = request.json
        
        # Extract features
        year = int(data['year'])
        present_price = float(data['present_price'])
        kms = int(data['kms'])
        fuel = int(data['fuel'])  # 0: Petrol, 1: Diesel, 2: CNG
        seller = int(data['seller'])  # 0: Dealer, 1: Individual
        transmission = int(data['transmission'])  # 0: Manual, 1: Automatic
        owner = int(data['owner'])
        
        # Create feature array
        X = np.array([[year, present_price, kms, fuel, seller, transmission, owner]])
        
        # Predict
        price = assets["car"].predict(X)[0]
        
        return jsonify({
            'success': True,
            'price': round(price, 2),
            'currency': 'Lakhs'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
@app.route('/api/predict/house', methods=['POST'])
def predict_house():
    """House price prediction endpoint"""
    try:
        data = request.json
        house = assets["house"]
        cols = house["columns"]
        
        # Extract features
        total_sqft = float(data['total_sqft'])
        bath = int(data['bath'])
        bhk = int(data['bhk'])
        location = data['location']
        
        # Create feature array
        X = np.zeros(len(cols))
        X[cols.index("total_sqft")] = total_sqft
        X[cols.index("bath")] = bath
        X[cols.index("bhk")] = bhk
        
        # Set location
        loc_col = f"location_{location}"
        if loc_col in cols:
            X[cols.index(loc_col)] = 1
        
        # Predict
        price = house["model"].predict([X])[0]
        
        return jsonify({
            'success': True,
            'price': round(price, 2),
            'currency': 'Lakhs'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/predict/laptop', methods=['POST'])
def predict_laptop():
    """Laptop price prediction endpoint"""
    try:
        data = request.json
        laptop = assets["laptop"]
        cols = laptop["columns"]
        
        # Extract features
        ram = int(data['ram'])
        weight = float(data['weight'])
        inches = float(data['inches'])
        
        # Create feature array
        X = np.zeros(len(cols))
        if "Ram" in cols:
            X[cols.index("Ram")] = ram
        if "Weight" in cols:
            X[cols.index("Weight")] = weight
        if "Inches" in cols:
            X[cols.index("Inches")] = inches
        
        # Predict
        price_eur = laptop["model"].predict([X])[0]
        price_inr = price_eur * 90
        
        return jsonify({
            'success': True,
            'price': round(price_inr, 0),
            'price_eur': round(price_eur, 0),
            'currency': '₹'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Get available house locations"""
    try:
        house = assets["house"]
        cols = house["columns"]
        locations = sorted([c.replace("location_", "") for c in cols if c.startswith("location_")])
        
        return jsonify({
            'success': True,
            'locations': locations
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ===============================
# RUN SERVER
# ===============================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
