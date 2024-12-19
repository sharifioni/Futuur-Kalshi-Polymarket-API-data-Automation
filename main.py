import pandas as pd
import schedule
import time
from datetime import datetime
from polymarket_data import poly_market_data
from kalshi_data import kalshi_data_results
from futuur_data import futuur_data_results
from matching_titles import find_similar_titles
from automation import all_working
import os


# Initialize the global variable to track the task's running status
is_running = False

def highlight_empty_rows(row):
    # Check if all values in the row are either empty string or NaN
    is_empty = row.apply(lambda x: x == '' or pd.isna(x))
    if is_empty.all():
        return ['background-color: yellow'] * len(row)
    else:
        return [''] * len(row)
    
# Function to run the whole process
def run_and_save_data():
    global is_running
    
    if not is_running:
        is_running = True
        try:
            # Get the current date in the format YYYYMMDD
            current_date = datetime.now().strftime("%Y%m%d")
            file_name = f'{current_date}.xlsx'
            
            # Check if the file exists; if not, create a new one for the new day
            if not os.path.exists(file_name):
                print(f"Creating new file for the day: {file_name}")
            
            # Run your data gathering and processing functions
            polymarket_dataframe = poly_market_data()
            kalshi_dataframe = kalshi_data_results()
            futuur_dataframe = futuur_data_results()
            matching_titles = find_similar_titles(polymarket_dataframe, futuur_dataframe, kalshi_dataframe)
            final_results = all_working(futuur_dataframe, polymarket_dataframe, kalshi_dataframe, matching_titles)
            final_results = final_results.style.apply(highlight_empty_rows, axis=1)
            
            # Create a Pandas Excel writer object, overwrite the existing file
            try:
                with pd.ExcelWriter(file_name, engine='xlsxwriter', mode='w') as writer:
                    # Write each DataFrame to a different sheet
                    polymarket_dataframe.to_excel(writer, sheet_name='Polymarket Data', index=False)
                    kalshi_dataframe.to_excel(writer, sheet_name='Kalshi Data', index=False)
                    futuur_dataframe.to_excel(writer, sheet_name='Futuur Data', index=False)
                    matching_titles.to_excel(writer, sheet_name='Matching Titles', index=False)
                    final_results.to_excel(writer, sheet_name='Final Results', index=False)
                print(f"DataFrames have been written to '{file_name}'")
            except PermissionError:
                print(f"Permission denied: Unable to write to {file_name}. Please make sure the file is not open.")
        
        except Exception as e:
            print(f"An error occurred: {e}")
        
        finally:
            # Set is_running to False to allow the next execution
            is_running = False
    else:
        print("Task is already running, waiting for the next cycle.")

# Schedule the job to run hours
schedule.every(12).hours.do(run_and_save_data)

# Run the task immediately once when the script starts
run_and_save_data()

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
