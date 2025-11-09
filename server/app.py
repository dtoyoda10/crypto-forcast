from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from routes import register_routes
from config import get_config
import logging
import sys
import os

def setup_logging(config):
    """Configure application logging"""
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    # File handler
    file_handler = logging.FileHandler(config.LOG_FILE)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    return logging.getLogger(__name__)

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)

    # Load configuration
    config = get_config()
    app.config.from_object(config)

    # Setup logging
    logger = setup_logging(config)
    logger.info(f"Starting application in {os.environ.get('FLASK_ENV', 'development')} mode")

    # Initialize JWT
    jwt = JWTManager(app)

    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[config.RATELIMIT_DEFAULT] if config.RATELIMIT_ENABLED else [],
        storage_uri="memory://"
    )

    # Rate limit error handler
    @app.errorhandler(429)
    def ratelimit_handler(e):
        logger.warning(f"Rate limit exceeded: {get_remote_address()}")
        return jsonify({
            'error': 'Rate limit exceeded',
            'message': 'Too many requests. Please try again later.'
        }), 429

    # Configure CORS with specific origins
    CORS(app, resources={
        r"/api/*": {"origins": config.CORS_ORIGINS},
        r"/register": {"origins": config.CORS_ORIGINS},
        r"/login": {"origins": config.CORS_ORIGINS}
    })

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        logger.warning("Expired token accessed")
        return jsonify({
            'error': 'Token has expired',
            'message': 'Please log in again'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        logger.warning(f"Invalid token accessed: {error}")
        return jsonify({
            'error': 'Invalid token',
            'message': 'Authentication failed'
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'error': 'Authorization required',
            'message': 'Request does not contain a valid token'
        }), 401

    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"404 error: {error}")
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"500 error: {error}")
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(f"Unhandled exception: {error}", exc_info=True)
        return jsonify({'error': 'An unexpected error occurred'}), 500

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'crypto-forecast-api'
        }), 200

    # Register routes
    register_routes(app)

    # Create database indexes
    try:
        from models import User
        User.create_indexes()
    except Exception as e:
        logger.error(f"Failed to create database indexes: {e}")

    logger.info("Application initialization complete")
    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)