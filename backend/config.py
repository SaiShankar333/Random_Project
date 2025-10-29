"""
Configuration settings for the Flask backend
"""

import os

class Config:
    """Base configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fake-review-detection-secret-key'
    DEBUG = True
    
    # Model paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ML_MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(BASE_DIR), 'ml_models', 'saved_models'))
    DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(BASE_DIR), 'data'))
    
    # CORS settings
    CORS_ORIGINS = ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:3000', 'http://127.0.0.1:5173', 'http://127.0.0.1:5174']
    
    # Upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
    
    # Pagination
    REVIEWS_PER_PAGE = 50


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

