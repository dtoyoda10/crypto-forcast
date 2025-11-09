import os
from datetime import timedelta

class Config:
    """Base configuration with secure defaults"""

    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    DEBUG = False
    TESTING = False

    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Database settings
    MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017')
    MONGODB_DB_NAME = os.environ.get('MONGODB_DB_NAME', 'crypto_forcast')

    # API settings
    COINBASE_API_TIMEOUT = int(os.environ.get('COINBASE_API_TIMEOUT', '10'))
    CACHE_TIMEOUT = int(os.environ.get('CACHE_TIMEOUT', '300'))

    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')

    # Rate limiting
    RATELIMIT_ENABLED = os.environ.get('RATELIMIT_ENABLED', 'True').lower() == 'true'
    RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', '100 per hour')

    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'app.log')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

    # Enforce required environment variables in production
    @classmethod
    def validate(cls):
        required_vars = ['JWT_SECRET_KEY', 'MONGODB_URI', 'SECRET_KEY']
        missing = [var for var in required_vars if not os.environ.get(var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    MONGODB_DB_NAME = 'crypto_forcast_test'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')

    configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }

    config_class = configs.get(env, DevelopmentConfig)

    if env == 'production':
        config_class.validate()

    return config_class
