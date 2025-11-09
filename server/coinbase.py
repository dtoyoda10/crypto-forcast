import requests
from requests.exceptions import RequestException, Timeout
from config import get_config
import logging

logger = logging.getLogger(__name__)
config = get_config()

COINBASE_API_BASE = 'https://api.coinbase.com/v2'
COINBASE_ASSETS_BASE = 'https://coinbase.com/api/v2'

def make_api_request(url, params=None):
    """Make a request to Coinbase API with error handling"""
    try:
        response = requests.get(
            url,
            params=params,
            timeout=config.COINBASE_API_TIMEOUT,
            headers={'User-Agent': 'crypto-forecast/1.0'}
        )
        response.raise_for_status()
        return response.json()
    except Timeout:
        logger.error(f"Timeout while fetching data from {url}")
        return None
    except RequestException as e:
        logger.error(f"Error fetching data from {url}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Invalid JSON response from {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching data from {url}: {e}")
        return None

def get_coins_summary():
    """Fetch summary of all available cryptocurrencies"""
    url = f'{COINBASE_ASSETS_BASE}/assets/summary'
    params = {
        'include_prices': 'true',
        'resolution': 'week',
        'filter': 'listed',
        'base': 'USD'
    }

    logger.info("Fetching coins summary")
    result = make_api_request(url, params)

    if result:
        logger.info("Successfully fetched coins summary")
    else:
        logger.error("Failed to fetch coins summary")

    return result

def get_coins_search():
    """Search for available cryptocurrencies"""
    url = f'{COINBASE_ASSETS_BASE}/assets/search'
    params = {
        'base': 'USD',
        'filter': 'listed',
        'include_prices': 'true',
        'resolution': 'week'
    }

    logger.info("Searching coins")
    result = make_api_request(url, params)

    if result:
        logger.info("Successfully searched coins")
    else:
        logger.error("Failed to search coins")

    return result

def get_coins_histories(coin, period):
    """Fetch historical price data for a specific cryptocurrency"""
    url = f'{COINBASE_API_BASE}/prices/{coin}-USD/historic'
    params = {
        'period': period
    }

    logger.info(f"Fetching historical data for {coin} with period {period}")
    result = make_api_request(url, params)

    if result:
        logger.info(f"Successfully fetched historical data for {coin}")
    else:
        logger.error(f"Failed to fetch historical data for {coin}")

    return result
