#import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
#url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
#r = requests.get(url)
#data = r.json()

#print(data)



from flask import Flask, render_template, request, make_response
import json
from api_handler import fetch_currency_data, fetch_stock_data
from data_processing import process_data, create_plot

app = Flask(__name__)

# Startsidan (visar sökformuläret)
@app.route('/')
def index():
    # Försök läsa tidigare sökning från cookie
    last_search = request.cookies.get('last_search')
    form_data = json.loads(last_search) if last_search else {}
    return render_template('index.html', form_data=form_data)

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
