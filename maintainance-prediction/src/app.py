# from flask import Flask, request, jsonify
# import pandas as pd
# import xgboost as xgb
# import numpy as np
# import joblib
# from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

# def preprocess(data):
#     features=['Type','Air temperature','Process temperature','Rotational speed','Torque','Tool wear']
#     x = data[features].copy()
    
#     scaler=joblib.load('model/standardScaler.joblib')
#     numerical_cols=['Air temperature','Process temperature','Rotational speed','Torque','Tool wear']
#     x[numerical_cols]=scaler.transform(x[numerical_cols])
    
#     encoder = joblib.load('model/oneHotEncoder.joblib')
#     oh_cols = encoder.transform(x[['Type']])
#     oh_cols_df = pd.DataFrame(oh_cols, columns=encoder.get_feature_names_out(['Type']))
#     oh_cols_df.index = x.index 
    
#     encoded_x = x.drop('Type', axis=1)
#     encoded_x = pd.concat([encoded_x, oh_cols_df], axis=1)
    
#     return encoded_x


# app = Flask(__name__)

# model_path = 'model/xgboost_model.joblib'
# model = joblib.load(model_path)

# @app.route('/predict', methods=['GET', 'POST'])
# def predict():
#     if request.method == 'POST':
#         data = request.get_json()
#         required_fields = ['UDI', 'Product ID', 'Type', 'Air temperature' ,'Process temperature' ,'Rotational speed' ,'Torque' ,'Tool wear']
#         if not all(field in data for field in required_fields):
#             return jsonify({'error': 'Missing fields in input data'}), 400

#         input_data = pd.DataFrame([data])

#         input_data = preprocess(input_data)
            

#         predictions = model.predict(input_data)
#         # failure_probability = int(predictions[0][0])
#         # maintenance_needed = bool(failure_probability == 1) 

#         # return jsonify({
#         #     'failure_probability': failure_probability,
#         #     'maintenance_needed': maintenance_needed
#         # })


#     else: 
#         return "This endpoint is for predictions via POST requests."

    

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify, render_template
import pandas as pd
import xgboost as xgb
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from flask_cors import CORS



# Preprocess function to transform input data
def preprocess(data):
    features = ['Type', 'Air temperature', 'Process temperature', 'Rotational speed', 'Torque', 'Tool wear']
    x = data[features].copy()
    numerical_cols = ['Air temperature', 'Process temperature', 'Rotational speed', 'Torque', 'Tool wear']
    for col in numerical_cols:
        x[col] = x[col].astype('float64')
    # Load scaler and encoder models
    scaler = joblib.load('./model/standardScaler.joblib')
    x[numerical_cols] = scaler.transform(x[numerical_cols])
    
    encoder = joblib.load('./model/oneHotEncoder.joblib')
    oh_cols = encoder.transform(x[['Type']])
    oh_cols_df = pd.DataFrame(oh_cols, columns=encoder.get_feature_names_out(['Type']))
    oh_cols_df.index = x.index 
    
    # Drop 'Type' and concatenate encoded columns
    encoded_x = x.drop('Type', axis=1)
    encoded_x = pd.concat([encoded_x, oh_cols_df], axis=1)
    
    return encoded_x

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the predictive model
model_path = './model/xgboost_model.joblib'
model = joblib.load(model_path)

# Route to serve the HTML form
# @app.route('/')
# def index():
#     return render_template('dashboard.html')

# Route to handle form submission and prediction
@app.route('/api/predict', methods=['POST'])
def predict():
    
    data = request.json
    app.logger.info("Received data: %s", data)  # Log received data for debugging
    
    if not data:
        return jsonify({"error": "No data received"}), 400
    required_fields = ['Type', 'Air temperature', 'Process temperature', 'Rotational speed', 'Torque', 'Tool wear']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields in input data'}), 400

    # Convert form data to DataFrame
    input_data = pd.DataFrame([data])
    app.logger.info(input_data.dtypes)
    # Preprocess data
    processed_data = preprocess(input_data)
    
    # Make predictions
    predictions = model.predict(processed_data)

    # Return predictions to display in the HTML
    return jsonify({
        "machineFailure": predictions[0][0],
        "TWF": predictions[0][1],
        "HDF": predictions[0][2],
        "PWF": predictions[0][3],
        "OSF": predictions[0][4],
        "RNF": predictions[0][5]
    })

if __name__ == '__main__':
    app.run(port=5000)
