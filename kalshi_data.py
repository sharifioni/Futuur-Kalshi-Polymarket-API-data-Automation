import requests
import pandas as pd

def fetch_all_events():
    all_events_kalshi = []
    url = "https://api.elections.kalshi.com/trade-api/v2/events"

    # Parameters for the initial request
    params = {
        "with_nested_markets": "true",
        "status": "open",  # Modify this if you want to fetch other statuses
        "limit": 200  # Maximum limit allowed by the API
    }

    while True:
        # Make the API request
        r = requests.get(url, params=params)
        response = r.json()

        # Check if the response contains events
        if 'events' in response:
            all_events_kalshi.extend(response['events'])
        else:
            break

        # Get the cursor for the next page, if it exists
        cursor = response.get('cursor', None)

        # If there's no cursor, we've fetched all pages
        if not cursor:
            break

        # Update the parameters to fetch the next page using the cursor
        params['cursor'] = cursor

    return all_events_kalshi




def kalshi_data_results():
    # Fetch all events
    all_events_kalshi = fetch_all_events()

    # Print total number of events fetched
    print(f"Total events fetched from kalshi: {len(all_events_kalshi)}")
    # List to store the extracted data
    flattened_data = []

    # Used to track the last processed event title
    last_event_title = None

    # Loop through each dictionary in the data
    for event in all_events_kalshi:
        # Extract event title
        event_title = event.get('title', '')

        # Determine whether to display the event info
        display_event_info = (event_title != last_event_title)

        # Update last processed event title
        last_event_title = event_title

        # Extract the markets information
        for market in event.get('markets', []):
            # Extract and convert the outcome values, default to '0' if missing
            outcome_yes_str = market.get('yes_ask', '0')
            outcome_no_str = market.get('no_ask', '0')

            # Convert to float, divide by 100, and round to 3 decimal places
            try:
                outcome_yes = round(float(outcome_yes_str) / 100, 3)
            except ValueError:
                outcome_yes = 0.000

            try:
                outcome_no = round(float(outcome_no_str) / 100, 3)
            except ValueError:
                outcome_no = 0.000

            # Format dates to 'YYYY-MM-DD'
            start_date = pd.to_datetime(market.get('open_time', '')).strftime('%Y-%m-%d') if market.get('open_time', '') else ''
            end_date = pd.to_datetime(market.get('close_time', '')).strftime('%Y-%m-%d') if market.get('close_time', '') else ''

            # Create a dictionary for each market with the required information
            row = {
                'title': event_title if display_event_info else '',
                'startDate': start_date if display_event_info else '',
                'endDate': end_date if display_event_info else '',
                'groupItemTitle': market.get('subtitle') or "Yes/No",
                'outcome_yes': outcome_yes,
                'outcome_no': outcome_no
            }

            # Append to the flattened data list
            flattened_data.append(row)

            # After the first market, don't display event info for this event again
            display_event_info = False

    # Convert the list of dictionaries into a DataFrame
    df_kalshi_1 = pd.DataFrame(flattened_data)

    # Assuming df_kalshi_1 is your final dataframe
    df_kalshi_1['outcome_yes'] = df_kalshi_1['outcome_yes'].apply(lambda x: f"{x:.3f}")
    df_kalshi_1['outcome_no'] = df_kalshi_1['outcome_no'].apply(lambda x: f"{x:.3f}")

    return df_kalshi_1


