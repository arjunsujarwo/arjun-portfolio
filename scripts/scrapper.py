import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import Counter
import datetime
import pandas as pd # Tambahkan pandas

def run_scraper():
    url = "https://news.google.com/rss/search?q=when:24h+allinurl:cnbcindonesia.com&hl=id&gl=ID&ceid=ID:id"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    print("Mencoba mengambil berita lewat jalur RSS (Anti-Blokir)...")
    
    titles = [] # Inisialisasi list kosong

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.content, 'xml') # Sudah pakai xml
        items = soup.find_all('item')
        
        titles = [item.title.text.replace(' - CNBC Indonesia', '').strip() for item in items]

    except Exception as e:
        print(f"Gagal mengambil data dari RSS: {e}")

    # --- BAGIAN KRUSIAL: ALWAYS SAVE CSV ---
    # Jika titles kosong, kita buat data placeholder agar analyzer.py tidak error
    data_to_save = titles if titles else ["Tidak ada berita terbaru"]
    df = pd.DataFrame(data_to_save, columns=['title'])
    
    # Simpan ke folder root agar sinkron dengan skrip lainnya
    df.to_csv('../data_mentah_berita.csv', index=False)
    print(f"File 'data_mentah_berita.csv' berhasil diperbarui dengan {len(titles)} berita.")

    # --- VISUALISASI ---
    if titles:
        all_words = " ".join(titles).lower().split()
        stop_words = ['dan', 'yang', 'untuk', 'pada', 'ke', 'di', 'dari', 'ini', 'itu', 'dengan', 'ada', 'tak', 'bisa', 'dalam', 'akan', 'oleh', 'adalah']
        
        filtered_words = [w.strip(':,."') for w in all_words if len(w) > 3 and w not in stop_words]
        
        if filtered_words:
            counts = Counter(filtered_words).most_common(10)
            words, frequencies = zip(*counts)

            plt.figure(figsize=(10, 6))
            plt.bar(words, frequencies, color='darkblue')
            
            waktu_sekarang = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            plt.title(f"Tren Berita (via RSS) - Update: {waktu_sekarang} WIB")
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Simpan grafik ke folder root
            plt.savefig('../tren_berita.png')
            plt.close() # Tutup agar tidak memakan RAM GitHub
            
            # Simpan kata terpopuler
            top_word = words[0] 
            with open("../top_keyword.txt", "w", encoding="utf-8") as f:
                f.write(top_word.capitalize())
            
            print(f"Grafik dan top_keyword berhasil diperbarui.")
    else:
        print("Grafik tidak diperbarui karena tidak ada data berita.")

if __name__ == "__main__":
    run_scraper()
