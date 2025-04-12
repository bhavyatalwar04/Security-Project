import pandas as pd
import numpy as np
import yfinance as yf

def calculate_beta_var(stock_symbol, market_symbol="^NSEI"):
    # Download stock and market data for 1 year
    try:
        stock_data = yf.download(stock_symbol, start="2024-03-28", end="2025-03-31")
        market_data = yf.download(market_symbol, start="2024-03-28", end="2025-03-31")
        
        # Check if data frames are empty
        if stock_data.empty or market_data.empty:
            print(f"❗ No data available for {stock_symbol} or market. Skipping...")
            print("-" * 50)
            return
            
        # Extract close prices
        stock_close = stock_data["Close"]
        market_close = market_data["Close"]
        
        # Make sure the dates align by creating a DataFrame with both series
        data_combined = pd.DataFrame()
        data_combined["Stock"] = stock_close
        data_combined["Market"] = market_close
        data_combined = data_combined.dropna()
        
        # Check if data is sufficient
        if len(data_combined) < 2:
            print(f"❗ Insufficient data for {stock_symbol}. Skipping...")
            print("-" * 50)
            return
            
        # Calculate daily returns and drop NaN values
        data_combined["Stock_Returns"] = data_combined["Stock"].pct_change()
        data_combined["Market_Returns"] = data_combined["Market"].pct_change()
        data_combined = data_combined.dropna(subset=["Stock_Returns", "Market_Returns"])
        
        # Check if data is sufficient after returns calculation
        if len(data_combined) < 2:
            print(f"❗ Not enough return data to calculate Beta and VaR for {stock_symbol}. Skipping...")
            print("-" * 50)
            return
            
        # Calculate Beta using covariance and variance
        cov_matrix = np.cov(data_combined["Stock_Returns"], data_combined["Market_Returns"])
        beta = cov_matrix[0, 1] / cov_matrix[1, 1]
        
        # Calculate Value-at-Risk (VaR) at 1% and 5% confidence levels
        var_1 = np.percentile(data_combined["Stock_Returns"], 1)  # 1% VaR
        var_5 = np.percentile(data_combined["Stock_Returns"], 5)  # 5% VaR
        
        # Extract the company name from the stock symbol
        company_name = stock_symbol.split(".")[0]
        
        # Print results
        print(f"✅ Results for {company_name}:")
        print(f"Beta: {beta:.4f}")
        print(f"1% VaR: {var_1 * 100:.2f}%")
        print(f"5% VaR: {var_5 * 100:.2f}%")
        print("-" * 50)
        
    except Exception as e:
        print(f"❗ Error processing {stock_symbol}: {e}")
        print("-" * 50)

# List of stock symbols to analyze
stock_symbols = [
    "NTPC.NS",
    "BAJFINANCE.NS",
    "ASHOKLEY.NS",
    "KOTAKBANK.NS",
    "INFY.NS"
]

# Loop through each stock and calculate Beta and VaR
for symbol in stock_symbols:
    calculate_beta_var(symbol)
