import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import Counter
import os

def run_scraper():
    url = "https://www.cnbcindonesia.com/news/indeks/3"
    
    # 1. Menambahkan Headers agar tidak terkena Error 403 (Forbidden)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    print("Sedang mencoba mengambil data dari CNBC Indonesia...")
    
    try:
        # Mengirim permintaan dengan headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')
        
        titles = []
        for article in articles:
            title_tag = article.find('h2')
            if title_tag:
                titles.append(title_tag.text.strip())

        if not titles:
            print("Data masih kosong. Struktur HTML mungkin berubah.")
            return

        # 2. Pengolahan Data (Contoh: Menghitung kata kunci)
        all_words = " ".join(titles).lower().split()
        # Filter kata-kata umum (optional)
        stop_words = ['di', 'ke', 'dan', 'ini', 'itu', 'yang', 'untuk', 'dari']
        filtered_words = [w for w in all_words if len(w) > 3 and w not in stop_words]
        
        counts = Counter(filtered_words).most_common(10)
        words, frequencies = zip(*counts)

        # 3. Membuat Grafik
        plt.figure(figsize=(10, 6))
        plt.bar(words, frequencies, color='skyblue', edgecolor='black')
        plt.title(f"Tren Kata Kunci Berita CNBC Indonesia (Update: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')})")
        plt.xlabel("Kata Kunci")
        plt.ylabel("Frekuensi")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # 4. Menyimpan Gambar (Pastikan nama file sesuai dengan index.html)
        # Kita simpan di folder utama agar GitHub Pages mudah membacanya
        plt.savefig('tren_berita.png')
        print("Akses berhasil! Grafik 'tren_berita.png' telah diperbarui.")

    except requests.exceptions.HTTPError as err:
        print(f"Terjadi kesalahan HTTP: {err}")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    run_scraper()
