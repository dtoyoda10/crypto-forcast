from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
from services import get_market_chart
from coinbase import get_coins_search, get_coins_summary, get_coins_histories
from auth import register_user, login_user
import logging

logger = logging.getLogger(__name__)

def validate_coin_symbol(coin):
    """Validate cryptocurrency symbol format"""
    if not coin:
        return False
    if len(coin) < 2 or len(coin) > 10:
        return False
    return coin.replace('-', '').isalnum()

def validate_period(period):
    """Validate time period parameter"""
    valid_periods = ['hour', 'day', 'week', 'month', 'year', 'all']
    return period in valid_periods

def register_routes(app):
    @app.route('/register', methods=['POST'])
    def register():
        """User registration endpoint"""
        try:
            return register_user(request.get_json())
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return jsonify({'error': 'Registration failed'}), 500

    @app.route('/login', methods=['POST'])
    def login():
        """User login endpoint"""
        try:
            return login_user(request.get_json())
        except Exception as e:
            logger.error(f"Login error: {e}")
            return jsonify({'error': 'Login failed'}), 500

    @app.route('/api/prediction', methods=['POST'])
    def get_coins_prediction():
        """Get cryptocurrency price predictions"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Request body is required'}), 400

            coin = data.get('coin', '').strip().upper()
            period = data.get('period', '').strip().lower()

            if not coin:
                return jsonify({'error': 'Coin symbol is required'}), 400

            if not validate_coin_symbol(coin):
                return jsonify({'error': 'Invalid coin symbol format'}), 400

            if not period:
                return jsonify({'error': 'Period is required'}), 400

            if not validate_period(period):
                return jsonify({
                    'error': 'Invalid period',
                    'valid_periods': ['hour', 'day', 'week', 'month', 'year', 'all']
                }), 400

            predictions = get_market_chart(coin, period)

            if predictions is None:
                return jsonify({'error': 'Failed to generate predictions'}), 500

            return jsonify({
                'coin': coin,
                'period': period,
                'predictions': predictions
            })

        except ValueError as e:
            logger.error(f"Validation error in prediction endpoint: {e}")
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logger.error(f"Error in prediction endpoint: {e}", exc_info=True)
            return jsonify({'error': 'Failed to get predictions'}), 500

    @app.route('/api/get_coins_summary', methods=['GET'])
    def coins_summary():
        """Get summary of all available cryptocurrencies"""
        try:
            result = get_coins_summary()

            if result is None:
                return jsonify({'error': 'Failed to fetch coins summary'}), 500

            return jsonify(result)

        except Exception as e:
            logger.error(f"Error fetching coins summary: {e}", exc_info=True)
            return jsonify({'error': 'Failed to fetch coins summary'}), 500

    @app.route('/api/get_coins_search', methods=['GET'])
    def coins_search():
        """Search for cryptocurrencies"""
        try:
            result = get_coins_search()

            if result is None:
                return jsonify({'error': 'Failed to search coins'}), 500

            return jsonify(result)

        except Exception as e:
            logger.error(f"Error searching coins: {e}", exc_info=True)
            return jsonify({'error': 'Failed to search coins'}), 500

    @app.route('/api/get_coins_histories', methods=['POST'])
    def coins_histories():
        """Get historical price data for a cryptocurrency"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Request body is required'}), 400

            coin = data.get('coin', '').strip().upper()
            period = data.get('period', '').strip().lower()

            if not coin:
                return jsonify({'error': 'Coin symbol is required'}), 400

            if not validate_coin_symbol(coin):
                return jsonify({'error': 'Invalid coin symbol format'}), 400

            if not period:
                return jsonify({'error': 'Period is required'}), 400

            if not validate_period(period):
                return jsonify({
                    'error': 'Invalid period',
                    'valid_periods': ['hour', 'day', 'week', 'month', 'year', 'all']
                }), 400

            result = get_coins_histories(coin, period)

            if result is None:
                return jsonify({'error': 'Failed to fetch historical data'}), 500

            return jsonify({
                'coin': coin,
                'period': period,
                'data': result
            })

        except ValueError as e:
            logger.error(f"Validation error in histories endpoint: {e}")
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logger.error(f"Error fetching coin histories: {e}", exc_info=True)
            return jsonify({'error': 'Failed to fetch historical data'}), 500