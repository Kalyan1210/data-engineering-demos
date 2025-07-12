#!/usr/bin/env python3
"""
Run data replication from APIs to DuckDB
"""

import requests
import pandas as pd
import duckdb
import json
import os
from datetime import datetime
import time

def fetch_weather_data():
    """Fetch weather data from API"""
    print("🌤️ Fetching weather data...")
    
    # Simulate API call (in real scenario, use actual weather API)
    weather_data = [
        {"city": "New York", "temperature": 22.5, "humidity": 65, "description": "Partly Cloudy"},
        {"city": "Los Angeles", "temperature": 28.0, "humidity": 45, "description": "Sunny"},
        {"city": "Chicago", "temperature": 15.2, "humidity": 70, "description": "Cloudy"},
        {"city": "Miami", "temperature": 30.5, "humidity": 80, "description": "Humid"},
        {"city": "Seattle", "temperature": 12.8, "humidity": 85, "description": "Rainy"}
    ]
    
    # Save raw data
    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/weather_data.json", "w") as f:
        json.dump(weather_data, f, indent=2)
    
    return weather_data

def fetch_stock_data():
    """Fetch stock data from API"""
    print("📈 Fetching stock data...")
    
    # Simulate API call (in real scenario, use actual stock API)
    stock_data = [
        {"symbol": "AAPL", "price": 150.25, "volume": 1000000, "change_percent": 2.5},
        {"symbol": "GOOGL", "price": 2800.50, "volume": 500000, "change_percent": -1.2},
        {"symbol": "MSFT", "price": 320.75, "volume": 750000, "change_percent": 0.8},
        {"symbol": "TSLA", "price": 250.00, "volume": 1200000, "change_percent": 5.2},
        {"symbol": "AMZN", "price": 3300.25, "volume": 300000, "change_percent": -0.5}
    ]
    
    # Save raw data
    with open("data/raw/stock_data.json", "w") as f:
        json.dump(stock_data, f, indent=2)
    
    return stock_data

def fetch_news_data():
    """Fetch news data from API"""
    print("📰 Fetching news data...")
    
    # Simulate API call (in real scenario, use actual news API)
    news_data = [
        {"title": "Tech Innovation", "content": "New AI breakthrough...", "source": "Tech News", "category": "Technology"},
        {"title": "Market Update", "content": "Stock market trends...", "source": "Financial Times", "category": "Finance"},
        {"title": "Weather Alert", "content": "Severe weather warning...", "source": "Weather Service", "category": "Weather"},
        {"title": "Sports News", "content": "Championship results...", "source": "Sports Daily", "category": "Sports"},
        {"title": "Health Update", "content": "Medical breakthrough...", "source": "Health Journal", "category": "Health"}
    ]
    
    # Save raw data
    with open("data/raw/news_data.json", "w") as f:
        json.dump(news_data, f, indent=2)
    
    return news_data

def transform_data(weather_data, stock_data, news_data):
    """Transform raw data for warehouse"""
    print("🔄 Transforming data...")
    
    # Transform weather data
    weather_df = pd.DataFrame(weather_data)
    weather_df['timestamp'] = datetime.now()
    weather_df['id'] = range(1, len(weather_df) + 1)
    
    # Transform stock data
    stock_df = pd.DataFrame(stock_data)
    stock_df['timestamp'] = datetime.now()
    stock_df['id'] = range(1, len(stock_df) + 1)
    
    # Transform news data
    news_df = pd.DataFrame(news_data)
    news_df['published_at'] = datetime.now()
    news_df['id'] = range(1, len(news_df) + 1)
    
    # Save processed data
    os.makedirs("data/processed", exist_ok=True)
    weather_df.to_csv("data/processed/weather_processed.csv", index=False)
    stock_df.to_csv("data/processed/stock_processed.csv", index=False)
    news_df.to_csv("data/processed/news_processed.csv", index=False)
    
    return weather_df, stock_df, news_df

def load_to_warehouse(weather_df, stock_df, news_df):
    """Load data into DuckDB warehouse"""
    print("📦 Loading data into warehouse...")
    
    # Connect to DuckDB
    conn = duckdb.connect("data/warehouse/warehouse.db")
    
    # Load weather data
    conn.execute("DELETE FROM weather_data")
    conn.execute("""
        INSERT INTO weather_data 
        SELECT * FROM weather_df
    """)
    
    # Load stock data
    conn.execute("DELETE FROM stock_data")
    conn.execute("""
        INSERT INTO stock_data 
        SELECT * FROM stock_df
    """)
    
    # Load news data
    conn.execute("DELETE FROM news_data")
    conn.execute("""
        INSERT INTO news_data 
        SELECT * FROM news_df
    """)
    
    conn.close()
    print("✅ Data loaded into warehouse successfully!")

def main():
    """Main replication process"""
    print("🚀 Starting data replication process...")
    
    # Fetch data from APIs
    weather_data = fetch_weather_data()
    stock_data = fetch_stock_data()
    news_data = fetch_news_data()
    
    # Transform data
    weather_df, stock_df, news_df = transform_data(weather_data, stock_data, news_data)
    
    # Load to warehouse
    load_to_warehouse(weather_df, stock_df, news_df)
    
    print("\n🎉 Data replication completed!")
    print("📊 Data sources processed:")
    print("   - Weather data: 5 records")
    print("   - Stock data: 5 records")
    print("   - News data: 5 records")
    print("📁 Files created:")
    print("   - Raw data: data/raw/")
    print("   - Processed data: data/processed/")
    print("   - Warehouse: data/warehouse/warehouse.db")

if __name__ == "__main__":
    main() 