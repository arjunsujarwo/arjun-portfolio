import pandas as pd
from collections import Counter
import re
import matplotlib.pyplot as plt
import os

def analyze_and_plot():
    # 1. Load data dengan proteksi FileNotFoundError
    # Kita cek apakah file ada di folder scripts atau di root
    file_name = 'data_mentah_berita.csv'
    
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
    elif os.path.exists('../' + file_name):
        df = pd.read_csv('../' + file_name)
    else:
        print(f"PERINGATAN: {file_name} tidak ditemukan. Menggunakan data dummy.")
        df = pd.DataFrame({'title': ['tidak ada berita terbaru hari ini']})

    # 2. Gabungkan judul
    all_titles = " ".join(df['title'].astype(str))

    # 3. Cleaning
    words = re.findall(r'\w+', all_titles.lower())
    stopwords = {'dan', 'di', 'ke', 'dari', 'untuk', 'pada', 'dalam', 'yang', 'itu', 'dengan', 'ada', 'buat', 'ini', 'news', 'breaking', 'terbaru'}
    filtered_words = [w for w in words if w not in stopwords and len(w) > 3]

    # 4. Hitung 10 kata teratas
    if not filtered_words:
        filtered_words = ["kosong"]
        
    word_counts = Counter(filtered_words)
    common_words = word_counts.most_common(10)
    
    labels, values = zip(*common_words)

    # 5. Visualisasi
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='skyblue', edgecolor='navy')
    plt.title('Trending Keywords di CNBC Indonesia Hari Ini', fontsize=14)
    plt.ylabel('Frekuensi Muncul')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    
    # Simpan ke folder root agar terbaca oleh index.html
    # Kita simpan ke '../tren_berita.png' karena skrip ini jalan di dalam folder /scripts
    plt.savefig('../tren_berita.png') 
    print("Grafik berhasil disimpan di root folder!")
    
    # plt.show()  <-- WAJIB DIMATIKAN agar GitHub Actions tidak macet
    plt.close() # Menutup plot untuk menghemat memori server

if __name__ == "__main__":
    analyze_and_plot()
