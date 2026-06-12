# 🚀 Nubra Pro Trading Hub

A professional options trading dashboard for NSE indices with real-time data analysis and signal generation.

## Features

- **Multi-Instrument Support**: Trade NIFTY, BANKNIFTY, FINNIFTY indices
- **Real-Time Market Data**: Live option chain data with 1-second refresh
- **Advanced Analytics**: 
  - Market Bias (BULLISH/BEARISH/NEUTRAL)
  - Support & Resistance levels
  - Put-Call Ratio analysis
  - Max Pain calculation
  - OI Heatmaps
- **Trading Signals**: High-confidence buy/sell signals (>70%)
- **Paper Trading**: Log and track hypothetical trades
- **Professional UI**: Dark theme with real-time clock and metrics

## 📊 Dashboard Tabs

1. **⚙ Setup** - Market structure, bias, levels, PCR, max pain
2. **📈 Price Action** - Momentum radar, top signals by confidence
3. **⚡ Signals** - High-confidence trading setups
4. **🎯 Monitor** - Best CE/PE trade opportunities
5. **📒 Journal** - Trading history and performance metrics
6. **📊 Chain Data** - Complete option chain analysis

## 🔧 Requirements

- Python 3.11+
- Nubra SDK account with live trading credentials
- Valid trading phone number and MPIN

## 📦 Installation

```bash
pip install -r requirements.txt
```

## 🚀 Running Locally

```bash
streamlit run app_v2.py
```

## 📥 Deployment on Streamlit Cloud

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Nubra Trading Hub"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Click "New app"
3. Select your GitHub repo and branch
4. Set main file to: `app_v2.py`
5. Click "Deploy"

### Step 3: Add Secrets

1. Once deployed, go to **App settings** (⚙️)
2. Click **Secrets**
3. Add your credentials:

```toml
PHONE_NO = "your_phone_number"
MPIN = "your_mpin"
```

4. Save and your app will restart with credentials

## 📝 Environment Variables

Create `.env` file for local testing:

```
PHONE_NO=your_phone_number
MPIN=your_mpin
```

## 🎯 Data Sources

- **Nubra Python SDK v0.4.4**
- Live NSE option chain data
- Real-time spot prices
- Open interest and volume data

## 📊 Supported Instruments

- **NIFTY** - Nifty 50 index options
- **BANKNIFTY** - Bank Nifty index options  
- **FINNIFTY** - Financial Nifty index options

## ⚠️ Risk Disclaimer

This is an educational trading tool. Trading in options involves substantial risk of loss. Past performance is not indicative of future results. Always use proper risk management and never risk more than you can afford to lose.

## 📄 License

Private Project

## 👨‍💻 Author

Developed for professional options trading analysis

---

**Live Dashboard**: Check out the deployed app on Streamlit Cloud for real-time trading signals!
