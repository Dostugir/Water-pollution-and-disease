from flask import Flask, render_template, request, jsonify
import pickle
import os
import numpy as np
from werkzeug.exceptions import BadRequest
import logging
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load the model
try:
    model = pickle.load(open('rf_model.pkl', 'rb'))
    logger.info("Model loaded successfully")
except FileNotFoundError:
    logger.error("Model file not found. Please make sure rf_model.pkl exists in the current directory.")
    exit(1)
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    exit(1)

def validate_input(data):
    """Validate input parameters against expected ranges"""
    try:
        # Convert all values to float
        ph = float(data.get('ph', 0))
        turbidity = float(data.get('turbidity', 0))
        nitrate = float(data.get('nitrate', 0))
        lead = float(data.get('lead', 0))
        oxygen = float(data.get('oxygen', 0))

        # Validate ranges
        if not (0 <= ph <= 14):
            raise ValueError("pH must be between 0 and 14")
        if turbidity < 0:
            raise ValueError("Turbidity cannot be negative")
        if nitrate < 0:
            raise ValueError("Nitrate level cannot be negative")
        if lead < 0:
            raise ValueError("Lead concentration cannot be negative")
        if oxygen < 0:
            raise ValueError("Dissolved oxygen cannot be negative")

        return [ph, turbidity, nitrate, lead, oxygen]
    except ValueError as e:
        raise ValueError(f"Invalid input: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing input: {str(e)}")

@app.route('/')
def home():
    """Render the main page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    try:
        # Validate and process input
        features = validate_input(request.form)
        final_features = [np.array(features)]
        
        # Make prediction
        prediction = model.predict(final_features)
        probability = model.predict_proba(final_features)[0]
        
        # Format output
        output = prediction[0]
        confidence = round(max(probability) * 100, 2)
        
        # Determine water quality based on prediction
        if output == 1:
            result = 'Safe for consumption'
            details = 'The water meets quality standards based on the provided parameters.'
        else:
            result = 'Not safe for consumption'
            details = 'The water does not meet quality standards and may pose health risks.'
        
        # Create detailed response with recommendations
        response = {
            'status': 'success',
            'prediction': result,
            'confidence': f"{confidence}%",
            'details': {
                'ph': features[0],
                'turbidity': features[1],
                'nitrate': features[2],
                'lead': features[3],
                'oxygen': features[4]
            },
            'recommendations': get_recommendations(features)
        }
        
        return render_template('index.html', 
                             prediction_text=f'{result} (Confidence: {confidence}%)',
                             response=response)
    
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        return render_template('index.html', 
                             prediction_text=f'Error: {str(e)}',
                             response={'status': 'error', 'message': str(e)})
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return render_template('index.html', 
                             prediction_text='Error: An unexpected error occurred',
                             response={'status': 'error', 'message': 'An unexpected error occurred'})

def get_recommendations(features):
    """Generate recommendations based on water parameters"""
    recommendations = []
    ph, turbidity, nitrate, lead, oxygen = features
    
    # pH recommendations
    if ph < 6.5:
        recommendations.append("pH is too acidic. Consider using a neutralizing filter.")
    elif ph > 8.5:
        recommendations.append("pH is too alkaline. Consider using an acid injection system.")
    
    # Turbidity recommendations
    if turbidity > 5:
        recommendations.append("High turbidity detected. Consider using a sediment filter or flocculation treatment.")
    
    # Nitrate recommendations
    if nitrate > 10:
        recommendations.append("Nitrate levels exceed WHO standards. Consider reverse osmosis or ion exchange treatment.")
    
    # Lead recommendations
    if lead > 10:
        recommendations.append("Lead concentration exceeds safe limits. Use activated carbon filtration or reverse osmosis.")
    
    # Oxygen recommendations
    if oxygen < 5:
        recommendations.append("Low dissolved oxygen levels. Consider aeration or oxygenation treatment.")
    
    if not recommendations:
        recommendations.append("All parameters are within acceptable ranges.")
    
    return recommendations

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('index.html', 
                         prediction_text='Error: Page not found',
                         response={'status': 'error', 'message': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Server error: {str(error)}")
    return render_template('index.html', 
                         prediction_text='Error: Internal server error',
                         response={'status': 'error', 'message': 'Internal server error'}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)