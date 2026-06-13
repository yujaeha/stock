import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="주가 분석 대시보드",
    page_icon="📈",
    layout="wide"
)

st.title("📈 글로벌 주식 1년 분석")

stocks = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "구글": "GOOGL",
    "마이크로소프트": "MSFT",
    "애플": "AAPL"
}

@st.cache_data
def load_data():
    data = yf.download(
        list(stocks.values()),
        period="1y",
        auto_adjust=True,
        progress=False
    )

    close = data["Close"]
    close.columns = stocks.keys()
    return close

df = load_data()

st.subheader("📊 최근 1년 주가 추이")

fig = go.Figure()

for company in df.columns:
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[company],
            mode="lines",
            name=company
        )
    )

fig.update_layout(
    height=600,
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="주가",
    legend_title="종목"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------
# 수익률 계산
# --------------------

returns = ((df.iloc[-1] / df.iloc[0]) - 1) * 100

st.subheader("🚀 최근 1년 수익률")

returns_df = pd.DataFrame({
    "종목": returns.index,
    "수익률(%)": returns.values
}).sort_values("수익률(%)", ascending=False)

st.dataframe(
    returns_df,
    use_container_width=True,
    hide_index=True
)

best_stock = returns.idxmax()
best_return = returns.max()

st.success(
    f"🏆 최고 상승 종목: {best_stock} ({best_return:.2f}%)"
)

# --------------------
# 정규화 그래프
# --------------------

st.subheader("📉 시작가 기준 성과 비교")

normalized = df / df.iloc[0] * 100

fig2 = go.Figure()

for company in normalized.columns:
    fig2.add_trace(
        go.Scatter(
            x=normalized.index,
            y=normalized[company],
            mode="lines",
            name=company
        )
    )

fig2.update_layout(
    height=600,
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="시작가 대비 (%)"
)

st.plotly_chart(fig2, use_container_width=True)

# --------------------
# 변동성 분석
# --------------------

daily_returns = df.pct_change().dropna()
volatility = daily_returns.std() * 100

st.subheader("⚡ 변동성 분석")

vol_df = pd.DataFrame({
    "종목": volatility.index,
    "일간 변동성(%)": volatility.values
}).sort_values("일간 변동성(%)", ascending=False)

st.dataframe(
    vol_df,
    use_container_width=True,
    hide_index=True
)

most_volatile = volatility.idxmax()

st.info(
    f"📌 가장 변동성이 큰 종목: {most_volatile}"
)

st.caption("데이터 출처: Yahoo Finance (yfinance)")
