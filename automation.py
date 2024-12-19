import pandas as pd
from datetime import datetime

# Assuming df1 is Futuur, df2 is Polymarket, and df3 is Kalshi
# Assuming df3_match is the dataframe that matches semantically similar titles

#df1 = df_futuur
#df2 = df_polymarket_1
#df3 = df_kalshi_1
#df3_match = similar_titles_df

# Define today's date to calculate 'Days Until End Date'
today = pd.to_datetime(datetime.today())

# Initialize an empty list to store the resulting rows
result_list = []

# Function to calculate 'Days Until End Date'
def calculate_days_until_end(end_date):
    return (pd.to_datetime(end_date) - today).days if pd.notna(end_date) else None

def matched_outcomes(poly_data_list, futuur_data_list, kalshi_data_list):
    Matched_data = []
    
    # Create a set of outcomes that have already been matched
    matched_outcomes_set = set()
    
    help_dict = {'Matched Outcome': '', 'Lowest Yes': '', 'Lowest No': '',
                 '1 minus Yes plus No': '', 'D/End_Date': '', 'min_day': ''}

    # Prepare lists for outcomes, yes/no prices, and days until end date
    poly_outcomes = [data.get('Poly Outcomes', '') for data in poly_data_list]
    futuur_outcomes = [data.get('Futuur Outcomes', '') for data in futuur_data_list]
    kalshi_outcomes = [data.get('Kalshi Outcomes', '') for data in kalshi_data_list]

    # Iterate through Poly outcomes and match with Futuur and Kalshi
    if poly_outcomes and futuur_outcomes and kalshi_outcomes:
        for value in poly_outcomes:
            # Only match if the value hasn't been matched already
            if value in futuur_outcomes and value in kalshi_outcomes and value not in matched_outcomes_set:
                help_dict['Matched Outcome'] = value

                # Get Poly YES, NO values
                poly_yes, poly_no = next((data.get('Poly YES', '0') or '0', data.get('Poly NO', '0') or '0') \
                                        for data in poly_data_list if data.get('Poly Outcomes') == value)

                # Get Futuur YES, NO values
                futuur_yes, futuur_no = next((data.get('Futuur YES', '0') or '0', data.get('Futuur NO', 1) or 1) \
                                            for data in futuur_data_list if data.get('Futuur Outcomes') == value)

                # Get Kalshi YES, NO values
                kalshi_yes, kalshi_no = next((data.get('Kalshi YES', '0') or '0', data.get('Kalshi NO', '0') or '0') \
                                            for data in kalshi_data_list if data.get('Kalshi Outcomes') == value)

                # Get Poly, Futuur, Kalshi Days until End Date
                poly_days = poly_data_list[0].get('Poly Days until End Date', '0')
                futuur_days = futuur_data_list[0].get('Futuur Days until End Date', '0')
                kalshi_days = kalshi_data_list[0].get('Kalshi Days until End Date', '0')

                # Calculate Lowest Yes and Lowest No
                help_dict['Lowest Yes'] = min(float(poly_yes), float(futuur_yes), float(kalshi_yes))
                help_dict['Lowest No'] = min(float(poly_no), float(futuur_no), float(kalshi_no))

                # Calculate 1 - (Yes + No)
                help_dict['1 minus Yes plus No'] = 1 - (help_dict['Lowest Yes'] + help_dict['Lowest No'])
                help_dict['min_day'] = min(int(poly_days), int(futuur_days), int(kalshi_days))

                # Calculate D/End_Date if applicable
                if help_dict['1 minus Yes plus No'] > 0:
                    # Ensure no division by zero
                    if int(poly_days) != 0 and int(futuur_days) != 0 and int(kalshi_days) != 0:
                        help_dict['D/End_Date'] = help_dict['1 minus Yes plus No'] / \
                                                  min(int(poly_days), int(futuur_days), int(kalshi_days))
                    else:
                        help_dict['D/End_Date'] = 0
                else:
                    help_dict['D/End_Date'] = 0

                # Append the result to Matched_data
                Matched_data.append(help_dict.copy())

                # Add the matched outcome to the set
                matched_outcomes_set.add(value)

    # Matching between Poly and Futuur only
    if poly_outcomes and futuur_outcomes:
        for value in poly_outcomes:
            if value in futuur_outcomes and value not in matched_outcomes_set:
                help_dict['Matched Outcome'] = value

                poly_yes, poly_no = next((data.get('Poly YES','0') or '0', data.get('Poly NO', '0') or '0') \
                                         for data in poly_data_list if data.get('Poly Outcomes') == value)
                futuur_yes, futuur_no = next((data.get('Futuur YES', '0') or '0', data.get('Futuur NO',1) or 1) \
                                             for data in futuur_data_list if data.get('Futuur Outcomes') == value)
                poly_days = poly_data_list[0].get('Poly Days until End Date', '0')
                futuur_days = futuur_data_list[0].get('Futuur Days until End Date', '0')

                help_dict['Lowest Yes'] = min(float(poly_yes), float(futuur_yes))
                help_dict['Lowest No'] = min(float(poly_no), float(futuur_no))
                help_dict['1 minus Yes plus No'] = 1 - (help_dict['Lowest Yes'] + help_dict['Lowest No'])
                
                help_dict['min_day'] = min(int(poly_days), int(futuur_days))

                if help_dict['1 minus Yes plus No'] > 0:
                    if int(poly_days) != 0 and int(futuur_days) != 0:
                        help_dict['D/End_Date'] = help_dict['1 minus Yes plus No'] / \
                        min(int(poly_days), int(futuur_days))
                    else:
                        help_dict['D/End_Date'] = 0
                else:
                    help_dict['D/End_Date'] = 0

                Matched_data.append(help_dict.copy())
                matched_outcomes_set.add(value)

    # Matching between Poly and Kalshi only
    if poly_outcomes and kalshi_outcomes:
        for value in poly_outcomes:
            if value in kalshi_outcomes and value not in matched_outcomes_set:
                help_dict['Matched Outcome'] = value

                # Get Poly YES, NO values
                poly_yes, poly_no = next((data.get('Poly YES', '0') or '0', data.get('Poly NO', '0') or '0') \
                                        for data in poly_data_list if data.get('Poly Outcomes') == value)

                # Get Kalshi YES, NO values
                kalshi_yes, kalshi_no = next((data.get('Kalshi YES', '0') or '0', data.get('Kalshi NO', '0') or '0') \
                                            for data in kalshi_data_list if data.get('Kalshi Outcomes') == value)

                # Get Poly, Kalshi Days until End Date
                poly_days = poly_data_list[0].get('Poly Days until End Date', '0')  
                kalshi_days = kalshi_data_list[0].get('Kalshi Days until End Date', '0')

                # Calculate Lowest Yes and Lowest No
                help_dict['Lowest Yes'] = min(float(poly_yes), float(kalshi_yes))
                help_dict['Lowest No'] = min(float(poly_no), float(kalshi_no))

                # Calculate 1 - (Yes + No)
                help_dict['1 minus Yes plus No'] = 1 - (help_dict['Lowest Yes'] + help_dict['Lowest No'])
                help_dict['min_day'] = min(int(poly_days), int(kalshi_days))
                
                # Calculate D/End_Date if applicable
                if help_dict['1 minus Yes plus No'] > 0:
                    # Ensure no division by zero
                    if int(poly_days) != 0  and int(kalshi_days) != 0:
                        help_dict['D/End_Date'] = help_dict['1 minus Yes plus No'] / \
                                                  min(int(poly_days), int(kalshi_days))
                    else:
                        help_dict['D/End_Date'] = 0
                else:
                    help_dict['D/End_Date'] = 0

                # Append the result to Matched_data
                Matched_data.append(help_dict.copy())
                matched_outcomes_set.add(value)

    # Matching between Futuur and Kalshi only
    if futuur_outcomes and kalshi_outcomes:
        for value in futuur_outcomes:
            if value in kalshi_outcomes and value not in matched_outcomes_set:
                help_dict['Matched Outcome'] = value

                futuur_yes, futuur_no = next((data.get('Futuur YES', '0') or '0', data.get('Futuur NO', 1) or 1) \
                            for data in futuur_data_list if data.get('Futuur Outcomes') == value)

                # Get Kalshi YES, NO values
                kalshi_yes, kalshi_no = next((data.get('Kalshi YES', '0') or '0', data.get('Kalshi NO', '0') or '0') \
                                            for data in kalshi_data_list if data.get('Kalshi Outcomes') == value)

                # Get Futuur, Kalshi Days until End Date
                futuur_days = futuur_data_list[0].get('Futuur Days until End Date', '0')
                kalshi_days = kalshi_data_list[0].get('Kalshi Days until End Date', '0')

                # Calculate Lowest Yes and Lowest No
                help_dict['Lowest Yes'] = min(float(futuur_yes), float(kalshi_yes))
                help_dict['Lowest No'] = min(float(futuur_no), float(kalshi_no))

                # Calculate 1 - (Yes + No)
                help_dict['1 minus Yes plus No'] = 1 - (help_dict['Lowest Yes'] + help_dict['Lowest No'])
                help_dict['min_day'] = min(int(futuur_days), int(kalshi_days))

                # Calculate D/End_Date if applicable
                if help_dict['1 minus Yes plus No'] > 0:
                    # Ensure no division by zero
                    if int(futuur_days) != 0 and int(kalshi_days) != 0:
                        help_dict['D/End_Date'] = help_dict['1 minus Yes plus No'] / \
                                                  min(int(futuur_days), int(kalshi_days))
                    else:
                        help_dict['D/End_Date'] = 0
                else:
                    help_dict['D/End_Date'] = 0

                # Append the result to Matched_data
                Matched_data.append(help_dict.copy())
                matched_outcomes_set.add(value)

    # Final checks to return Matched_data
    if Matched_data:
        return Matched_data
    else:
        # If no matches were found, return an empty help_dict
        Matched_data.append(help_dict.copy())
        return Matched_data



def yes_no_rows(matched_data):
    help_dict = {'Matched Outcome': '', 'Lowest Yes': '', 'Lowest No': '',
                 '1 minus Yes plus No': '', 'D/End_Date': '', 'min_day': ''}

    help_dict['Matched Outcome'] = 'TOTAL YES'
    help_dict['Lowest Yes'] = sum(float(data['Lowest Yes']) for data in matched_data)
    help_dict['Lowest No'] = 0.00
    help_dict['1 minus Yes plus No'] = 1 - help_dict['Lowest Yes']
    help_dict['min_day'] = min(data['min_day'] for data in matched_data)
    #print(matched_data)
    #print(help_dict['min_day'])
    if help_dict['1 minus Yes plus No'] > 0:
        if help_dict['min_day'] != 0:
            help_dict['D/End_Date'] = help_dict['1 minus Yes plus No'] / help_dict['min_day']
        else:
            help_dict['D/End_Date'] = 0
    else:
        help_dict['D/End_Date'] = 0
    matched_data.append(help_dict)

    help_dict = {'Matched Outcome': '', 'Lowest Yes': '', 'Lowest No': '',
                 '1 minus Yes plus No': '', 'D/End_Date': '', 'min_day': ''}
    help_dict['Matched Outcome'] = 'TOTAL NO'
    help_dict['Lowest Yes'] = 0.00
    help_dict['Lowest No'] = sum(float(data['Lowest No']) for data in matched_data)
    help_dict['1 minus Yes plus No'] = 1 - help_dict['Lowest No']
    help_dict['min_day'] = min(data['min_day'] for data in matched_data)
    if help_dict['1 minus Yes plus No'] > 0:
        if help_dict['min_day'] != 0:
            help_dict['D/End_Date'] = help_dict['1 minus Yes plus No'] / help_dict['min_day']
        else:
            help_dict['D/End_Date'] = 0
    else:
        help_dict['D/End_Date'] = 0
    matched_data.append(help_dict)

    return matched_data

def all_working(df1, df2, df3, df3_match):

    # Iterate through each row of the match dataframe
    for index, row in df3_match.iterrows():
        # Initialize dictionaries and lists to store values for Polymarket, Futuur, and Kalshi
        poly_data = {}
        futuur_data = {}
        kalshi_data = {}
        poly_list = []
        futuur_list = []
        kalshi_list = []
        combined_list = []

        # Polymarket logic (same as before)
        if row['Polymarket'] != '':
            poly_title = row['Polymarket']

            # Start collecting from the first match of the title
            start_collecting = False
            for i, poly_row in df2.iterrows():
                if pd.notna(poly_row['title']) and poly_row['title'] == poly_title:
                    start_collecting = True
                    poly_data = {
                        'Poly Title': poly_row['title'],
                        'Poly Start Date': poly_row['startDate'],
                        'Poly End Date': poly_row['endDate'],
                        'Poly Days until End Date': calculate_days_until_end(poly_row['endDate']),
                        'Poly Outcomes': poly_row['groupItemTitle'],
                        'Poly YES': poly_row['outcome_yes'],
                        'Poly NO': poly_row['outcome_no']
                    }
                    poly_list.append(poly_data)
                    continue

                if start_collecting and pd.notna(poly_row['title']) and poly_row['title'] != poly_title:
                    break  # Stop collecting when a new title is found

                if start_collecting:
                    poly_data = {
                        'Poly Title': poly_row['title'] if pd.notna(poly_row['title']) else '',
                        'Poly Start Date': poly_row['startDate'] if pd.notna(poly_row['startDate']) else '',
                        'Poly End Date': poly_row['endDate'] if pd.notna(poly_row['endDate']) else '',
                        'Poly Days until End Date': calculate_days_until_end(poly_row['endDate']),
                        'Poly Outcomes': poly_row['groupItemTitle'] if pd.notna(poly_row['groupItemTitle']) else '',
                        'Poly YES': poly_row['outcome_yes'] if pd.notna(poly_row['outcome_yes']) else '',
                        'Poly NO': poly_row['outcome_no'] if pd.notna(poly_row['outcome_no']) else ''
                    }
                    poly_list.append(poly_data)

        # Futuur logic (converted similarly to Polymarket)
        if row['Futuur'] != '':
            futuur_title = row['Futuur']
            

            start_collecting = False
            for i, futuur_row in df1.iterrows():
                if pd.notna(futuur_row['title']) and futuur_row['title'] == futuur_title:
                    start_collecting = True
                    value = ''
                    if futuur_row['groupItemTitle'] == 'Democratic':
                        value = 'Democrat'
                    elif futuur_row['groupItemTitle'] == 'Tie':
                        value = 'Draw'
                    else:
                        value = futuur_row['groupItemTitle']
                    futuur_data = {
                        'Futuur Title': futuur_row['title'],
                        'Futuur Start Date': futuur_row['startDate'],
                        'Futuur End Date': futuur_row['endDate'],
                        'Futuur Days until End Date': calculate_days_until_end(futuur_row['endDate']),
                        'Futuur Outcomes': value,
                        'Futuur YES': futuur_row['outcome_yes'],
                        'Futuur NO': futuur_row['outcome_no']
                    }
                    futuur_list.append(futuur_data)

                    continue

                if start_collecting and futuur_row['title']!='' and futuur_row['title'] != futuur_title:
                    #print("Hello")
                    #print(futuur_row['title'], futuur_title)
                    break

                if start_collecting:
                    value = ''
                    if futuur_row['groupItemTitle'] == 'Democratic':
                        value = 'Democrat'
                    elif futuur_row['groupItemTitle'] == 'Tie':
                        value = 'Draw'
                    else:
                        value = futuur_row['groupItemTitle']
                    futuur_data = {
                        'Futuur Title': futuur_row['title'] if pd.notna(futuur_row['title']) else '',
                        'Futuur Start Date': futuur_row['startDate'] if pd.notna(futuur_row['startDate']) else '',
                        'Futuur End Date': futuur_row['endDate'] if pd.notna(futuur_row['endDate']) else '',
                        'Futuur Days until End Date': calculate_days_until_end(futuur_row['endDate']) if pd.notna(futuur_row['endDate']) and futuur_row['endDate'] != '' else '',
                        'Futuur Outcomes': value,
                        'Futuur YES': futuur_row['outcome_yes'] if pd.notna(futuur_row['outcome_yes']) else '',
                        'Futuur NO': futuur_row['outcome_no'] if pd.notna(futuur_row['outcome_no']) else ''
                    }
                    futuur_list.append(futuur_data)

        # Kalshi logic (converted similarly to Polymarket)
        if row['Kalshi'] != '':
            kalshi_title = row['Kalshi']

            start_collecting = False
            for i, kalshi_row in df3.iterrows():
                if pd.notna(kalshi_row['title']) and kalshi_row['title'] == kalshi_title:
                    start_collecting = True
                    kalshi_data = {
                        'Kalshi Title': kalshi_row['title'],
                        'Kalshi Start Date': kalshi_row['startDate'],
                        'Kalshi End Date': kalshi_row['endDate'],
                        'Kalshi Days until End Date': calculate_days_until_end(kalshi_row['endDate']),
                        'Kalshi Outcomes': kalshi_row['groupItemTitle'],
                        'Kalshi YES': kalshi_row['outcome_yes'],
                        'Kalshi NO': kalshi_row['outcome_no']
                    }
                    kalshi_list.append(kalshi_data)
                    continue

                if start_collecting and kalshi_row['title']!='' and kalshi_row['title'] != kalshi_title:
                    break

                if start_collecting:
                    kalshi_data = {
                        'Kalshi Title': kalshi_row['title'] if pd.notna(kalshi_row['title']) else '',
                        'Kalshi Start Date': kalshi_row['startDate'] if pd.notna(kalshi_row['startDate']) else '',
                        'Kalshi End Date': kalshi_row['endDate'] if pd.notna(kalshi_row['endDate']) else '',
                        'Kalshi Days until End Date': calculate_days_until_end(kalshi_row['endDate']) if pd.notna(kalshi_row['endDate']) and kalshi_row['endDate'] != '' else '',
                        'Kalshi Outcomes': kalshi_row['groupItemTitle'] if pd.notna(kalshi_row['groupItemTitle']) else '',
                        'Kalshi YES': kalshi_row['outcome_yes'] if pd.notna(kalshi_row['outcome_yes']) else '',
                        'Kalshi NO': kalshi_row['outcome_no'] if pd.notna(kalshi_row['outcome_no']) else ''
                    }
                    kalshi_list.append(kalshi_data)
                    

        # Combine the data for the row, handling cases where one or more data sources are empty
        combined_data = [
            poly_list,
            futuur_list,
            kalshi_list
        ]

        # Append to the result list
        result_list.append(combined_data)

    # Convert the result list into a DataFrame
    final_df = pd.DataFrame(result_list)


    # Define the column names for the output DataFrame
    columns = [
        'Matched Outcome','Lowest Yes','Lowest No','1 minus Yes plus No','Poly Title', 'Poly Start Date', 'Poly End Date', 'Poly Outcomes', 'Poly YES', 'Poly NO',
        'Futuur Title', 'Futuur Start Date', 'Futuur End Date', 'Futuur Outcomes', 'Futuur YES', 'Futuur NO',
        'Kalshi Title', 'Kalshi Start Date', 'Kalshi End Date', 'Kalshi Outcomes', 'Kalshi YES', 'Kalshi NO'
    ]

    # Initialize an empty list to store the final data
    final_data = []




    # Iterate over each row in the DataFrame
    for index, row in final_df.iterrows():
        poly_data_list = row[0]  # Assuming Poly data is the first column
        futuur_data_list = row[1]  # Assuming Futuur data is the second column
        kalshi_data_list = row[2]  # Assuming Kalshi data is the third column

        matched_data = matched_outcomes(poly_data_list, futuur_data_list, kalshi_data_list)

        if matched_data != None:
            if matched_data[0]['Matched Outcome']:
                matched_data = yes_no_rows(matched_data)


        # Determine the maximum number of entries for Poly, Futuur, and Kalshi
        if matched_data != None:
            max_len = max(len(poly_data_list), len(futuur_data_list), len(kalshi_data_list), len(matched_data))
        else:
            max_len = max(len(poly_data_list), len(futuur_data_list), len(kalshi_data_list))


        # Iterate over each list, processing up to the maximum number of entries
        for i in range(max_len):
            poly_data = poly_data_list[i] if i < len(poly_data_list) else {}
            futuur_data = futuur_data_list[i] if i < len(futuur_data_list) else {}
            kalshi_data = kalshi_data_list[i] if i < len(kalshi_data_list) else {}
            match_data = matched_data[i] if i < len(matched_data) else {}

            # Append data to the final list, filling missing values with empty strings
            final_data.append([
                match_data.get('Matched Outcome', ''),
                match_data.get('Lowest Yes', ''),
                match_data.get('Lowest No', ''),
                match_data.get('1 minus Yes plus No', ''),
                poly_data.get('Poly Title', ''),
                poly_data.get('Poly Start Date', ''),
                poly_data.get('Poly End Date', ''),
                poly_data.get('Poly Outcomes', ''),
                poly_data.get('Poly YES', ''),
                poly_data.get('Poly NO', ''),
                futuur_data.get('Futuur Title', ''),
                futuur_data.get('Futuur Start Date', ''),
                futuur_data.get('Futuur End Date', ''),
                futuur_data.get('Futuur Outcomes', ''),
                futuur_data.get('Futuur YES', ''),
                futuur_data.get('Futuur NO', ''),
                kalshi_data.get('Kalshi Title', ''),
                kalshi_data.get('Kalshi Start Date', ''),
                kalshi_data.get('Kalshi End Date', ''),
                kalshi_data.get('Kalshi Outcomes', ''),
                kalshi_data.get('Kalshi YES', ''),
                kalshi_data.get('Kalshi NO', '')
            ])
        final_data.append([])

    # Create a DataFrame with the processed data
    final_df_1 = pd.DataFrame(final_data, columns=columns)

    return final_df_1