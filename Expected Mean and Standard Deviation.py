# Import required libraries
import pandas as pd
import numpy as np

# Define a function to calculate expected return and standard deviation
def calculate_stock_metrics(file_path):
    # Print the file being processed for debugging
    print(f"Processing file: {file_path}")

    # Load stock data from the provided file path
    stock_data = pd.read_csv(file_path)

    # Clean column names (remove trailing spaces)
    stock_data.columns = stock_data.columns.str.strip()

    # Convert 'Date' column to datetime format and sort the data
    stock_data['Date'] = pd.to_datetime(stock_data['Date'], format="%d-%b-%Y")
    stock_data = stock_data.sort_values(by='Date')

    # Convert 'close' to numeric and handle errors
    stock_data['close'] = stock_data['close'].astype(str).str.replace(',', '', regex=True).astype(float)


    # Fill missing or invalid values in 'close' using forward fill
    stock_data['close'] = stock_data['close'].ffill()

    # Calculate daily returns and drop NaN values
    stock_data['Returns'] = stock_data['close'].pct_change(fill_method=None)
    stock_data = stock_data.dropna(subset=['Returns'])

    # Calculate expected return and standard deviation (annualized)
    expected_return = stock_data['Returns'].mean() * 252
    std_dev = stock_data['Returns'].std() * np.sqrt(252)

    # Extract the company name from the file name
    company_name = file_path.split('/')[-1].replace('.csv', '')

    # Print results
    print(f"Results for {company_name}:")
    print(f"Expected Annual Return: {expected_return * 100:.2f}%")
    print(f"Annualized Standard Deviation: {std_dev * 100:.2f}%")
    print("-" * 50)

# Example usage with different files
file_paths = [
    "C:/Users/acer/OneDrive/Desktop/VS FILES/market/NTPC.csv",
    "C:/Users/acer/OneDrive/Desktop/VS FILES/market/BAJFINANCE.csv",
    "C:/Users/acer/OneDrive/Desktop/VS FILES/market/KOTAKBANK.csv",
    "C:/Users/acer/OneDrive/Desktop/VS FILES/market/INFY.csv",
    "C:/Users/acer/OneDrive/Desktop/VS FILES/market/Ashokley.csv"
]

# Loop through each file and calculate metrics
for file in file_paths:
    calculate_stock_metrics(file)
