
from pnl_tracker import (
    calculate_pnl
)
import streamlit as st
from fetch_chain import get_chain
from buying_engine import option_buying_engine
from buying_terminal import build_trade
from market_bias import market_bias
from paper_trade import save_paper_trade
from trade_journal import load_journal
from trade_monitor import (
    monitor_trades
)
@st.fragment(run_every="1s")
def clock_panel():

    from datetime import datetime

    st.markdown(
        f"### ⏰ {datetime.now().strftime('%H:%M:%S')}"
    )
   

st.markdown("""
<style>

.stApp{
background-color:#0a0d14;
}

[data-testid="stMetric"]{
background:#161b22;
padding:12px;
border-radius:12px;
border:1px solid #2d333b;
}

</style>
""", unsafe_allow_html=True) 

st.set_page_config(page_title="Buying Terminal", layout="wide")

@st.cache_data(ttl=1)
def get_live():
    return get_chain()

st.title("🚀 NUBRA OPTION BUYING TERMINAL")

@st.fragment(run_every="1s")
def live_panel():
    df, chain = get_live()
    spot = (chain.current_price or 0) / 100

    best_ce, best_pe, board = option_buying_engine(df, spot)

    bias = market_bias(board)

    st.success(
        f"📈 Market Bias: {bias}"
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Spot", round(spot, 2))
    c2.metric("Rows", len(df))
    c3.metric("Tracked", len(board))

    l, r = st.columns(2)

    with l:
        st.subheader("🚀 Best CE")

        if len(best_ce):
            ce_trade = build_trade(best_ce.iloc[0])

            st.metric("Strike", ce_trade["strike"])
            st.metric("Entry", ce_trade["entry"])
            st.metric("SL", ce_trade["sl"])
            st.metric("Target 1", ce_trade["target1"])
            st.metric("Target 2", ce_trade["target2"])
            st.metric("Confidence", ce_trade["confidence"])
            st.write(f"Flow: {ce_trade['flow']}")
            st.write(f"Grade: {ce_trade['grade']}")

            if st.button("💾 Save CE Trade"):
                save_paper_trade(ce_trade)
                st.success("CE Trade Saved")

    with r:
        st.subheader("🔻 Best PE")

        if len(best_pe):
            pe_trade = build_trade(best_pe.iloc[0])

            st.metric("Strike", pe_trade["strike"])
            st.metric("Entry", pe_trade["entry"])
            st.metric("SL", pe_trade["sl"])
            st.metric("Target 1", pe_trade["target1"])
            st.metric("Target 2", pe_trade["target2"])
            st.metric("Confidence", pe_trade["confidence"])
            st.write(f"Flow: {pe_trade['flow']}")
            st.write(f"Grade: {pe_trade['grade']}")

            if st.button("💾 Save PE Trade"):
                save_paper_trade(pe_trade)
                st.success("PE Trade Saved")

@st.fragment(run_every="2s")
def radar_panel():

    df, chain = get_live()

    _, _, board = option_buying_engine(
        df,
        (chain.current_price or 0) / 100
    )

    radar = (
        board[
            board["confidence"] >= 50
        ]
        .sort_values(
            ["confidence", "score"],
            ascending=False
        )
        .head(10)
    )

    if len(radar):
        best = radar.iloc[0]

        st.success(
            f"""
            🚨 BEST SETUP

            {best['type']} {best['strike']}

            Grade: {best['grade']}

            Flow: {best['flow']}

            Confidence: {best['confidence']}%
            """
        )

    st.subheader("🎯 Trade Radar")

    st.dataframe(
        radar[
            [
                "type",
                "strike",
                "flow",
                "strength",
                "confidence",
                "score",
                "grade",
                "signal"
            ]
        ],
        use_container_width=True
    )

@st.fragment(run_every="3s")
def institutional_panel():

    df, chain = get_live()

    _, _, board = option_buying_engine(
        df,
        (chain.current_price or 0) / 100
    )

    inst = board[
        board["institutional"]
    ]

    st.subheader("🏦 Institutional Flow")

    if len(inst):
        st.dataframe(
            inst[
                [
                    "type",
                    "strike",
                    "flow",
                    "confidence",
                    "score"
                ]
            ],
            use_container_width=True
        )
    else:
        st.info("No institutional activity detected.")

@st.fragment(run_every="2s")
def elite_radar():

    df, chain = get_live()

    _, _, board = option_buying_engine(
        df,
        (chain.current_price or 0) / 100
    )

    elite = board[
        board["institutional"]
    ].sort_values(
        "radar_score",
        ascending=False
    )

    st.subheader("🚨 Elite Momentum Radar")

    if len(elite):
        st.dataframe(
            elite[
                [
                    "type",
                    "strike",
                    "flow",
                    "strength",
                    "grade",
                    "confidence",
                    "radar_score"
                ]
            ].head(10),
            use_container_width=True
        )
    else:
        st.info("No elite setups.")

@st.fragment(run_every="3s")
def momentum_panel():
    df, chain = get_live()
    _, _, board = option_buying_engine(df, (chain.current_price or 0) / 100)

    st.subheader("⚡ Momentum")
    st.dataframe(board, use_container_width=True)

@st.fragment(run_every="5s")
def journal_panel():

    trades = load_journal()

    st.subheader(
        "📒 Trade Journal"
    )

    if len(trades):

        st.dataframe(
            trades,
            use_container_width=True
        )

    else:

        st.info(
            "No trades saved."
        )

@st.fragment(run_every="5s")
def pnl_panel():

    trades = load_journal()

    stats = calculate_pnl(
        trades
    )

    st.subheader(
        "📊 Strategy Stats"
    )

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Trades",
        stats["total"]
    )

    c2.metric(
        "Wins",
        stats["wins"]
    )

    c3.metric(
        "Losses",
        stats["losses"]
    )

    c4.metric(
        "Win Rate",
        f"{stats['win_rate']}%"
    )

@st.fragment(run_every="2s")
def trade_monitor_panel():

    trades = load_journal()

    if len(trades) == 0:

        return

    df, chain = get_live()

    monitor = monitor_trades(
        trades,
        df
    )

    st.subheader(
        "🎯 Live Trade Monitor"
    )

    st.dataframe(
        monitor[
            [
                "strike",
                "type",
                "entry",
                "current_ltp",
                "pnl",
                "pnl_pct",
                "status",
                "grade",
                "confidence"
            ]
        ],
        use_container_width=True
    )
clock_panel()
trade_monitor_panel()
pnl_panel()
live_panel()
radar_panel()
momentum_panel()
institutional_panel()
elite_radar()
journal_panel()
