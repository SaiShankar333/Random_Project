"""
Bulk processing endpoint for analyzing multiple reviews from CSV
"""

from flask import Blueprint, request, jsonify, send_file
import pandas as pd
import os
import sys
from io import BytesIO
import tempfile

# Add ml_models to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ml_models'))

from model_utils import load_trained_model, predict_bulk_reviews
from config import Config

bp = Blueprint('bulk', __name__)

# Load model once at startup
try:
    model, feature_extractor = load_trained_model(Config.ML_MODELS_DIR)
    print("Model loaded successfully for bulk endpoint")
except Exception as e:
    print(f"Error loading model: {e}")
    model, feature_extractor = None, None


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'xlsx'}


@bp.route('/bulk/upload', methods=['POST'])
def upload_bulk_reviews():
    """
    Upload CSV/Excel file for bulk prediction
    
    Expects file upload with reviews containing:
    - text_ (required)
    - rating (required)
    - order_id, purchase_id, verified_purchase, etc. (optional)
    
    Returns:
    {
        "total": 100,
        "fake_count": 45,
        "genuine_count": 55,
        "results": [...],
        "download_url": "/api/bulk/download/abc123"
    }
    """
    
    if model is None or feature_extractor is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only CSV and XLSX allowed'}), 400
        
        # Read file
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        # Validate required columns
        if 'text_' not in df.columns:
            return jsonify({'error': 'Missing required column: text_'}), 400
        
        if 'rating' not in df.columns:
            return jsonify({'error': 'Missing required column: rating'}), 400
        
        # Fill missing optional columns with defaults
        if 'order_id' not in df.columns:
            df['order_id'] = None
        if 'purchase_id' not in df.columns:
            df['purchase_id'] = None
        if 'verified_purchase' not in df.columns:
            df['verified_purchase'] = False
        if 'user_id' not in df.columns:
            df['user_id'] = 'UNKNOWN'
        if 'days_after_purchase' not in df.columns:
            df['days_after_purchase'] = 30
        if 'user_review_count' not in df.columns:
            df['user_review_count'] = 1
        if 'category' not in df.columns:
            df['category'] = 'General'
        
        # Predict
        result_df = predict_bulk_reviews(df, model, feature_extractor)
        
        # Calculate summary
        total = len(result_df)
        fake_count = len(result_df[result_df['prediction'] == 'FAKE'])
        genuine_count = len(result_df[result_df['prediction'] == 'GENUINE'])
        
        # Convert to JSON for response
        results = []
        for _, row in result_df.head(100).iterrows():  # Limit to first 100 for response
            results.append({
                'text': row['text_'],
                'rating': float(row['rating']),
                'prediction': row['prediction'],
                'confidence': float(row['confidence']),
                'fake_probability': float(row['fake_probability']),
                'genuine_probability': float(row['genuine_probability'])
            })
        
        # Save full results temporarily for download
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        result_df.to_csv(temp_file.name, index=False)
        temp_file.close()
        
        # Store file path in session or return immediately
        file_id = os.path.basename(temp_file.name)
        
        return jsonify({
            'total': int(total),
            'fake_count': int(fake_count),
            'genuine_count': int(genuine_count),
            'fake_percentage': round(fake_count / total * 100, 2),
            'genuine_percentage': round(genuine_count / total * 100, 2),
            'results_preview': results,
            'download_id': file_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Bulk processing failed: {str(e)}'}), 500


@bp.route('/bulk/download/<file_id>', methods=['GET'])
def download_results(file_id):
    """
    Download processed results CSV
    """
    try:
        # Reconstruct file path
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, file_id)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found or expired'}), 404
        
        return send_file(
            file_path,
            mimetype='text/csv',
            as_attachment=True,
            download_name='predictions.csv'
        )
        
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500


@bp.route('/bulk/template', methods=['GET'])
def download_template():
    """
    Download CSV template with required columns
    """
    try:
        # Create sample template
        template_data = {
            'text_': [
                'This product is amazing! Best purchase ever!',
                'Not satisfied with the quality. Would not recommend.',
                'Good value for money. Works as expected.'
            ],
            'rating': [5.0, 2.0, 4.0],
            'order_id': ['ORD-2024-12345', 'ORD-2024-12346', None],
            'purchase_id': ['PUR-ABC123', 'PUR-DEF456', 'PUR-GHI789'],
            'verified_purchase': [True, True, False],
            'user_id': ['USER-001', 'USER-002', 'USER-003'],
            'days_after_purchase': [15, 30, -5],
            'user_review_count': [3, 5, 150],
            'category': ['Electronics', 'Home', 'Electronics']
        }
        
        template_df = pd.DataFrame(template_data)
        
        # Create in-memory CSV
        output = BytesIO()
        template_df.to_csv(output, index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name='review_template.csv'
        )
        
    except Exception as e:
        return jsonify({'error': f'Template generation failed: {str(e)}'}), 500

