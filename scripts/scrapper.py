import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import Counter
import datetime

def run_scraper():
    # Jalur RSS Google News untuk CNBC Indonesia
    url = "https://news.google.com/rss/search?q=when:24h+allinurl:cnbcindonesia.com&hl=id&gl=ID&ceid=ID:id"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    print("Mencoba mengambil berita lewat jalur RSS (Anti-Blokir)...")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        
        # Parse XML (RSS menggunakan format XML)
        soup = BeautifulSoup(response.content, 'lxml')
        items = soup.find_all('item')
        
        titles = [item.title.text.replace(' - CNBC Indonesia', '').strip() for item in items]

        if not titles:
            print("Data tidak ditemukan di RSS.")
            return

        # Pengolahan Kata
        all_words = " ".join(titles).lower().split()
        stop_words = ['dan', 'yang', 'untuk', 'pada', 'ke', 'di', 'dari', 'ini', 'itu', 'dengan', 'ada', 'tak', 'bisa']
        filtered_words = [w for w in all_words if len(w) > 3 and w not in stop_words]
        
        counts = Counter(filtered_words).most_common(10)
        words, frequencies = zip(*counts)

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.bar(words, frequencies, color='darkblue')
        
        waktu_sekarang = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        plt.title(f"Tren Berita (via RSS) - Update: {waktu_sekarang} WIB")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # plt.savefig('tren_berita.png')
        # # ... (kode plotting sebelumnya) ...
        # plt.savefig('tren_berita.png')
        
        # TAMBAHKAN INI: Simpan kata terpopuler ke file teks
        top_word = words[0] # Mengambil kata dengan frekuensi tertinggi
        with open("top_keyword.txt", "w") as f:
            f.write(top_word.capitalize())
            
        print(f"SUKSES! Grafik dan kata kunci '{top_word}' telah diperbarui.")
        # print(f"SUKSES! Grafik diperbarui via RSS pada {waktu_sekarang}")

    except Exception as e:
        print(f"Gagal lagi di RSS: {e}")

if __name__ == "__main__":
    run_scraper()
