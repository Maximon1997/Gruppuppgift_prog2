

from flask import Flask, render_template, request, make_response
import json
try:
    # när appen körs som paket (pytest, python -m)
    from application.api_handler import fetch_currency_data, fetch_stock_data, fetch_top_gainers_losers
    from application.data_processing import process_data, create_plot
except ImportError:
    # när du kör Flask direkt i application/
    from api_handler import fetch_currency_data, fetch_stock_data, fetch_top_gainers_losers
    from data_processing import process_data, create_plot
app = Flask(__name__)

# Startsidan (visar sökformuläret)
@app.route('/')
def index():
    """Startsidan visar sökformulär + Top Gainers/Losers."""

    # Minns tidigare sökning
    last_search = request.cookies.get('last_search')
    form_data = json.loads(last_search) if last_search else {}

    # Hämta data via api_handler
    gainers_df, losers_df = fetch_top_gainers_losers()

    # Om vi fick data, gör HTML-tabeller med färg
    def make_table(df, color_class):
        if df.empty:
            return "<p>Ingen data att visa just nu.</p>"
        df["Förändring %"] = df["Förändring %"].apply(
    lambda x: f"<span class='{color_class}'>{x}</span>"
)
        return df.head(20).to_html(classes=f"table {color_class}-table", index=False, escape=False)

    gainers_table = make_table(gainers_df, "positive")
    losers_table = make_table(losers_df, "negative")

    return render_template(
        "index.html",
        form_data=form_data,
        gainers_table=gainers_table,
        losers_table=losers_table
    )


# Resultatsidan (visar tabeller och diagram)
@app.route('/results', methods=['POST'])
def results():
    # Hämta data från formuläret
    stock_symbol = request.form.get('stock')
    base_currency = request.form.get('currency')

    # Hämta data från båda API:erna
    stock_df = fetch_stock_data(stock_symbol)
    currency_df = fetch_currency_data(base_currency)

    # Bearbeta data med hjälp av Pandas
    result_df = process_data(stock_df, currency_df)

    # Skapa ett diagram med Plotly
    chart_html = create_plot(result_df)

    # Skapa svaret och spara senaste sökningen i en cookie
    resp = make_response(render_template('results.html',
                                         tables=[result_df.to_html(classes='table')],
                                         chart=chart_html))
    resp.set_cookie('last_search', json.dumps(request.form), max_age=3600)
    return resp

# Felhantering för 404 (sida hittas ej)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

# Starta Flask-applikationen
if __name__ == '__main__':
    app.run(debug=True)
