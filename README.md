# Futuur-Kalshi-Polymarket-API-data-Automation

This is my project for one of my clients to retrieve data from Futuur, Kalshi and Polymarket of different ongoing events and apply different automations based on matched titles in each of the Futuur, Kalshi and Polymarket


# Project Documentation

## Overview

This project involves extracting and processing data from multiple prediction markets platforms: Polymarket, Kalshi, and Futuur. The data is matched across these platforms based on similar titles, and automation processes are applied. The processed data is saved to an Excel file, with separate sheets for each data source, matching titles, and final results.

## Files Overview

### 1. **`main.py`**
   - This is the main script that coordinates the entire process. It schedules the data extraction and saving every 12 hours. It also runs the task immediately upon start and writes the results to an Excel file.
   - **Functions**:
     - `highlight_empty_rows`: Highlights empty rows in the final results.
     - `run_and_save_data`: Coordinates the data extraction from Polymarket, Kalshi, and Futuur, matches titles, and saves the results to an Excel file.
   
### 2. **`polymarket_data.py`**
   - Extracts and processes data from the Polymarket platform.
   - Uses Polymarket's API to gather the required event data.
   
### 3. **`kalshi_data.py`**
   - Extracts and processes data from the Kalshi platform.
   - Uses Kalshi's API to gather the required event data.
   
### 4. **`futuur_data.py`**
   - Extracts and processes data from the Futuur platform.
   - **Important**: Requires both public and private API keys to access the Futuur API. You can explore how to obtain these keys from the [Futuur API documentation](https://api.futuur.com/docs/).

### 5. **`matching_titles.py`**
   - Matches similar titles across the three platforms.
   - **Dependency**: Uses the `sentence-transformers` library to compute similarity scores between event titles.

### 6. **`automation.py`**
   - Applies automation logic based on the matched event titles across the platforms.
   
## Dependencies

To run this project, you need to install the following dependencies:

- **`pandas`**: For handling data manipulation and exporting data to Excel.
- **`schedule`**: For scheduling the periodic execution of the data extraction process.
- **`sentence-transformers`**: For computing similarity between event titles using pre-trained models from the Sentence Transformers library.
- **`requests`**: For making HTTP requests to the APIs of Polymarket, Kalshi, and Futuur.
- **`openai`**: If you are using OpenAI's GPT models for additional processing or generation tasks.
- **`xlsxwriter`**: For writing data to Excel files.

To install all dependencies, you can run:

```bash
pip install pandas schedule sentence-transformers requests openai xlsxwriter
```

### Notes for Futuur API Integration:
- The `futuur_data.py` file requires both public and private keys to interact with Futuur’s API.
- You can find the API documentation and instructions on how to get the keys at [Futuur API Documentation](https://api.futuur.com/docs/).

## File Execution Flow

1. **Start Script**: When `main.py` is executed, it runs the data extraction functions (`poly_market_data`, `kalshi_data_results`, `futuur_data_results`).
2. **Data Extraction**: 
   - Polymarket and Kalshi data is retrieved via their respective APIs.
   - Futuur data requires a valid API key and is fetched accordingly.
3. **Title Matching**: Titles from all three platforms are compared using the `find_similar_titles` function in `matching_titles.py`, utilizing the `sentence-transformers` model for similarity.
4. **Final Processing**: The `all_working` function in `automation.py` applies any required automation to the matched titles.
5. **Save Data**: The processed data is written to an Excel file, with separate sheets for each data source, matching titles, and final results.

## Configuration and Setup

1. **API Keys for Futuur**:
   - You will need to provide your Futuur API keys in the `futuur_data.py` file.
   - **Public Key**: For making requests.
   - **Private Key**: For authentication.
   - Refer to the Futuur API documentation to learn how to generate and set these keys.
   
2. **Running the Script**:
   - After configuring your API keys, you can run `main.py` directly to start the data extraction and automation process.
   - The script will run once immediately and then periodically every 12 hours, saving the results in an Excel file named by the current date (e.g., `20231219.xlsx`).

## Troubleshooting

- **Permission Error on Excel File**: If you encounter a "Permission Denied" error when trying to write to the Excel file, make sure the file is not open in Excel or any other program.
- **API Key Issues**: If you're having trouble with the Futuur API, double-check that you've set your public and private keys correctly and that they are valid.
```

