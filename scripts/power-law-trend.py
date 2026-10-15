# power-law-trend.py  (fixed & improved)
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# Resolve paths from the repo root so the script runs from any working directory
REPO_ROOT = Path(__file__).resolve().parent.parent
PRICES_CSV = REPO_ROOT / 'data' / 'bitcoin-monthly-prices.csv'
OUTPUT_PNG = REPO_ROOT / 'charts' / 'power-law-trend.png'
# Load data
df = pd.read_csv(PRICES_CSV, parse_dates=['date'])
df = df.rename(columns={'date': 'Date', 'price_usd': 'Price'})
# Remove zero/near-zero prices (keeps the trend clean)
df = df[df['Price'] > 1].copy()
# Reference date = first valid price date
reference_date = df['Date'].min()
# Days since reference date
df['Days'] = (df['Date'] - reference_date).dt.days
# Log regression → straight line on log scale
df['LogPrice'] = np.log10(df['Price'])
X = df[['Days']]
y = df['LogPrice']
model = LinearRegression()
model.fit(X, y)
# Trend line back to USD
df['Trend_Price'] = 10 ** model.predict(X)
# === 2030 Prediction (FIXED - no .dt error) ===
future_date = pd.to_datetime('2030-01-01')
# ← scalar, use .days directly
future_days = (future_date - reference_date).days
pred_log = model.predict(pd.DataFrame({'Days': [future_days]}))[0]
pred_price = 10 ** pred_log
print(f"Predicted Bitcoin price on 2030-01-01: ${pred_price:,.0f}")
# === Plot ===
plt.figure(figsize=(14, 8))
plt.scatter(df['Date'], df['Price'], color='blue',
            alpha=0.8, s=40, label='Historical Price')
plt.plot(df['Date'], df['Trend_Price'], color='red',
         linewidth=3, label='Exponential Trend (Log Fit)')
# 2030 marker
plt.axvline(future_date, color='green', linestyle='--', linewidth=2)
plt.scatter(future_date, pred_price, color='green', s=200, zorder=10)
plt.text(future_date, pred_price * 1.3, f'2030\n${pred_price:,.0f}',
         fontsize=14, fontweight='bold', color='green', ha='center',
         bbox=dict(facecolor='white', alpha=0.9, edgecolor='none', pad=8))
plt.yscale('log')
plt.title('Bitcoin Long-Term Price – Straight Exponential Trend (Log Scale)',
          fontsize=16, pad=20)
plt.xlabel('Year')
plt.ylabel('Price (USD) – Log Scale')
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend(fontsize=12)
# Clean x-axis
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.YearLocator(2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_PNG,
            dpi=300, bbox_inches='tight')
print(f"Chart saved: {OUTPUT_PNG.relative_to(REPO_ROOT)}")
