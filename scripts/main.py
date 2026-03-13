# scripts/main.py
import scrapper
import analyzer
import crypto_analyzer
import ingestion
import anomaly_detector
from datetime import datetime

def run_all_updates():
    print(f"=== [{datetime.now()}] MEMULAI ETL PIPELINE ===")
    
    # Project 1: News Scraper & Analyzer
    print("\n[1/4] Mengambil dan menganalisis berita...")
    scrapper.run() # Pastikan di scrapper.py ada fungsi def run()
    analyzer.analyze_and_plot()
    
    # Project 3: Crypto Analyzer
    print("\n[2/4] Menganalisis pasar Crypto...")
    crypto_analyzer.run_analysis() # Sesuaikan nama fungsi di crypto_analyzer.py
    
    # Project 4: Anomaly Detection (Ingestion & Detection)
    print("\n[3/4] Ingesting market data & detecting anomalies...")
    # Jika di ingestion.py nama fungsinya fetch_market_data:
    ingestion.fetch_market_data() 
    # Jika di anomaly_detector.py nama fungsinya detect_anomalies:
    anomaly_detector.detect_anomalies("market_transactions.csv")
    
    print(f"\n=== [{datetime.now()}] SEMUA DATA BERHASIL DIPERBARUI ===")

if __name__ == "__main__":
    run_all_updates()
