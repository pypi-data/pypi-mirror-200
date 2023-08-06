from feboun.download.main import download_all_data

from pathlib import Path

working_dir = Path.cwd()

data_dir = "/Volumes/Data 1/Developer/FE-Project/data/stocks/"
# List of stock tickers to download data for
us_stocks_tickers = ['M', 'NOK', 'AVTR', 'BCS', 'VTRS', 'XOM', 'DIDIY', 'ORCL', 'HAL', 'HST', 'XPEV', 'GM', 'PATH',
                     'CFG', 'FCX', 'BTG', 'BSX', 'NCLH', 'PACB', 'KEY', 'KMI', 'OSH', 'AAL', 'TFC', 'RF', 'APE', 'JPM',
                     'RUN', 'SHOP', 'KGC', 'U', 'KO', 'AGNC', 'ROKU', 'LYFT', 'UBER', 'JD', 'NABL', 'HBAN', 'GOLD',
                     'SIRI', 'USB', 'HPE', 'MQ', 'GRAB', 'CMCSA', 'COIN', 'C', 'SWN', 'AFRM', 'BUR', 'RIG', 'PFE',
                     'MPW', 'NU', 'WBD', 'PLUG', 'RLX', 'SQ', 'AMC', 'DNA', 'SNAP', 'LUMN', 'LCID', 'T', 'CSCO', 'VALE',
                     'BB', 'NYCB', 'META', 'PBR', 'CS', 'VZ', 'WFC', 'PLTR', 'ABEV', 'PCG', 'GOOG', 'BABA', 'MSFT',
                     'BBD', 'MU', 'NIO', 'RIVN', 'FRC', 'GOOGL', 'CCL', 'NVDA', 'SOFI', 'AUY', 'SCHW', 'AMZN', 'INTC',
                     'AMD', 'BAC', 'F', 'AI', 'AAPL', 'ITUB', 'TSLA']

# Call function to download historical data for all tickers
if __name__ == '__main__':
    tickers = us_stocks_tickers
    to_dir = data_dir
    download_all_data(tickers, to_dir)
