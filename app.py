from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask_bootstrap import Bootstrap
import yfinance as yf
import plotly.graph_objs as go
from newsapi import NewsApiClient
import json
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
Bootstrap(app)

NEWS_API = os.getenv('NEWS_API')

app.secret_key = 'your_secret_key_here'  # Set this to a random secret key

newsapi = NewsApiClient(api_key=NEWS_API)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (pd.Timestamp, datetime)):
            return obj.isoformat()
        return super().default(obj)

def process_stock_data(data):
    return json.loads(json.dumps(data, cls=CustomJSONEncoder))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_symbol = request.form['stock_symbol']
        stock_info = yf.Ticker(stock_symbol)
        stock_data = stock_info.info
    else:
        stock_symbol = "^IXIC"
        stock_info = yf.Ticker(stock_symbol)  
        stock_data = stock_info.info
        stock_data['currentPrice'] = stock_data.get('dayHigh') 

    # Check if the symbol is valid
    try:
        stock_info.info['longName']
        # flash(f'Showing data for {company_name} ({stock_symbol})', 'success')
        # Proceed with your existing logic for valid symbols
        # ...
    except (KeyError, IndexError, ValueError):
        flash(f'"{stock_symbol}" is not a valid stock symbol', 'error')
        return redirect(url_for('index'))

    stock_data = stock_info.info

        # Fetch historical stock data for all time periods
    stock_history_1d = process_stock_data(stock_info.history(period='1d', interval='5m').reset_index().to_dict('records'))
    stock_history_5d = process_stock_data(stock_info.history(period='5d', interval='1h').reset_index().to_dict('records'))
    stock_history_1mo = process_stock_data(stock_info.history(period='1mo').reset_index().to_dict('records'))
    stock_history_6mo = process_stock_data(stock_info.history(period='6mo').reset_index().to_dict('records'))
    stock_history_1y = process_stock_data(stock_info.history(period='1y').reset_index().to_dict('records'))
    stock_history_max = process_stock_data(stock_info.history(period='max').reset_index().to_dict('records'))

    # Create the stock price graph for the default time period (6mo)
    trace = go.Scatter(x=[data['Date'] for data in stock_history_6mo],
                        y=[data['Close'] for data in stock_history_6mo],
                        mode='lines')
    layout = go.Layout(title=f"{stock_data['longName']} Stock Price",
                        xaxis_title="Date",
                        yaxis_title="Price (USD)")
    fig = go.Figure(data=[trace], layout=layout)
    graph_div = fig.to_html(full_html=False)

    # Fetch news articles
    news_query = stock_data['longName']
    # print(stock_data)
    news_articles = newsapi.get_everything(q=news_query, language='en', sort_by='publishedAt')['articles'][:4]

    return render_template('index.html', stock_data=stock_data, graph_div=graph_div, news_articles=news_articles,
                            stock_history_1d=stock_history_1d,
                            stock_history_5d=stock_history_5d,
                            stock_history_1mo=stock_history_1mo,
                            stock_history_6mo=stock_history_6mo,
                            stock_history_1y=stock_history_1y,
                            stock_history_max=stock_history_max)

if __name__ == '__main__':
    app.run(debug=True)