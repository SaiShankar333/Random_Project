"""
Analytics endpoint for dashboard statistics and metrics
"""

from flask import Blueprint, request, jsonify
import pandas as pd
import json
import os
import sys

# Add ml_models to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ml_models'))

from config import Config

bp = Blueprint('analytics', __name__)

# Load dataset and metrics
try:
    data_path = os.path.join(Config.DATA_DIR, 'enhanced_reviews_dataset.csv')
    df = pd.read_csv(data_path)
    df['label_binary'] = (df['label'] == 'CG').astype(int)
    
    metrics_path = os.path.join(Config.ML_MODELS_DIR, 'full_metrics.json')
    with open(metrics_path, 'r') as f:
        model_metrics = json.load(f)
    
    print("Dataset and metrics loaded successfully for analytics")
except Exception as e:
    print(f"Error loading dataset/metrics: {e}")
    df = None
    model_metrics = {}


@bp.route('/analytics/summary', methods=['GET'])
def get_summary():
    """
    Get overall summary statistics
    
    Returns:
    {
        "total_reviews": 40432,
        "fake_reviews": 20216,
        "genuine_reviews": 20216,
        "fake_percentage": 50.0,
        "model_accuracy": 0.95
    }
    """
    
    if df is None:
        return jsonify({'error': 'Dataset not loaded'}), 500
    
    try:
        total = len(df)
        fake_count = len(df[df['label'] == 'CG'])
        genuine_count = len(df[df['label'] == 'OR'])
        
        summary = {
            'total_reviews': int(total),
            'fake_reviews': int(fake_count),
            'genuine_reviews': int(genuine_count),
            'fake_percentage': round(fake_count / total * 100, 2),
            'genuine_percentage': round(genuine_count / total * 100, 2),
            'model_accuracy': model_metrics.get('accuracy', 0.0)
        }
        
        return jsonify(summary), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to compute summary: {str(e)}'}), 500


@bp.route('/analytics/category', methods=['GET'])
def get_category_stats():
    """
    Get statistics by category
    
    Returns:
    {
        "categories": [
            {
                "category": "Electronics",
                "total": 5000,
                "fake": 2500,
                "genuine": 2500,
                "fake_rate": 50.0
            },
            ...
        ]
    }
    """
    
    if df is None:
        return jsonify({'error': 'Dataset not loaded'}), 500
    
    try:
        category_stats = []
        
        for category in df['category'].unique():
            cat_df = df[df['category'] == category]
            total = len(cat_df)
            fake = len(cat_df[cat_df['label'] == 'CG'])
            genuine = len(cat_df[cat_df['label'] == 'OR'])
            
            category_stats.append({
                'category': category,
                'total': int(total),
                'fake': int(fake),
                'genuine': int(genuine),
                'fake_rate': round(fake / total * 100, 2) if total > 0 else 0
            })
        
        # Sort by fake rate descending
        category_stats.sort(key=lambda x: x['fake_rate'], reverse=True)
        
        return jsonify({'categories': category_stats}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to compute category stats: {str(e)}'}), 500


@bp.route('/analytics/timing', methods=['GET'])
def get_timing_stats():
    """
    Get timing-based statistics (days after purchase)
    
    Returns distribution of reviews by timing
    """
    
    if df is None:
        return jsonify({'error': 'Dataset not loaded'}), 500
    
    try:
        # Define bins
        bins = [-float('inf'), 0, 7, 30, 90, 180, 365, float('inf')]
        labels = ['Before Purchase', '0-7 days', '8-30 days', '31-90 days', 
                 '91-180 days', '181-365 days', '365+ days']
        
        df['timing_bin'] = pd.cut(df['days_after_purchase'], bins=bins, labels=labels)
        
        timing_stats = []
        for label in labels:
            bin_df = df[df['timing_bin'] == label]
            total = len(bin_df)
            fake = len(bin_df[bin_df['label'] == 'CG'])
            
            if total > 0:
                timing_stats.append({
                    'period': label,
                    'total': int(total),
                    'fake': int(fake),
                    'genuine': int(total - fake),
                    'fake_rate': round(fake / total * 100, 2)
                })
        
        return jsonify({'timing_distribution': timing_stats}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to compute timing stats: {str(e)}'}), 500


@bp.route('/analytics/reviews', methods=['GET'])
def get_reviews():
    """
    Get paginated list of reviews
    
    Query parameters:
    - page: page number (default 1)
    - per_page: items per page (default 50)
    - filter: 'all', 'fake', 'genuine' (default 'all')
    """
    
    if df is None:
        return jsonify({'error': 'Dataset not loaded'}), 500
    
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        filter_type = request.args.get('filter', 'all')
        
        # Filter data
        if filter_type == 'fake':
            filtered_df = df[df['label'] == 'CG']
        elif filter_type == 'genuine':
            filtered_df = df[df['label'] == 'OR']
        else:
            filtered_df = df
        
        # Pagination
        total = len(filtered_df)
        start = (page - 1) * per_page
        end = start + per_page
        
        page_df = filtered_df.iloc[start:end]
        
        # Convert to dict
        reviews = []
        for _, row in page_df.iterrows():
            reviews.append({
                'text': row['text_'],
                'rating': float(row['rating']),
                'label': row['label'],
                'category': row['category'],
                'verified_purchase': bool(row['verified_purchase']),
                'days_after_purchase': int(row['days_after_purchase']),
                'user_review_count': int(row['user_review_count']),
                'order_id': row['order_id'] if pd.notna(row['order_id']) else None,
                'purchase_id': row['purchase_id'] if pd.notna(row['purchase_id']) else None
            })
        
        return jsonify({
            'total': int(total),
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page,
            'reviews': reviews
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch reviews: {str(e)}'}), 500


@bp.route('/analytics/model-performance', methods=['GET'])
def get_model_performance():
    """
    Get model performance metrics
    """
    
    if not model_metrics:
        return jsonify({'error': 'Metrics not loaded'}), 500
    
    try:
        # Extract key metrics
        performance = {
            'accuracy': model_metrics.get('accuracy', 0),
            'precision': model_metrics.get('precision', 0),
            'recall': model_metrics.get('recall', 0),
            'f1_score': model_metrics.get('f1_score', 0),
            'roc_auc': model_metrics.get('roc_auc', 0),
            'confusion_matrix': {
                'true_negatives': model_metrics.get('true_negatives', 0),
                'false_positives': model_metrics.get('false_positives', 0),
                'false_negatives': model_metrics.get('false_negatives', 0),
                'true_positives': model_metrics.get('true_positives', 0)
            },
            'classification_report': model_metrics.get('classification_report', {})
        }
        
        return jsonify(performance), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch model performance: {str(e)}'}), 500


@bp.route('/analytics/verification-status', methods=['GET'])
def get_verification_status():
    """
    Get verification status distribution
    """
    
    if df is None:
        return jsonify({'error': 'Dataset not loaded'}), 500
    
    try:
        verified = len(df[df['verified_purchase'] == True])
        unverified = len(df[df['verified_purchase'] == False])
        missing_order = df['order_id'].isna().sum()
        missing_purchase = df['purchase_id'].isna().sum()
        
        return jsonify({
            'verified_purchases': int(verified),
            'unverified_purchases': int(unverified),
            'missing_order_id': int(missing_order),
            'missing_purchase_id': int(missing_purchase),
            'verification_rate': round(verified / len(df) * 100, 2)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to compute verification status: {str(e)}'}), 500

