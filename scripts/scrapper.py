import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_cnbc():
    # URL berita terkini CNBC Indonesia
    url = "https://www.cnbcindonesia.com/news/indeks/3"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    print(f"Sedang mencoba mengambil data dari CNBC Indonesia...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Cek apakah koneksi sukses
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # CNBC menggunakan list berita di dalam class 'list media_rows'
        articles = soup.find_all('article')
        
        news_list = []
        for article in articles:
            title_tag = article.find('h2') # Judul biasanya di h2
            if title_tag:
                title = title_tag.text.strip()
                # Mencari link yang ada di dalam artikel tersebut
                link = article.find('a')['href'] if article.find('a') else "No Link"
                
                news_list.append({
                    'title': title,
                    'link': link,
                    'scraped_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        
        return pd.DataFrame(news_list)
        
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None

if __name__ == "__main__":
    df_berita = scrape_cnbc()
    
    if df_berita is not None and not df_berita.empty:
        # Menyimpan hasil
        df_berita.to_csv('data_mentah_berita.csv', index=False)
        print(f"BERHASIL! {len(df_berita)} berita berhasil diamankan.")
        print("-" * 30)
        print(df_berita['title'].head()) # Tampilkan 5 judul teratas
    else:
        print("Data masih kosong. Website mungkin sedang memblokir akses otomatis.")
