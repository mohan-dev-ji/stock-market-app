from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import yfinance as yf
import plotly.graph_objs as go
from newsapi import NewsApiClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import nasdaq_scrapper

app = Flask(__name__)
Bootstrap(app)

NEWS_API = 'd304891846254648836dbbb5ad21d9e3'

newsapi = NewsApiClient(api_key=NEWS_API)

@app.route('/')
def index():
    if request.method == 'POST':
        stock_symbol = request.form['stock_symbol']
        stock_info = yf.Ticker(stock_symbol)
        stock_data = stock_info.info
        
        # Fetch historical stock data
        stock_history = stock_info.history(period="6mo")

        # Create the stock price graph
        trace = go.Scatter(x=stock_history.index,
                            y=stock_history['Close'],
                            mode='lines')
        layout = go.Layout(title=f"{stock_data['longName']} Stock Price",
                           xaxis_title="Date",
                           yaxis_title="Price (USD)")
        fig = go.Figure(data=[trace], layout=layout)
        graph_div = fig.to_html(full_html=False)

        # Fetch news articles
        news_query = stock_data['longName']
        print(stock_data)
        news_articles = newsapi.get_everything(q=news_query, language='en', sort_by='publishedAt')['articles'][:4]
        # news_articles = [article for article in newsapi.get_everything(q=news_query, sort_by='publishedAt')['articles'] if 'language' in article and article['language'] == 'en'][:4]
        
        return render_template('stock_info.html', stock_data=stock_data, graph_div=graph_div, news_articles=news_articles, is_search=True)
    # Fetch leadin stock data
   
    # leading_stock = nasdaq_scrapper.most_active_stock()
    leading_stock = "^IXIC"
    # time.sleep(1)
    print(leading_stock)
    leading_stock_info = yf.Ticker(leading_stock)
    leading_stock_data = leading_stock_info.info
    print(leading_stock_data)
    # Fetch historical stock data
    stock_history = leading_stock_info.history(period="6mo")

    # Create the stock price graph
    trace = go.Scatter(x=stock_history.index,
                        y=stock_history['Close'],
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
    
    return render_template('stock_info.html', stock_data=leading_stock_data, graph_div=graph_div, news_articles=news_articles, is_search=False)

    # return render_template('stock_info.html', stock_data=leading_stock_data, is_search=False)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        print(f"the request form is {request.form}") 
        stock_symbol = request.form['stock_symbol']
        # time_period = request.form['time-period']
        stock_info = yf.Ticker(stock_symbol)
        stock_data = stock_info.info
        
        # Fetch historical stock data
        stock_history = stock_info.history(period="6mo")

        # Create the stock price graph
        trace = go.Scatter(x=stock_history.index,
                            y=stock_history['Close'],
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
        # news_articles = [article for article in newsapi.get_everything(q=news_query, sort_by='publishedAt')['articles'] if 'language' in article and article['language'] == 'en'][:4]
        
        return render_template('stock_info.html', stock_data=stock_data, graph_div=graph_div, news_articles=news_articles, is_search=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)