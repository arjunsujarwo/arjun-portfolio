import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def get_crypto_data():
    # Mengambil data harga Bitcoin 7 hari terakhir dari API CoinGecko
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=idr&days=7&interval=daily"
    response = requests.get(url, timeout=15)
    data = response.json()
    
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    # Mengonversi harga ke satuan Juta agar grafik lebih bersih
    df['price_jt'] = df['price'] / 1_000_000
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.strftime('%d %b')
    
    return df

def run_crypto_project(): # Pastikan nama ini dipanggil benar di main.py
    try:
        df = get_crypto_data()
        
        # Plotting Harga
        plt.figure(figsize=(10, 5))
        plt.plot(df['date'], df['price_jt'], marker='o', color='#f2a900', linewidth=2)
        plt.fill_between(df['date'], df['price_jt'], color='#f2a900', alpha=0.1)
        
        plt.title(f"Bitcoin Price Trend (Juta IDR) - Update: {datetime.now().strftime('%Y-%m-%d')}")
        plt.xlabel("Tanggal")
        plt.ylabel("Harga (Juta IDR)")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # SIMPAN GRAFIK KE ROOT (../)
        plt.savefig('../crypto_trend.png')
        plt.close() # Penting untuk GitHub Actions
        
        # Simpan Sentiment (Simpan ke root juga)
        with open("../crypto_status.txt", "w") as f:
            status = "BULLISH (Positive Sentiment)" if df['price'].iloc[-1] > df['price'].iloc[-2] else "BEARISH (Caution)"
            f.write(status)
            
        print("Proyek Crypto Berhasil Diperbarui di folder root!")
    except Exception as e:
        print(f"Error di Crypto Project: {e}")

if __name__ == "__main__":
    run_crypto_project()
