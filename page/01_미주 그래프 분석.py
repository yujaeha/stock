import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="미국 주식 TOP10 분석",
    page_icon="📈",
    layout="wide"
)

st.title("🚀 미국 대표 주식 TOP 10 분석")

stocks = {
    "Tesla": "TSLA",
    "NVIDIA": "NVDA",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Meta": "META",
    "Google": "GOOGL",
    "Palantir": "PLTR",
    "AMD": "AMD",
    "Broadcom": "AVGO"
}

@st.cache_data(ttl=3600)
def load_data():
    df = pd.DataFrame()

    for name, ticker in stocks.items():
        try:
            data = yf.download(
                ticker,
                period="1y",
                auto_adjust=True,
                progress=False
            )

            if not data.empty:
                df[name] = data["Close"]

        except Exception as e:
            st.error(f"{name} 오류: {e}")

    return df

df = load_data()

if df.empty:
    st.error("주가 데이터를 불러오지 못했습니다.")
    st.stop()

# ======================
# 원본 주가 그래프
# ======================

st.subheader("📊 최근 1년 주가")

fig = go.Figure()

for stock in df.columns:
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[stock],
            mode="lines",
            name=stock
        )
    )

fig.update_layout(
    template="plotly_dark",
    height=700,
    hovermode="x unified",
    title="미국 대표 주식 TOP10"
)

st.plotly_chart(fig, use_container_width=True)

# ======================
# 수익률 계산
# ======================

returns = ((df.iloc[-1] / df.iloc[0]) - 1) * 100

returns_df = pd.DataFrame({
    "종목": returns.index,
    "수익률(%)": returns.round(2)
}).sort_values("수익률(%)", ascending=False)

st.subheader("🏆 최근 1년 수익률 순위")

st.dataframe(
    returns_df,
    use_container_width=True,
    hide_index=True
)

winner = returns.idxmax()

st.success(
    f"1위: {winner} ({returns.max():.2f}%)"
)

# ======================
# 정규화 비교 그래프
# ======================

st.subheader("📈 시작가 기준 성과 비교")

normalized = df / df.iloc[0] * 100

fig2 = go.Figure()

for stock in normalized.columns:
    fig2.add_trace(
        go.Scatter(
            x=normalized.index,
            y=normalized[stock],
            mode="lines",
            name=stock
        )
    )

fig2.update_layout(
    template="plotly_dark",
    height=700,
    hovermode="x unified",
    yaxis_title="시작가 = 100"
)

st.plotly_chart(fig2, use_container_width=True)

# ======================
# 변동성 분석
# ======================

daily_returns = df.pct_change().dropna()

volatility = daily_returns.std() * 100

vol_df = pd.DataFrame({
    "종목": volatility.index,
    "일일 변동성(%)": volatility.round(2)
}).sort_values("일일 변동성(%)", ascending=False)

st.subheader("⚡ 변동성 순위")

st.dataframe(
    vol_df,
    use_container_width=True,
    hide_index=True
)

st.info(
    f"가장 변동성이 큰 종목: {volatility.idxmax()}"
)

# ======================
# 데이터 확인
# ======================

with st.expander("원본 데이터 보기"):
    st.dataframe(df.tail())

st.caption("Data Source : Yahoo Finance")
