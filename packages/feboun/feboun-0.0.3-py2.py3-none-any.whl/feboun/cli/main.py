import typer
from pathlib import Path
import typer
import yfinance as yf
import pandas as pd
from datetime import datetime


app = typer.Typer()


@app.command()
def debug():
    cwd = Path.cwd()
    data_dir = cwd / "data"
    if not data_dir.exists():
        data_dir.mkdir()
        print(f"Data dir: '{data_dir}' has been created.")
    else:
        print(f"The folder '{data_dir}' already exists, skipping creation.")
    typer.echo(f"Working from {cwd}")


@app.command()
def download(ticker: str, start_date: str, end_date: str = datetime.today().strftime('%Y-%m-%d'), output_dir: str = "data"):
    """
    Download daily stock data for the specified ticker and save as CSV.
    """
    # Download stock data
    stock_data = yf.download(ticker, start_date, end_date)

    # Save to CSV file
    output_file = Path(output_dir) / f"{ticker}.csv"
    stock_data.to_csv(output_file)
    typer.echo(f"Stock data saved to {output_file}")


if __name__ == "__main__":
    app()
