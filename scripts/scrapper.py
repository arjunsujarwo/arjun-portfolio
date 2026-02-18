import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import Counter
import datetime

def run_scraper():
    url = "https://www.cnbcindonesia.com/news/indeks/3"
    
    # KUNCI UTAMA: Menyamar sebagai browser Chrome di Windows
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    print("Sedang mencoba mengambil data dari CNBC Indonesia...")
    
    try:
        # Gunakan headers dalam requests.get
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('h2')
        
        titles = [a.text.strip() for a in articles if len(a.text.strip()) > 10]

        if not titles:
            print("Data masih kosong. Struktur HTML mungkin berubah.")
            return

        # Pengolahan Kata kunci
        all_words = " ".join(titles).lower().split()
        stop_words = ['dan', 'yang', 'untuk', 'pada', 'ke', 'di', 'dari', 'ini', 'itu', 'dengan']
        filtered_words = [w for w in all_words if len(w) > 3 and w not in stop_words]
        
        counts = Counter(filtered_words).most_common(10)
        words, frequencies = zip(*counts)

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.bar(words, frequencies, color='darkred')
        
        # Tambahkan waktu di judul agar file selalu dianggap "berubah" oleh Git
        waktu_sekarang = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        plt.title(f"Tren Kata Berita CNBC - Update: {waktu_sekarang} WIB")
        
        plt.savefig('tren_berita.png')
        print(f"Akses berhasil! Grafik diperbarui pada {waktu_sekarang}")

    except Exception as e:
        print(f"Gagal total: {e}")

if __name__ == "__main__":
    run_scraper()

