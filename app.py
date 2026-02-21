import streamlit as st
import requests
import pandas as pd

st.title("📈 AI暗号資産シミュレーター（JPY対応）")

symbol = st.selectbox("通貨ペア", ["BTCUSDT", "ETHUSDT"])
initial_jpy = st.number_input("初期資金（円）", value=100000, step=10000)

if "cash_jpy" not in st.session_state:
    st.session_state.cash_jpy = initial_jpy
    st.session_state.coin = 0.0
    st.session_state.prices = []

def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    return float(requests.get(url, timeout=5).json()["price"])

def get_usdjpy():
    url = "https://api.exchangerate.host/latest?base=USD&symbols=JPY"
    return float(requests.get(url, timeout=5).json()["rates"]["JPY"])

price_usdt = get_price(symbol)
usd_jpy = get_usdjpy()
price_jpy = price_usdt * usd_jpy

st.metric("現在価格（円）", f"{price_jpy:,.0f} 円")

st.session_state.prices.append(price_jpy)

if len(st.session_state.prices) > 5:
    ma = pd.Series(st.session_state.prices).rolling(5).mean().iloc[-1]

    if price_jpy > ma and st.session_state.cash_jpy > 0:
        st.session_state.coin = st.session_state.cash_jpy / price_jpy
        st.session_state.cash_jpy = 0
        st.success("📈 BUY")

    elif price_jpy < ma and st.session_state.coin > 0:
        st.session_state.cash_jpy = st.session_state.coin * price_jpy
        st.session_state.coin = 0
        st.warning("📉 SELL")

assets = st.session_state.cash_jpy + st.session_state.coin * price_jpy
st.metric("総資産（円）", f"{assets:,.0f} 円")

st.line_chart(st.session_state.prices)
