# feboun/download / main.py
# Created by azat at 3.04.2023
from datetime import datetime
from pathlib import Path
import yfinance as yf
import pandas as pd
import multiprocessing as mp


# Define function to download historical data for a single stock ticker
def download_data(ticker: str, to_dir: Path | str):
    data = yf.download(ticker, start="2010-01-01", end=datetime.today().strftime('%Y-%m-%d'))
    working_dir = Path(to_dir)
    # Save to CSV file
    file_path = working_dir / f"{ticker}.csv"
    data.to_csv(file_path)


# Define function to download historical data for all tickers in parallel
def download_all_data(tickers, to_dir):
    with mp.Pool(processes=mp.cpu_count()) as pool:
        pool.starmap(download_data, [(ticker, to_dir) for ticker in tickers])
