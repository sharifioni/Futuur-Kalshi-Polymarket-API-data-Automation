import requests
import pandas as pd
import ast  # To safely evaluate strings containing lists


def poly_market_data():
    # Base URL of the API
    base_url = "https://gamma-api.polymarket.com/events?closed=false"

    # Initialize a list to store all results
    all_results_polymarket = []

    # Parameters for pagination
    params = {  # Filter for open events
        "limit": 20,        # Set limit of results per page
        "offset": 0         # Start at the first result
    }

    while True:
        # Make the request with the current offset and limit
        response = requests.get(base_url, params=params)
        data = response.json()

        # Add the results from the current page to the list of all results
        all_results_polymarket.extend(data)

        # If the number of results is less than the limit, we have reached the end
        if len(data) < params["limit"]:
            break

        # Increment the offset by the limit to get the next batch of results
        params["offset"] += params["limit"]

    # Print or work with the collected data
    print(f"Total results fetched for polymarket: {len(all_results_polymarket)}")

    # List to store the flattened rows for each event
    flattened_data = []

    # Iterate over the list of events (dictionaries)
    for event in all_results_polymarket:
        # Get the base event info
        base_event_info = {
            'title': event.get('title', ''),
            'startDate': event.get('startDate', '')[:10],  # Truncate to YYYY-MM-DD
            'endDate': event.get('endDate', '')[:10]  # Truncate to YYYY-MM-DD
        }

        # If the event has 'markets', iterate through the list of market items
        if 'markets' in event:
            for market in event['markets']:
                # Extract the outcome prices (which is a string representing a list)
                outcome_prices_str = market.get('outcomePrices', '[]')

                # Safely evaluate the string to convert it into a list of strings
                try:
                    outcome_prices = ast.literal_eval(outcome_prices_str)
                except (ValueError, SyntaxError):
                    outcome_prices = []

                # Ensure we have two values in outcomePrices and convert them to floats
                if isinstance(outcome_prices, list) and len(outcome_prices) == 2:
                    try:
                        outcome_yes = float(outcome_prices[0])
                        outcome_no = float(outcome_prices[1])

                        # Truncate to 3 decimal places without rounding
                        outcome_yes = "{:.3f}".format(outcome_yes)
                        outcome_no = "{:.3f}".format(outcome_no)
                    except ValueError:
                        outcome_yes = "0.000"
                        outcome_no = "0.000"
                else:
                    outcome_yes = "0.000"
                    outcome_no = "0.000"

                # Create a new row with event info and market-specific info
                row = {
                    'title': base_event_info['title'],
                    'startDate': base_event_info['startDate'],
                    'endDate': base_event_info['endDate'],
                    'groupItemTitle': market.get('groupItemTitle') or "Yes/No",
                    'outcome_yes': outcome_yes,
                    'outcome_no': outcome_no
                }
                flattened_data.append(row)
        else:
            # If there are no markets, still add the base event info (without market details)
            flattened_data.append(base_event_info)

    # Convert the flattened data into a DataFrame
    df_polymarket = pd.DataFrame(flattened_data)

    df_polymarket_1 = df_polymarket.copy()
    # Now, for each group of 'title', 'startDate', 'endDate', we blank out the repeated fields
    df_polymarket_1[['title', 'startDate', 'endDate']] = df_polymarket_1[['title', 'startDate', 'endDate']].mask(df_polymarket_1[['title', 'startDate', 'endDate']].duplicated())

    return df_polymarket_1

