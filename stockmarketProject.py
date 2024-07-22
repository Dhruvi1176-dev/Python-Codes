import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import streamlit as st

# Function to fetch real-time stock data
def fetch_data(ticker, period='1d'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval='1m')
    return data

# Function to process the data
def process_data(data):
    data.reset_index(inplace=True)
    data['Datetime'] = pd.to_datetime(data['Datetime'])
    return data

# Function to plot the data
def plot_data(data, ticker):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data['Datetime'],
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'],
                                 name=ticker))
    fig.update_layout(title=f'Stock Price Data for {ticker}',
                      xaxis_title='Date',
                      yaxis_title='Price',
                      xaxis_rangeslider_visible=False)
    return fig

# Streamlit app
st.title("Real-Time Stock Price Dashboard")

ticker = st.text_input("Enter Stock Ticker", "AAPL")
period = st.selectbox("Select Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"])

if st.button("Fetch Data"):
    with st.spinner("Fetching data..."):
        data = fetch_data(ticker, period)
        data = process_data(data)
        fig = plot_data(data, ticker)
        st.plotly_chart(fig)

st.write("Data Source: Yahoo Finance")
