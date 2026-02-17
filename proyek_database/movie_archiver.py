import pandas as pd
import sqlite3
import matplotlib.pyplot as plt # Tambahkan ini di paling atas

def run_movie_pipeline():
    # 1. LOAD DATA DARI KAGGLE
    try:
        df = pd.read_csv('proyek_database/imdb_top_1000.csv')
    except FileNotFoundError:
        print("File csv dari Kaggle tidak ditemukan! Pastikan namanya 'imdb_top_1000.csv'")
        return

    # 2. DATA CLEANING (TRANSFORM)
    # Kita ambil kolom penting saja: Title, Genre, IMDB_Rating, Released_Year, Gross
    df_clean = df[['Series_Title', 'Genre', 'IMDB_Rating', 'Released_Year', 'Gross']].copy()
    
    # Bersihkan kolom Gross (hapus koma dan ubah ke angka)
    df_clean['Gross'] = df_clean['Gross'].str.replace(',', '').fillna(0).astype(float)
    
    # Bersihkan tahun (pastikan angka)
    df_clean['Released_Year'] = pd.to_numeric(df_clean['Released_Year'], errors='coerce')

    # 3. LOAD TO SQLITE
    conn = sqlite3.connect('imdb_movies.db')
    df_clean.to_sql('movies', conn, if_exists='replace', index=False)
    print("Data berhasil masuk ke Database SQL!")

    # 4. SQL QUERY CHALLENGE
    # Cari 5 Genre dengan rata-rata pendapatan tertinggi
    query = """
    SELECT Genre, AVG(Gross) as Average_Gross, COUNT(*) as Total_Movies
    FROM movies
    WHERE Gross > 0
    GROUP BY Genre
    HAVING Total_Movies > 5
    ORDER BY Average_Gross DESC
    LIMIT 5
    """
    
    insight = pd.read_sql_query(query, conn)
    print("\n=== INSIGHT DARI SQL DATABASE ===")
    print(insight)
    # ... (kode sebelumnya) ...
    # 5. VISUALISASI
    plt.figure(figsize=(10, 6))
    plt.barh(insight['Genre'], insight['Average_Gross'], color='skyblue')
    plt.xlabel('Average Gross (in USD)')
    plt.title('Top 5 Most Profitable Movie Genres (SQL Query Result)')
    plt.gca().invert_yaxis() # Biar yang paling tinggi ada di atas
    plt.tight_layout()
    
    # Simpan sebagai gambar untuk web
    plt.savefig('proyek_database/movie_trends.png') 
    print("\nGrafik berhasil disimpan sebagai 'movie_trends.png'!")
    
    plt.show() # Munculkan grafik di layar
    conn.close()

if __name__ == "__main__":
    run_movie_pipeline()
