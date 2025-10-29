"""
Prediction endpoint for single review analysis
"""

from flask import Blueprint, request, jsonify
import sys
import os

# Add ml_models to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ml_models'))

from model_utils import load_trained_model, predict_single_review, validate_review_data
from config import Config

bp = Blueprint('predict', __name__)

# Load model once at startup
try:
    model, feature_extractor = load_trained_model(Config.ML_MODELS_DIR)
    print("Model loaded successfully for prediction endpoint")
except Exception as e:
    print(f"Error loading model: {e}")
    model, feature_extractor = None, None


@bp.route('/predict', methods=['POST'])
def predict_review():
    """
    Predict if a single review is fake
    
    Request JSON:
    {
        "text_": "Review text here",
        "order_id": "ORD-2024-12345" (optional),
        "purchase_id": "PUR-ABC123" (optional),
        "verified_purchase": true/false (optional),
        "user_id": "USER-12345" (optional),
        "days_after_purchase": 30 (optional),
        "user_review_count": 5 (optional),
        "rating": 4.5 (required),
        "category": "Electronics" (optional)
    }
    
    Returns:
    {
        "prediction": "FAKE" or "GENUINE",
        "status": "FAKE", "GENUINE", or "SUSPICIOUS",
        "confidence": 0.95,
        "fake_probability": 0.95,
        "genuine_probability": 0.05,
        "risk_factors": ["Missing order ID", ...]
    }
    """
    
    if model is None or feature_extractor is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        if 'text_' not in data:
            return jsonify({'error': 'Missing required field: text_'}), 400
        
        if 'rating' not in data:
            return jsonify({'error': 'Missing required field: rating'}), 400
        
        # Validate and fill defaults
        review_data = validate_review_data(data)
        
        # Make prediction
        result = predict_single_review(review_data, model, feature_extractor)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500


@bp.route('/predict/batch', methods=['POST'])
def predict_batch():
    """
    Predict multiple reviews at once
    
    Request JSON:
    {
        "reviews": [
            {"text_": "...", "rating": 5, ...},
            {"text_": "...", "rating": 4, ...}
        ]
    }
    """
    
    if model is None or feature_extractor is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        if not data or 'reviews' not in data:
            return jsonify({'error': 'No reviews provided'}), 400
        
        reviews = data['reviews']
        
        if not isinstance(reviews, list):
            return jsonify({'error': 'Reviews must be a list'}), 400
        
        if len(reviews) == 0:
            return jsonify({'error': 'Empty reviews list'}), 400
        
        # Predict each review
        results = []
        for review in reviews:
            try:
                review_data = validate_review_data(review)
                result = predict_single_review(review_data, model, feature_extractor)
                results.append(result)
            except Exception as e:
                results.append({'error': str(e)})
        
        return jsonify({
            'total': len(reviews),
            'results': results
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Batch prediction failed: {str(e)}'}), 500

