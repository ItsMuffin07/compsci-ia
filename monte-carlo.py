'''
Monte-Carlo simulation
'''
from pprint import *
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict

# stock = yf.Ticker("GOOGL")
# print()
# pprint(stock.info)

def monte_carlo(stock_symbol, years, num_simulations) -> Dict[str,float] | None:

    try:
        # Fetch historical stock data
        stock_data = yf.download(stock_symbol, period="max")

        # Calculate daily returns
        returns = stock_data['Adj Close'].pct_change()

        # Calculate mean and standard deviation of returns
        mean_return = returns.mean()
        std_return = returns.std()

        # Get the latest stock price
        last_price = stock_data['Adj Close'].iloc[-1]
    except:
        return None


    # Set the number of trading days in a year
    num_trading_days = 252

    # Create an array to store the simulation results
    simulation_results = np.zeros((num_trading_days * years, num_simulations))

    # Run the Monte Carlo simulation
    for i in range(num_simulations):
        # Initialize the price array with the last stock price
        price_series = np.zeros(num_trading_days * years)
        price_series[0] = last_price

        # Simulate the price for each trading day
        for j in range(1, num_trading_days * years):
            # Generate a random price change based on the mean and standard deviation of returns
            price_change = np.random.normal(mean_return, std_return)
            price_series[j] = price_series[j - 1] * (1 + price_change)

        # Store the simulated price series in the results array
        simulation_results[:, i] = price_series

    # Calculate the percentage change in stock price for each simulation
    percent_changes = (simulation_results[-1, :] - last_price) / last_price * 100

    # Plot the distribution of percentage changes
    plt.figure(figsize=(10, 6))
    plt.hist(percent_changes, bins=50, density=True, alpha=0.7)
    plt.xlabel('Percentage Change in Stock Price')
    plt.ylabel('Probability Density')
    plt.title(f'Distribution of Percentage Change in {stock_symbol} Stock Price ({years} Years)')
    plt.grid(True)
    plt.show()

    # Calculate percentage of simulations that have positive returns
    percent_positive_returns = float(100 * sum(1 for x in percent_changes if x > 0) / num_simulations)

    # Calculate and print the mean, median, and IQR of the percentage changes
    mean_percent_change = np.mean(percent_changes)
    median_percent_change = np.median(percent_changes)
    q1, q3 = np.percentile(percent_changes, [25, 75])
    iqr = q3 - q1

    print(f"Mean percentage change after {years} years: {mean_percent_change:.2f}%")
    print(f"Median percentage change after {years} years: {median_percent_change:.2f}%")
    print(f"Interquartile range (IQR) of percentage changes: {iqr:.2f}%")
    print(f"Percent of simulations with positive returns: {percent_positive_returns:.2f}%")
    data = {'mean_percent_change': mean_percent_change,
            'median_percent_change': median_percent_change,
            'iqr': iqr,
            'percent_positive_returns': percent_positive_returns}
    return data

# Example usage
stock_symbol = input("Enter the stock symbol: ")
years = int(input("Enter the number of years: "))
num_simulations = 1000  # Number of simulations to run

monte_carlo(stock_symbol, years, num_simulations)