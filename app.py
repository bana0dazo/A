import streamlit as st
import ccxt
import pandas as pd

exchange = ccxt.binance()

st.title("📈 AI暗号資産シミュレーター")

symbol = st.selectbox("通貨ペア", ["BTC/USDT", "ETH/USDT"])
balance = st.number_input("初期資金（USDT）", 1000)

if "cash" not in st.session_state:
    st.session_state.cash = balance
    st.session_state.coin = 0
    st.session_state.prices = []

price = exchange.fetch_ticker(symbol)["last"]
st.metric("現在価格", price)

st.session_state.prices.append(price)

if len(st.session_state.prices) > 5:
    ma = pd.Series(st.session_state.prices).rolling(5).mean().iloc[-1]

    if price > ma and st.session_state.cash > 0:
        st.session_state.coin = st.session_state.cash / price
        st.session_state.cash = 0
        st.success("BUY")

    elif price < ma and st.session_state.coin > 0:
        st.session_state.cash = st.session_state.coin * price
        st.session_state.coin = 0
        st.warning("SELL")

assets = st.session_state.cash + st.session_state.coin * price
st.metric("総資産", round(assets, 2))

st.line_chart(st.session_state.prices)
