import hashlib
import hmac
import datetime
import requests
from collections import OrderedDict
from urllib.parse import urlencode, urlparse, parse_qs
import time

import pandas as pd

# Define your private and public keys and the base URL
PRIVATE_KEY = 'Your private key goes here'
PUBLIC_KEY = 'your public key goes here'
BASE_URL = 'https://api.futuur.com/api/v1/'

# Function to generate the HMAC signature for secure API requests
def build_signature(params: dict):
    params_to_sign = OrderedDict(sorted(list(params.items())))
    params_to_sign = urlencode(params_to_sign)
    encoded_params = params_to_sign.encode('utf-8')
    encoded_private_key = PRIVATE_KEY.encode('utf-8')
    data = {
        'hmac': hmac.new(encoded_private_key, encoded_params, hashlib.sha512).hexdigest(),
        'Timestamp': params['Timestamp']
    }
    return data

# Function to generate the headers including the timestamp and signature
def build_headers(params: dict):
    signature = build_signature(params)
    headers = {
        'Key': PUBLIC_KEY,
        'Timestamp': str(signature.get('Timestamp')),
        'HMAC': signature.get('hmac')
    }
    return headers

# Function to call the API
def call_api(endpoint: str, params: dict = None, method: str = 'GET') -> dict:
    url_params = '?' + urlencode(params) if params else ''
    headers = build_headers(params)
    url = BASE_URL + endpoint + url_params
    response = requests.request(method=method, url=url, headers=headers)

    # If we hit a throttling response, handle it by waiting 60 seconds
    if response.status_code == 429 or 'throttled' in response.text.lower():
        print("Request was throttled. Waiting for 60 seconds...")
        time.sleep(60)
        return call_api(endpoint, params, method)

    return response.json()

# Function to fetch all paginated results
def fetch_all_results():
    """Fetch all paginated results by handling pagination and throttling."""
    all_results = []
    params = {
        'Key': PUBLIC_KEY,
        'Timestamp': int(datetime.datetime.utcnow().timestamp()),
        'category': 5,
        'limit': 20  # Adjust the limit as needed
    }

    # Initial request to get the first set of results
    response = call_api(endpoint='markets/', params=params)
    all_results.extend(response.get('results', []))

    # Loop to follow pagination until all results are fetched
    while response.get('pagination', {}).get('next'):
        next_url = response['pagination']['next']
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        # Convert list values from parse_qs to single values
        next_params = {k: v[0] for k, v in next_params.items()}

        # Update the timestamp for each subsequent request
        next_params['Timestamp'] = int(datetime.datetime.utcnow().timestamp())

        # Recalculate headers for each page request
        headers = build_headers(next_params)

        # Fetch the next page using the "next" URL
        response = requests.get(next_url, headers=headers)

        # Check for throttling response, wait and retry if necessary
        if response.status_code == 429 or 'throttled' in response.text.lower():
            print("Request was throttled. Waiting for 60 seconds...")
            time.sleep(60)
            response = requests.get(next_url, headers=headers)

        response = response.json()
        #print(f"Fetching results from: {next_url}")

        # Extend the list with the next page's results
        all_results.extend(response.get('results', []))

    return all_results

def futuur_data_results():
    # Fetch all results
    all_events_futuur = fetch_all_results()

    # Print the total number of results fetched
    print(f"Total results fetched for futuur: {len(all_events_futuur)}")


    # List to store the extracted data
    flattened_data = []

    # Loop through each dictionary in the data
    for event in all_events_futuur:
        # Extract event title, start date, and end date
        event_title = event.get('title', '')
        event_start_date = event.get('event_start_date', '')
        event_end_date = event.get('bet_end_date', '')

        # Variables to store "Yes" and "No" prices
        outcome_yes = None
        outcome_no = None
        other_outcomes = []

        # Extract the outcomes information
        for outcome in event.get('outcomes', []):
            group_item_title = outcome.get('title', '')
            price = outcome['price'].get('BTC', None)  # Extract BTC price
            if price is None:
                price = outcome['price'].get('OOM', None)

            # Truncate the price to 3 decimal places
            if price is not None:
                price = "{:.3f}".format(float(price))

            # Check if the outcome is "Yes" or "No", otherwise add it to other_outcomes
            if group_item_title.lower() == 'yes':
                outcome_yes = price
            elif group_item_title.lower() == 'no':
                outcome_no = price
            else:
                other_outcomes.append((group_item_title, price))

        # Format dates to only include the date part (YYYY-MM-DD)
        event_start_date = event_start_date[:10] if event_start_date else ''
        event_end_date = event_end_date[:10] if event_end_date else ''

        # If we have both "Yes" and "No" outcomes, add them in a single row
        if outcome_yes and outcome_no:
            flattened_data.append({
                'title': event_title,
                'startDate': event_start_date,
                'endDate': event_end_date,
                'groupItemTitle': 'Yes/No',
                'outcome_yes': outcome_yes,
                'outcome_no': outcome_no
            })

        # Add the other outcomes (non-Yes/No outcomes) in separate rows
        for group_item_title, price in other_outcomes:
            flattened_data.append({
                'title': event_title if group_item_title == other_outcomes[0][0] else '',  # Only show title once for the first row
                'startDate': event_start_date if group_item_title == other_outcomes[0][0] else '',
                'endDate': event_end_date if group_item_title == other_outcomes[0][0] else '',
                'groupItemTitle': group_item_title,
                'outcome_yes': price,
                'outcome_no': ''
            })

    # Convert the list of dictionaries into a DataFrame
    df_futuur = pd.DataFrame(flattened_data)
    return df_futuur




