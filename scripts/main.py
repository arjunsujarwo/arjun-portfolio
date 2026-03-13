import ingestion
import anomaly_detector
import time
from datetime import datetime

def run_pipeline():
    print(f"\n[{datetime.now()}] Memulai Pipeline Otomatis...")
    
    # Langkah 1: Ambil Data Baru
    ingestion.fetch_market_data()
    
    # Langkah 2: Deteksi Anomali
    anomaly_detector.detect_anomalies("market_transactions.csv")
    
    print(f"[{datetime.now()}] Pipeline Selesai.\n")

if __name__ == "__main__":
    # Untuk keperluan demo, kita jalankan sekali.
    # Di server/cloud, ini akan dipicu oleh Task Scheduler atau GitHub Actions.
    run_pipeline()