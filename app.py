from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import yfinance as yf
import plotly.graph_objs as go
from newsapi import NewsApiClient
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
# import time
# import json
# from datetime import datetime


# import nasdaq_scrapper

app = Flask(__name__)
Bootstrap(app)

NEWS_API = 'd304891846254648836dbbb5ad21d9e3'

newsapi = NewsApiClient(api_key=NEWS_API)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(f"the request form is {request.form}") 
        stock_symbol = request.form['stock_symbol']
        # time_period = request.form['time-period']
        stock_info = yf.Ticker(stock_symbol)
        stock_data = stock_info.info

         # Fetch historical stock data for all time periods
        stock_history_1d = stock_info.history(period='1d', interval='60m').reset_index().to_dict('records')
        stock_history_5d = stock_info.history(period='5d', interval='1d').reset_index().to_dict('records')
        stock_history_1mo = stock_info.history(period='1mo').reset_index().to_dict('records')
        stock_history_6mo = stock_info.history(period='6mo').reset_index().to_dict('records')
        stock_history_1y = stock_info.history(period='1y').reset_index().to_dict('records')
        stock_history_max = stock_info.history(period='max').reset_index().to_dict('records')

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
                                stock_history_1d=stock_history_1d, stock_history_5d=stock_history_5d,
                                stock_history_1mo=stock_history_1mo, stock_history_6mo=stock_history_6mo,
                                stock_history_1y=stock_history_1y, stock_history_max=stock_history_max, 
                                is_search=True)
    else:
        # leading_stock = nasdaq_scrapper.most_active_stock()
        leading_stock = "^IXIC"
        leading_stock_info = yf.Ticker(leading_stock)
        leading_stock_data = leading_stock_info.info

        # Ensure currentPrice is available and is a number
        leading_stock_data['currentPrice'] = leading_stock_data.get('dayHigh')
        # leading_stock_data['currentPrice'] = leading_stock_data.get('regularMarketPrice') or leading_stock_data.get('currentPrice')

        # if leading_stock_data['currentPrice'] is None or not isinstance(leading_stock_data['currentPrice'], (int, float)):
        #     leading_stock_data['currentPrice'] = 'N/A'
        print(f"the nasdaq stock is {leading_stock_data}")
        # Fetch historical stock data for all time periods
        stock_history_1d = leading_stock_info.history(period='1d', interval='5m').reset_index().to_dict('records')
        stock_history_5d = leading_stock_info.history(period='5d', interval='1d').reset_index().to_dict('records')
        stock_history_1mo = leading_stock_info.history(period='1mo').reset_index().to_dict('records')
        stock_history_6mo = leading_stock_info.history(period='6mo').reset_index().to_dict('records')
        stock_history_1y = leading_stock_info.history(period='1y').reset_index().to_dict('records')
        stock_history_max = leading_stock_info.history(period='max').reset_index().to_dict('records')

        # Create the stock price graph for the default time period (6mo)
        trace = go.Scatter(x=[data['Date'] for data in stock_history_6mo],
                            y=[data['Close'] for data in stock_history_6mo],
                            mode='lines')
        layout = go.Layout(title=f"{leading_stock_data['longName']} Stock Price",
                            xaxis_title="Date",
                            yaxis_title="Price (USD)")
        fig = go.Figure(data=[trace], layout=layout)
        graph_div = fig.to_html(full_html=False)

        # Fetch news articles
        news_query = leading_stock_data['longName']
        # print(stock_data)
        news_articles = newsapi.get_everything(q=news_query, language='en', sort_by='publishedAt')['articles'][:4]
        # news_articles = [article for article in newsapi.get_everything(q=news_query, sort_by='publishedAt')['articles'] if 'language' in article and article['language'] == 'en'][:4]
        
        return render_template('index.html', stock_data=leading_stock_data, graph_div=graph_div, news_articles=news_articles,
                                stock_history_1d=stock_history_1d, stock_history_5d=stock_history_5d,
                                stock_history_1mo=stock_history_1mo, stock_history_6mo=stock_history_6mo,
                                stock_history_1y=stock_history_1y, stock_history_max=stock_history_max, 
                                is_search=False)

# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     if request.method == 'POST':
#         print(f"the request form is {request.form}") 
#         stock_symbol = request.form['stock_symbol']
#         # time_period = request.form['time-period']
#         stock_info = yf.Ticker(stock_symbol)
#         stock_data = stock_info.info

#          # Fetch historical stock data for all time periods
#         stock_history_1d = stock_info.history(period='1d', interval='5m').reset_index().to_dict('records')
#         stock_history_5d = stock_info.history(period='5d', interval='1d').reset_index().to_dict('records')
#         stock_history_1mo = stock_info.history(period='1mo').reset_index().to_dict('records')
#         stock_history_6mo = stock_info.history(period='6mo').reset_index().to_dict('records')
#         stock_history_1y = stock_info.history(period='1y').reset_index().to_dict('records')
#         stock_history_max = stock_info.history(period='max').reset_index().to_dict('records')

#         # Create the stock price graph for the default time period (6mo)
#         trace = go.Scatter(x=[data['Date'] for data in stock_history_6mo],
#                            y=[data['Close'] for data in stock_history_6mo],
#                            mode='lines')
#         layout = go.Layout(title=f"{stock_data['longName']} Stock Price",
#                            xaxis_title="Date",
#                            yaxis_title="Price (USD)")
#         fig = go.Figure(data=[trace], layout=layout)
#         graph_div = fig.to_html(full_html=False)

#         # Fetch news articles
#         news_query = stock_data['longName']
#         # print(stock_data)
#         news_articles = newsapi.get_everything(q=news_query, language='en', sort_by='publishedAt')['articles'][:4]
#         # news_articles = [article for article in newsapi.get_everything(q=news_query, sort_by='publishedAt')['articles'] if 'language' in article and article['language'] == 'en'][:4]
#         # Convert stock_history to JSON
#         # stock_history_json = json.dumps(stock_history)
#         return render_template('stock_info.html', stock_data=stock_data, graph_div=graph_div, news_articles=news_articles,
#                                 stock_history_1d=stock_history_1d, stock_history_5d=stock_history_5d,
#                                 stock_history_1mo=stock_history_1mo, stock_history_6mo=stock_history_6mo,
#                                 stock_history_1y=stock_history_1y, stock_history_max=stock_history_max, 
#                                 is_search=True)
#     return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)