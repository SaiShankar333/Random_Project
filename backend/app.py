"""
Flask Backend API for Fake Review Detection System
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add ml_models to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml_models'))

from config import config
from routes import predict, analytics, bulk

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config['development'])

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})


# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if API is running"""
    return jsonify({
        'status': 'healthy',
        'message': 'Fake Review Detection API is running'
    })


# Register blueprints
app.register_blueprint(predict.bp, url_prefix='/api')
app.register_blueprint(analytics.bp, url_prefix='/api')
app.register_blueprint(bulk.bp, url_prefix='/api')


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400


if __name__ == '__main__':
    print("=" * 60)
    print("Fake Review Detection API Server")
    print("=" * 60)
    print("Starting server on http://localhost:5001")
    print("API Documentation: http://localhost:5001/api/health")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )

