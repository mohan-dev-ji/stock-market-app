# Stock Tracker

Stock Tracker is a web application that allows users to search for and view stock information, including current price, historical data, and recent news articles.

## Features

- Search for stocks by symbol
- Display current stock price and basic information
- Show historical stock price data with interactive charts
- Present recent news articles related to the searched stock
- Responsive design for desktop and mobile devices

## Technologies Used

- Python 3.8+
- Flask web framework
- yfinance library for fetching stock data
- Plotly for interactive charts
- News API for fetching related news articles
- Bootstrap for frontend styling

## Installation

1. Clone the repository:

git clone https://github.com/mohan-dev-ji/stock-market-app/tree/main
cd stock-tracker

2. Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate

3. Install the required packages:

pip install -r requirements.txt

4. Create a `.env` file in the root directory and add your News API key:

NEWS_API_KEY=your_news_api_key_here

## Usage

1. Run the Flask application:

python app.py

2. Open a web browser and navigate to `http://localhost:5000`

3. Enter a stock symbol (e.g., AAPL for Apple Inc.) in the search bar and press Enter or click the Search button

4. View the stock information, historical price chart, and related news articles

## Project Structure


stock-tracker/
│
├── app.py # Main Flask application
├── requirements.txt # Python dependencies
├── .env # Environment variables (not in version control)
├── .gitignore # Git ignore file
│
├── templates/
│ ├── base.html # Base template
│ └── index.html # Main page template

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) for providing stock data
- [News API](https://newsapi.org/) for news article data
- [Plotly](https://plotly.com/) for interactive charting capabilities
- [Bootstrap](https://getbootstrap.com/) for responsive design components

