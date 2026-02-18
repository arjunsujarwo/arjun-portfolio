import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd # Tambahkan ini jika belum ada

def run_scraper():
    url = "https://www.cnbcindonesia.com/news/indeks/3"
    
    # INI KUNCINYA: Menyamar sebagai browser Chrome manusia
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    print("Sedang mencoba mengambil data dari CNBC Indonesia...")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # Cari judul berita (Struktur CNBC biasanya di h2 atau h3 di dalam list)
        articles = soup.find_all('h2')
        
        titles = [a.text.strip() for a in articles if len(a.text.strip()) > 10]

        if not titles:
            print("Data masih kosong. Struktur HTML mungkin berubah.")
            return

        # Ambil 10 kata kunci terpopuler
        all_words = " ".join(titles).lower().split()
        stop_words = ['dan', 'yang', 'untuk', 'pada', 'ke', 'di', 'dari', 'ini', 'itu', 'dengan']
        filtered_words = [w for w in all_words if len(w) > 3 and w not in stop_words]
        
        counts = Counter(filtered_words).most_common(10)
        words, frequencies = zip(*counts)

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.bar(words, frequencies, color='darkred') # Warna merah khas CNBC
        plt.title(f"Update: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')} WIB")
        plt.ylabel("Frekuensi Muncul")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Simpan di folder utama agar terbaca index.html
        plt.savefig('tren_berita.png')
        print("Akses berhasil! Grafik 'tren_berita.png' diperbarui.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_scraper()

