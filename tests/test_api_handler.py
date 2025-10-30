# Importera bibliotek
import requests
import pandas as pd

#  Sätt din Alpha Vantage API-nyckel här (demo för test)
ALPHA_VANTAGE_KEY = "demo"
EXCHANGE_API_URL = "https://api.exchangerate-api.com/v4/latest/"

#  Funktion för att hämta aktiedata från Alpha Vantage
def fetch_stock_data(symbol):
    """
    Hämtar historisk aktiedata från Alpha Vantage.
    Returnerar en Pandas DataFrame eller tom DataFrame om inget finns.
    """
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_KEY
    }

    r = requests.get(url, params=params)
    
    # Kontrollera om request lyckades
    if r.status_code != 200:
        return pd.DataFrame()

    data = r.json().get("Time Series (Daily)", {})

    # Om API:et inte returnerar data, returnera tom DataFrame
    if not data:
        return pd.DataFrame()

    # Konvertera JSON till DataFrame
    df = pd.DataFrame(data).T

    # Om DataFrame inte är tom, sätt kolumnnamn och typ
    if not df.empty:
        df.columns = ["Open", "High", "Low", "Close", "Volume"]
        df = df.astype(float)
        df.index.name = "Date"
        df.reset_index(inplace=True)

    return df


#  Funktion för att hämta valutakurser från ExchangeRate API
def fetch_currency_data(base_currency):
    """
    Hämtar valutakurser baserat på vald basvaluta.
    Returnerar Pandas DataFrame eller tom DataFrame om fel.
    """
    url = f"{EXCHANGE_API_URL}{base_currency}"

    r = requests.get(url)

    # Kontrollera status
    if r.status_code != 200:
        return pd.DataFrame()

    data = r.json().get("rates", {})

    # Om inga valutakurser returneras
    if not data:
        return pd.DataFrame()

    # Konvertera till DataFrame
    df = pd.DataFrame(list(data.items()), columns=["Currency", "Rate"])

    return df
