# scripts/main.py
import scrapper
import analyzer
import crypto_analyzer
import ingestion
import anomaly_detector
from datetime import datetime

def run_all_updates():
    print(f"=== [{datetime.now()}] MEMULAI ETL PIPELINE ===")
    
    # Project 1: News (Gunakan nama fungsi yang sudah kita perbaiki)
    print("\n[1/4] Mengambil dan menganalisis berita...")
    scrapper.run_scraper()
    analyzer.analyze_and_plot()
    
    # Project 3: Crypto (Pastikan indentasi 4 spasi di sini)
    print("\n[2/4] Menganalisis pasar Crypto...")
    crypto_analyzer.run_crypto_project()
    
    # Project 4: Anomaly Detection
    print("\n[3/4] Ingesting market data & detecting anomalies...")
    ingestion.fetch_market_data()
    anomaly_detector.detect_anomalies("../market_transactions.csv")
    
    print(f"\n=== [{datetime.now()}] SEMUA DATA BERHASIL DIPERBARUI ===")

if __name__ == "__main__":
    run_all_updates()
