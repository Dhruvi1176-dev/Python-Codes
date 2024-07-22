import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

# Function to fetch stock data
def fetch_stock_data(tickers):
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        data[ticker] = hist
    return data

# Function to plot individual stock data
def plot_stock_data(data, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name=ticker))
    fig.update_layout(title=f'{ticker} Stock Price', xaxis_title='Date', yaxis_title='Price')
    return fig

# Streamlit app
st.title("Stock Price Dashboard")

tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META']

if st.button("Show Data"):
    with st.spinner('Fetching data...'):
        stock_data = fetch_stock_data(tickers)
        
        # Render charts in 2 rows and 3 columns
        cols = st.columns(3)
        for i, ticker in enumerate(tickers):
            with cols[i % 3]:
                fig = plot_stock_data(stock_data[ticker], ticker)
                st.plotly_chart(fig)

        st.balloons()
        st.success('Data loaded successfully!')

