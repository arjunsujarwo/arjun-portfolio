import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import Counter
import datetime

def run_scraper():
    url = "https://news.google.com/rss/search?q=when:24h+allinurl:cnbcindonesia.com&hl=id&gl=ID&ceid=ID:id"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    print("Mencoba mengambil berita lewat jalur RSS (Anti-Blokir)...")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.content, 'lxml')
        items = soup.find_all('item')
        
        titles = [item.title.text.replace(' - CNBC Indonesia', '').strip() for item in items]

        if not titles:
            print("Data tidak ditemukan di RSS.")
            return

        # Pengolahan Kata
        all_words = " ".join(titles).lower().split()
        # Tambahkan kata umum lainnya ke stop_words agar hasil lebih berkualitas
        stop_words = ['dan', 'yang', 'untuk', 'pada', 'ke', 'di', 'dari', 'ini', 'itu', 'dengan', 'ada', 'tak', 'bisa', 'dalam', 'akan']
        
        # MEMBERSIHKAN TANDA BACA (Penting agar 'video:' jadi 'video')
        filtered_words = [w.strip(':,."') for w in all_words if len(w) > 3 and w not in stop_words]
        
        counts = Counter(filtered_words).most_common(10)
        words, frequencies = zip(*counts)

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.bar(words, frequencies, color='darkblue')
        
        waktu_sekarang = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        plt.title(f"Tren Berita (via RSS) - Update: {waktu_sekarang} WIB")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # AKTIFKAN KEMBALI SAVEFIG (Tadi ter-comment)
        plt.savefig('tren_berita.png')
        
        # Simpan kata terpopuler ke file teks (Ambil indeks 0 sebagai yang tertinggi)
        top_word = words[0] 
        with open("top_keyword.txt", "w", encoding="utf-8") as f:
            f.write(top_word.capitalize())
            
        print(f"SUKSES! Grafik 'tren_berita.png' dan kata kunci '{top_word}' telah diperbarui.")

    except Exception as e:
        print(f"Gagal di RSS: {e}")

if __name__ == "__main__":
    run_scraper()
