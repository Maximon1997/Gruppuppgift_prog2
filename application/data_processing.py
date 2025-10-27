import pandas as pd
import plotly.express as px

# Funktion för att bearbeta och kombinera data
def process_data(stock_df, currency_df):
    """
    Tar emot två DataFrames: en med aktiedata och en med valutakurser.
    Returnerar en bearbetad DataFrame som kan visas i tabellform.
    """

    # Om någon av DataFrames är tom, returnera en enkel fel-tabell
    if stock_df.empty or currency_df.empty:
        return pd.DataFrame({"Meddelande": ["Kunde inte hämta data från API."]})

    # Välj ut de viktigaste kolumnerna från aktiedatan
    df = stock_df[["Date", "Close"]].copy()

    # Konvertera valutakurs (t.ex. USD till SEK) om SEK finns i valutadata
    sek_rate = None
    if "SEK" in currency_df["Currency"].values:
        sek_rate = currency_df.loc[currency_df["Currency"] == "SEK", "Rate"].values[0]
        df["Close_SEK"] = df["Close"] * sek_rate
    else:
        df["Close_SEK"] = df["Close"]

    # Lägg till en kolumn för procentuell förändring per dag
    df["Förändring_%"] = df["Close_SEK"].pct_change() * 100

    # Sortera efter datum (senaste först)
    df = df.sort_values("Date", ascending=False)

    return df


# Funktion för att skapa ett Plotly-diagram
def create_plot(df):
    """
    Tar emot en DataFrame och returnerar ett interaktivt Plotly-diagram i HTML-format.
    """

    # Om DataFrame är tom, returnera en enkel text
    if df.empty or "Close_SEK" not in df.columns:
        return "<p>Ingen data att visa.</p>"

    # Skapa ett linjediagram över aktiekursen i SEK
    fig = px.line(df, x="Date", y="Close_SEK", title="Aktiekurs i SEK över tid")

    # Gör diagrammet mer kompakt för att passa på sidan
    fig.update_layout(height=400, margin=dict(l=40, r=40, t=40, b=40))

    # Returnera HTML som kan bäddas in i Jinja-template
    return fig.to_html(full_html=False)
