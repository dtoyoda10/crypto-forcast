import requests
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
from requests.exceptions import RequestException
from config import get_config
import logging

logger = logging.getLogger(__name__)
config = get_config()

def get_market_chart(coin, period):
    """
    Fetch historical price data and generate predictions using Linear Regression.

    This function retrieves historical cryptocurrency prices and uses them to train
    a simple linear regression model to forecast future prices.
    """
    try:
        # Fetch historical data from Coinbase API
        url = f'https://api.coinbase.com/v2/prices/{coin}-USD/historic'
        params = {'period': period}

        logger.info(f"Fetching market data for {coin} with period {period}")

        response = requests.get(
            url,
            params=params,
            timeout=config.COINBASE_API_TIMEOUT,
            headers={'User-Agent': 'crypto-forecast/1.0'}
        )
        response.raise_for_status()
        ohlc_data = response.json()

        # Validate response structure
        if 'data' not in ohlc_data or 'prices' not in ohlc_data['data']:
            logger.error(f"Invalid response structure from Coinbase API for {coin}")
            return None

        prices = ohlc_data['data']['prices']

        if not prices or len(prices) < 2:
            logger.error(f"Insufficient price data for {coin}: {len(prices) if prices else 0} points")
            return None

        logger.info(f"Retrieved {len(prices)} price points for {coin}")

        # Convert price data to numpy arrays
        timestamps = []
        price_values = []

        for price_point in prices:
            try:
                timestamp = int(price_point['time'])
                price = float(price_point['price'])
                timestamps.append(timestamp)
                price_values.append(price)
            except (KeyError, ValueError, TypeError) as e:
                logger.warning(f"Skipping invalid price point: {e}")
                continue

        if len(timestamps) < 2:
            logger.error(f"Not enough valid data points for {coin}")
            return None

        # Prepare data for model training
        X = np.array(timestamps).reshape(-1, 1)
        y = np.array(price_values).reshape(-1, 1)

        # Normalize timestamps for better model performance
        scaler_X = MinMaxScaler()
        X_scaled = scaler_X.fit_transform(X)

        # Train linear regression model
        model = LinearRegression()
        model.fit(X_scaled, y)

        # Determine prediction interval based on period
        prediction_intervals = {
            'hour': {'count': 12, 'delta_minutes': 5},     # Next hour in 5-min intervals
            'day': {'count': 24, 'delta_minutes': 60},     # Next day in hourly intervals
            'week': {'count': 14, 'delta_minutes': 720},   # Next 2 weeks in 12-hour intervals
            'month': {'count': 30, 'delta_minutes': 1440}, # Next month in daily intervals
            'year': {'count': 12, 'delta_minutes': 43200}, # Next year in monthly intervals
            'all': {'count': 30, 'delta_minutes': 1440}    # Next month in daily intervals
        }

        interval_config = prediction_intervals.get(period, prediction_intervals['day'])

        # Generate future timestamps for predictions
        last_timestamp = timestamps[-1]
        future_timestamps = []

        for i in range(1, interval_config['count'] + 1):
            future_time = last_timestamp + (i * interval_config['delta_minutes'] * 60)
            future_timestamps.append(future_time)

        # Scale future timestamps
        future_X = np.array(future_timestamps).reshape(-1, 1)
        future_X_scaled = scaler_X.transform(future_X)

        # Generate predictions
        predictions = model.predict(future_X_scaled)

        # Format predictions with timestamps
        result = []
        for timestamp, predicted_price in zip(future_timestamps, predictions):
            formatted_date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            result.append([formatted_date, float(predicted_price[0])])

        logger.info(f"Successfully generated {len(result)} predictions for {coin}")

        # Add model performance metrics for transparency
        train_score = model.score(X_scaled, y)
        logger.info(f"Model R² score on training data: {train_score:.4f}")

        return result

    except RequestException as e:
        logger.error(f"Network error while fetching market data for {coin}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Data processing error for {coin}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in get_market_chart for {coin}: {e}", exc_info=True)
        return None
