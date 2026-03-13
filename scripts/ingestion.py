import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_market_data(ticker="BTC-USD"):
    # Mengambil data 1 jam terakhir
    data = yf.download(tickers=ticker, period='1d', interval='1m')
    
    if not data.empty:
        # Menambahkan kolom timestamp untuk keperluan audit data
        data['processed_at'] = datetime.now()
        
        # Simpan ke CSV (Simulasi Data Warehouse sederhana)
        data.to_csv("market_transactions.csv")
        print(f"[{datetime.now()}] Berhasil menarik {len(data)} baris data.")
    else:
        print("Gagal menarik data.")

if __name__ == "__main__":
    fetch_market_data()