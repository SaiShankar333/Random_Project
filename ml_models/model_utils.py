"""
Utility functions for model operations
"""

import joblib
import pandas as pd
import numpy as np
from feature_extraction import prepare_features


def load_trained_model(model_dir='saved_models'):
    """Load the trained model and feature extractor"""
    try:
        model = joblib.load(f"{model_dir}/random_forest_model.pkl")
        feature_extractor = joblib.load(f"{model_dir}/feature_extractor.pkl")
        return model, feature_extractor
    except Exception as e:
        raise Exception(f"Error loading model: {str(e)}")


def predict_single_review(review_data, model, feature_extractor):
    """
    Predict whether a single review is fake
    
    Args:
        review_data: dict with review information
        model: trained ML model
        feature_extractor: fitted feature extractor
    
    Returns:
        dict with prediction results
    """
    # Convert to DataFrame
    df = pd.DataFrame([review_data])
    
    # Extract features
    features, _ = prepare_features(df, feature_extractor, is_training=False)
    
    # Predict
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    
    # Determine status
    if prediction == 1:
        status = 'FAKE'
    elif probabilities[1] > 0.3:
        status = 'SUSPICIOUS'
    else:
        status = 'GENUINE'
    
    # Analyze risk factors
    risk_factors = analyze_risk_factors(review_data, probabilities[1])
    
    return {
        'prediction': 'FAKE' if prediction == 1 else 'GENUINE',
        'status': status,
        'confidence': float(max(probabilities)),
        'fake_probability': float(probabilities[1]),
        'genuine_probability': float(probabilities[0]),
        'risk_factors': risk_factors
    }


def predict_bulk_reviews(reviews_df, model, feature_extractor):
    """
    Predict multiple reviews at once
    
    Args:
        reviews_df: DataFrame with review data
        model: trained ML model
        feature_extractor: fitted feature extractor
    
    Returns:
        DataFrame with predictions added
    """
    # Extract features
    features, _ = prepare_features(reviews_df, feature_extractor, is_training=False)
    
    # Predict
    predictions = model.predict(features)
    probabilities = model.predict_proba(features)
    
    # Add predictions to dataframe
    result_df = reviews_df.copy()
    result_df['prediction'] = ['FAKE' if p == 1 else 'GENUINE' for p in predictions]
    result_df['fake_probability'] = probabilities[:, 1]
    result_df['genuine_probability'] = probabilities[:, 0]
    result_df['confidence'] = np.max(probabilities, axis=1)
    
    return result_df


def analyze_risk_factors(review_data, fake_probability):
    """Identify specific risk factors in a review"""
    risk_factors = []
    
    # Check metadata issues
    if pd.isna(review_data.get('order_id')) or review_data.get('order_id') is None:
        risk_factors.append("Missing order ID")
    
    if pd.isna(review_data.get('purchase_id')) or review_data.get('purchase_id') is None:
        risk_factors.append("Missing purchase ID")
    
    if not review_data.get('verified_purchase', True):
        risk_factors.append("Unverified purchase - IDs do not match")
    
    # Check timing issues
    days = review_data.get('days_after_purchase', 0)
    if days < 0:
        risk_factors.append(f"Review posted before purchase (impossible timing)")
    elif days > 365:
        risk_factors.append(f"Review posted {days} days after purchase (very late)")
    
    # Check user behavior
    review_count = review_data.get('user_review_count', 0)
    if review_count > 50:
        risk_factors.append(f"User has posted {review_count} reviews (potential bot)")
    
    # Check rating
    rating = review_data.get('rating', 3.0)
    if rating in [1.0, 5.0]:
        risk_factors.append(f"Extreme rating ({rating} stars)")
    
    # Check text quality
    text = review_data.get('text_', '')
    if len(str(text)) < 50:
        risk_factors.append("Very short review (low detail)")
    
    # Overall risk
    if fake_probability > 0.7:
        risk_factors.append(f"High fake probability ({fake_probability:.1%})")
    
    return risk_factors


def get_feature_importance(model, feature_extractor):
    """Get feature importance from the model"""
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        
        # Get feature names (statistical + TF-IDF)
        statistical_features = [
            'review_length', 'word_count', 'avg_word_length', 'sentence_count',
            'exclamation_count', 'question_count', 'caps_ratio', 'unique_word_ratio',
            'verified_purchase', 'order_id_missing', 'purchase_id_missing',
            'days_after_purchase', 'negative_days', 'very_late_review',
            'user_review_count', 'high_review_count', 'rating', 'extreme_rating'
        ]
        
        # Get TF-IDF feature names
        if hasattr(feature_extractor.tfidf_vectorizer, 'get_feature_names_out'):
            tfidf_features = feature_extractor.tfidf_vectorizer.get_feature_names_out().tolist()
        else:
            tfidf_features = [f"tfidf_{i}" for i in range(len(importances) - len(statistical_features))]
        
        all_features = statistical_features + tfidf_features
        
        # Create importance dataframe
        importance_df = pd.DataFrame({
            'feature': all_features[:len(importances)],
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        return importance_df
    
    return None


def validate_review_data(review_data):
    """Validate review data has required fields"""
    required_fields = ['text_', 'rating']
    optional_fields = [
        'order_id', 'purchase_id', 'verified_purchase',
        'user_id', 'days_after_purchase', 'user_review_count'
    ]
    
    # Check required fields
    for field in required_fields:
        if field not in review_data:
            raise ValueError(f"Missing required field: {field}")
    
    # Fill optional fields with defaults
    defaults = {
        'order_id': None,
        'purchase_id': None,
        'verified_purchase': False,
        'user_id': 'UNKNOWN',
        'days_after_purchase': 30,
        'user_review_count': 1,
        'category': 'General'
    }
    
    for field, default_value in defaults.items():
        if field not in review_data:
            review_data[field] = default_value
    
    return review_data

