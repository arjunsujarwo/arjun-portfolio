import pandas as pd
import numpy as np

def detect_anomalies(file_path):
    # 1. Load data
    df = pd.read_csv(file_path)
    
    # 2. KONVERSI DATA: Pastikan kolom 'Close' adalah angka
    # errors='coerce' akan mengubah data yang bukan angka menjadi NaN
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    
    # Hapus baris yang kosong (NaN) agar perhitungan mean tidak error
    df = df.dropna(subset=['Close'])
    
    data = df['Close']
    
    # 3. Hitung Statistik
    mean = np.mean(data)
    std = np.std(data)
    
    # Jika standar deviasi 0 (data flat), kita tidak bisa hitung z-score
    if std == 0:
        print("Data terlalu stabil, tidak ada anomali yang bisa dihitung.")
        return df

    # 4. Tentukan Threshold Z-Score
    threshold = 3
    df['z_score'] = (df['Close'] - mean) / std
    df['is_anomaly'] = np.abs(df['z_score']) > threshold
    
    # 5. Filter Anomali
    anomalies = df[df['is_anomaly'] == True]
    
    print("-" * 30)
    print(f"Total Data dianalisis: {len(df)}")
    print(f"Anomali ditemukan: {len(anomalies)}")
    print("-" * 30)
    
    if len(anomalies) > 0:
        print("Detail Anomali Ditemukan!")
        print(anomalies[['Close', 'z_score']])
        anomalies.to_csv("alerts_log.csv", index=False)
    else:
        print("Tidak ada anomali terdeteksi (Data masih dalam batas wajar).")
    
    return df

if __name__ == "__main__":
    detect_anomalies("market_transactions.csv")

import pandas as pd
import numpy as np

def detect_anomalies(file_path):
    df = pd.read_csv(file_path)
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df = df.dropna(subset=['Close'])
    
    mean = np.mean(df['Close'])
    std = np.std(df['Close'])
    
    if std == 0: return df

    df['z_score'] = (df['Close'] - mean) / std
    df['is_anomaly'] = np.abs(df['z_score']) > 3
    
    # --- BAGIAN PENTING: SIMPAN HASIL KE CSV ---
    # Kita simpan kembali ke market_transactions.csv agar kolom 'is_anomaly' masuk ke sana
    df.to_csv(file_path, index=False) 
    
    anomalies = df[df['is_anomaly'] == True]
    print(f"Selesai! {len(anomalies)} anomali disimpan ke {file_path}")
    
    return df

if __name__ == "__main__":
    detect_anomalies("market_transactions.csv")