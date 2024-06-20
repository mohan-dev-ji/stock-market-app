function updateStockGraph(timePeriod) {
    // Get the stock symbol from the template
    console.log('updateStockGraph called with timePeriod:', timePeriod);
    const stockSymbol = "{{ stock_data['symbol'] }}";

    // Parse the stock history JSON string from the template
    const stockHistory = JSON.parse("{{ stock_history|safe }}");
    console.log('Stock history:', stockHistory);
    // Get the stock data for the selected time period
    const stockData = stockHistory[timePeriod];

    // Extract the dates and closing prices from the stock data
    const dates = stockData.map(data => data.Date);
    const closingPrices = stockData.map(data => data.Close);

    // Create the trace object for the stock price line chart
    const trace = {
        x: dates, // Set the x-axis data to the dates
        y: closingPrices, // Set the y-axis data to the closing prices
        mode: 'lines' // Set the mode to 'lines' to create a line chart
    };

    // Create the layout object for the chart
    const layout = {
        title: `{{ stock_data['longName'] }} Stock Price (${timePeriod})`, // Set the chart title
        xaxis: {
            title: 'Date' // Set the x-axis title
        },
        yaxis: {
            title: 'Price (USD)' // Set the y-axis title
        }
    };

    // Create an array with the trace object
    const data = [trace];

    // Use Plotly.newPlot to create the chart
    Plotly.newPlot('stock-graph', data, layout);
}