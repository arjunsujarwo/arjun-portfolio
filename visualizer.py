import pandas as pd
import plotly.graph_objects as go

def create_interactive_chart(file_path):
    df = pd.read_csv(file_path)
    
    # Buat grafik garis untuk harga
    fig = go.Figure()
    
    # Garis Harga Normal
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Market Price', line=dict(color='blue')))
    
    # Titik Anomali (Hanya yang is_anomaly == True)
    anomalies = df[df['is_anomaly'] == True]
    fig.add_trace(go.Scatter(x=anomalies.index, y=anomalies['Close'], 
                             mode='markers', name='Anomaly Detected',
                             marker=dict(color='red', size=10, symbol='x')))
    
    fig.update_layout(title='Real-time Anomaly Detection Dashboard',
                      xaxis_title='Time Index',
                      yaxis_title='Price (USD)',
                      template='plotly_dark')
    
    # SIMPAN SEBAGAI FILE HTML
    fig.write_html("dashboard.html")
    print("Dashboard interaktif berhasil dibuat! Buka file dashboard.html di browser kamu.")

if __name__ == "__main__":
    create_interactive_chart("market_transactions.csv")