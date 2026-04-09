"""
Configuration settings for the application
"""
import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-12345'
    DEBUG = False
    TESTING = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'data', 'uploads')
    EXPORT_FOLDER = os.path.join(os.path.dirname(__file__), 'data', 'exports')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

# Default config
config = DevelopmentConfig()
