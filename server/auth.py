from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from models import User
import re
import logging

logger = logging.getLogger(__name__)

def validate_email(email):
    """Validate email format"""
    if not email:
        return False
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if not password:
        return False, "Password is required"
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit"
    return True, "Password is valid"

def register_user(data):
    """Register a new user with validation"""
    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    email = data.get('email', '').strip()
    password = data.get('password', '')

    # Validate email
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    # Validate password
    is_valid, message = validate_password(password)
    if not is_valid:
        return jsonify({'error': message}), 400

    try:
        # Check if user already exists
        existing_user = User.find_by_email(email)
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 409

        # Create new user with hashed password
        password_hash = User.hash_password(password)
        user = User(email, password_hash)
        user.save()

        logger.info(f"New user registered: {email}")
        return jsonify({
            'message': 'User registered successfully',
            'email': email
        }), 201

    except ValueError as e:
        logger.error(f"Validation error during registration: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error during user registration: {e}")
        return jsonify({'error': 'An error occurred during registration'}), 500

def login_user(data):
    """Authenticate user and return JWT tokens"""
    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    email = data.get('email', '').strip()
    password = data.get('password', '')

    # Validate input
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    try:
        # Find user and verify password
        user = User.find_by_email(email)

        if not user:
            # Use generic message to prevent user enumeration
            return jsonify({'error': 'Invalid credentials'}), 401

        if not user.verify_password(password):
            logger.warning(f"Failed login attempt for user: {email}")
            return jsonify({'error': 'Invalid credentials'}), 401

        # Generate tokens
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        logger.info(f"User logged in successfully: {email}")
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'email': email
        }), 200

    except Exception as e:
        logger.error(f"Error during user login: {e}")
        return jsonify({'error': 'An error occurred during login'}), 500