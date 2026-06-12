import streamlit as st
import pandas as pd
from datetime import datetime

# Configure page FIRST
st.set_page_config(page_title="Nubra Trading Hub", layout="wide", initial_sidebar_state="collapsed")

# Dark theme styling
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

# Create tabs FIRST - before any imports or heavy processing
st.title("🏦 NUBRA TRADING HUB")
st.divider()

tab1, tab2 = st.tabs(["🚀 Buying Terminal", "📊 Options Dashboard"])

# Import functions
try:
    from fetch_chain import get_chain
    from pcr import calculate_pcr
    from max_pain import calculate_max_pain
    from buying_engine import option_buying_engine
    from buying_terminal import build_trade
    from market_bias import market_bias
    from paper_trade import save_paper_trade
    from trade_journal import load_journal
    from trade_monitor import monitor_trades
    from pnl_tracker import calculate_pnl
    from oi_heatmap import plot_oi
    from support_resistance import get_support_resistance
    from iv_skew import iv_skew
    from gex import calculate_gex
except Exception as e:
    st.error(f"Import error: {e}")

# Cache for live data
@st.cache_data(ttl=1)
def get_live():
    return get_chain()

# Clock panel
@st.fragment(run_every="1s")
def clock_panel():
    st.markdown(f"### ⏰ {datetime.now().strftime('%H:%M:%S')}")

# ==================== TAB 1: BUYING TERMINAL ====================
with tab1:
    st.header("🚀 OPTION BUYING TERMINAL")
    clock_panel()
    
    @st.fragment(run_every="1s")
    def buying_panel():
        try:
            df, chain = get_live()
            spot = (chain.current_price or 0) / 100

            best_ce, best_pe, board = option_buying_engine(df, spot)
            bias = market_bias(board)

            st.success(f"📈 Market Bias: {bias}")

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

            st.divider()
            st.subheader("Trade Journal")
            journal = load_journal()
            if not journal.empty:
                st.dataframe(journal, use_container_width=True)
            else:
                st.info("No trades in journal yet")

            st.divider()
            st.subheader("PnL Tracker")
            try:
                pnl = calculate_pnl(journal)
                st.metric("Total PnL", pnl)
            except:
                st.info("PnL calculation pending...")

        except Exception as e:
            st.error(f"Error loading buying terminal: {str(e)}")

    buying_panel()


# ==================== TAB 2: OPTIONS DASHBOARD ====================
with tab2:
    st.header("📊 OPTIONS DASHBOARD")
    
    try:
        df, chain = get_live()
        
        if "previous_df" not in st.session_state:
            st.session_state.previous_df = df.copy()
        
        st.session_state.previous_df = df.copy()

        spot = chain.current_price / 100
        pcr_data = calculate_pcr(df)
        max_pain = calculate_max_pain(df)

        # Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Spot", round(spot, 2))
        col2.metric("PCR", pcr_data["PCR"])
        col3.metric("Max Pain", max_pain)

        st.divider()

        # Option Chain Data
        st.subheader("Option Chain")
        st.dataframe(df, use_container_width=True)

        st.divider()

        # OI Distribution
        st.subheader("OI Distribution")
        try:
            st.plotly_chart(plot_oi(df), use_container_width=True)
        except:
            st.warning("Could not load OI heatmap")

        st.divider()

        # Top Resistance & Support
        ce = df[df.type == "CE"].sort_values("oi", ascending=False).head(10)
        pe = df[df.type == "PE"].sort_values("oi", ascending=False).head(10)

        left, right = st.columns(2)

        with left:
            st.subheader("Top Resistance (CE)")
            st.dataframe(ce[["strike", "oi", "volume"]], use_container_width=True)

        with right:
            st.subheader("Top Support (PE)")
            st.dataframe(pe[["strike", "oi", "volume"]], use_container_width=True)

        st.divider()

        # Support & Resistance Analysis
        try:
            support, resistance = get_support_resistance(df)
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Support Levels")
                st.write(support)
            
            with col2:
                st.subheader("Resistance Levels")
                st.write(resistance)
        except:
            st.warning("Could not calculate support/resistance")

        st.divider()

        # IV Analysis
        try:
            skew = iv_skew(df)
            st.subheader("IV Skew Analysis")
            st.write(skew)
        except:
            st.warning("Could not calculate IV skew")

        st.divider()

        # OI Build-up
        st.subheader("Largest OI Build-up")
        build_up = (
            df.sort_values("oi_change", ascending=False)
            [["type", "strike", "oi_change", "oi"]]
            .head(15)
        )
        st.dataframe(build_up, use_container_width=True)

        st.divider()

        # OI Unwinding
        st.subheader("Largest OI Unwinding")
        unwinding = (
            df.sort_values("oi_change", ascending=True)
            [["type", "strike", "oi_change", "oi"]]
            .head(15)
        )
        st.dataframe(unwinding, use_container_width=True)

        st.divider()

        # GEX Analysis
        try:
            st.subheader("Gamma Exposure Analysis")
            gex = calculate_gex(df)
            st.write(gex)
        except:
            st.warning("Could not calculate GEX")

    except Exception as e:
        st.error(f"Error loading options dashboard: {str(e)}")
