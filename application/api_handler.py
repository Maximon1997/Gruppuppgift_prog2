
import requests
import pandas as pd
from dotenv import load_dotenv
import os


load_dotenv()   
# Sätt dina API-nycklar här (ersätt med egna om du har)
ALPHA_VANTAGE_KEY = os.getenv("api_nyckel") 
EXCHANGE_API_URL = "https://api.exchangerate-api.com/v4/latest/"

#  Funktion för att hämta aktiedata från Alpha Vantage
def fetch_stock_data(symbol):
    """
    Hämtar aktiedata (t.ex. AAPL) från Alpha Vantage API.
    Returnerar en Pandas DataFrame.
    """
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_KEY
    }

    # Skicka request till API
    r = requests.get(url, params=params)

    # Kontrollera om API-svaret är giltigt
    if r.status_code != 200:
        return pd.DataFrame()  # Returnera tom DataFrame vid fel

    data = r.json().get("Time Series (Daily)", {})

    # Konvertera JSON till DataFrame
    df = pd.DataFrame(data).T
    df.columns = ["Open", "High", "Low", "Close", "Volume"]

    # Ändra datatyper till numeriska värden
    df = df.astype(float)

    # Sortera efter datum (senaste överst)
    df.index.name = "Date"
    df.reset_index(inplace=True)

    return df


#  Funktion för att hämta valutakurser från ExchangeRate API
def fetch_currency_data(base_currency):
    """
    Hämtar valutakurser baserat på vald basvaluta (t.ex. USD).
    Returnerar en Pandas DataFrame.
    """
    url = f"{EXCHANGE_API_URL}{base_currency}"

    r = requests.get(url)

    # Om något går fel, returnera tom DataFrame
    if r.status_code != 200:
        return pd.DataFrame()

    data = r.json().get("rates", {})

    # Konvertera till DataFrame med två kolumner
    df = pd.DataFrame(list(data.items()), columns=["Currency", "Rate"])

    return df
