# feboun/web / app.py
# Created by azat at 3.04.2023
from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from io import StringIO
import yfinance as yf
import csv

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/download")
async def download(request: Request, ticker: str = Form(...)):
    print(f"Received request with ticker={ticker}")
    data = yf.download(ticker, start="2010-01-01")
    print(f"Downloaded data for ticker={ticker}")
    # Create a CSV file in memory
    csv_data = StringIO()
    writer = csv.writer(csv_data)
    writer.writerows(data.to_records())
    # Reset the buffer pointer to the beginning of the file
    csv_data.seek(0)
    # Generate the response object
    response = StreamingResponse(iter([csv_data.getvalue()]),
                                 media_type="text/csv",
                                 headers={"Content-Disposition":
                                              f"attachment; filename={ticker}.csv"})
    return response
