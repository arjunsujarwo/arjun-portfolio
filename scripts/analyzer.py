# import pandas as pd
# from collections import Counter
# import re

# def analyze_data():
#     # 1. Load data hasil scraping
#     try:
#         df = pd.read_csv('data_mentah_berita.csv')
#     except FileNotFoundError:
#         print("File data_mentah_berita.csv tidak ditemukan! Jalankan scraper.py dulu.")
#         return

#     # 2. Gabungkan semua judul menjadi satu teks besar
#     all_titles = " ".join(df['title'].astype(str))

#     # 3. Pembersihan sederhana (Cleaning)
#     # Ubah ke huruf kecil dan hapus tanda baca
#     words = re.findall(r'\w+', all_titles.lower())

#     # 4. Filter Kata Sambung (Stopwords sederhana)
#     # Kita tidak ingin kata "di", "ke", "dan" menjadi pemenang
#     stopwords = {'dan', 'di', 'ke', 'dari', 'untuk', 'pada', 'dalam', 'yang', 'itu', 'dengan', 'ada', 'buat', 'ini'}
#     filtered_words = [w for w in words if w not in stopwords and len(w) > 3]

#     # 5. Hitung frekuensi kata
#     word_counts = Counter(filtered_words)
#     common_words = word_counts.most_common(5) # Ambil 5 teratas

#     print("=== HASIL ANALISIS TREN BERITA ===")
#     for word, count in common_words:
#         print(f"Kata '{word}' muncul sebanyak {count} kali")

# if __name__ == "__main__":
#     analyze_data()

import pandas as pd
from collections import Counter
import re
import matplotlib.pyplot as plt

def analyze_and_plot():
    # 1. Load data
    df = pd.read_csv('data_mentah_berita.csv')
    all_titles = " ".join(df['title'].astype(str))

    # 2. Cleaning
    words = re.findall(r'\w+', all_titles.lower())
    stopwords = {'dan', 'di', 'ke', 'dari', 'untuk', 'pada', 'dalam', 'yang', 'itu', 'dengan', 'ada', 'buat', 'ini', 'news', 'breaking'}
    filtered_words = [w for w in words if w not in stopwords and len(w) > 3]

    # 3. Hitung 10 kata teratas
    word_counts = Counter(filtered_words)
    common_words = word_counts.most_common(10)
    
    # Pisahkan kata dan jumlahnya untuk grafik
    labels, values = zip(*common_words)

    # 4. Membuat Grafik (Visualisasi)
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='skyblue', edgecolor='navy')
    plt.title('Trending Keywords di CNBC Indonesia Hari Ini', fontsize=14)
    plt.xlabel('Kata Kunci', fontsize=12)
    plt.ylabel('Frekuensi Muncul', fontsize=12)
    plt.xticks(rotation=45)
    
    # Simpan sebagai gambar untuk web portofolio
    plt.tight_layout()
    plt.savefig('tren_berita.png') 
    print("Grafik berhasil disimpan dengan nama 'tren_berita.png'!")
    plt.show()

if __name__ == "__main__":
    analyze_and_plot()
