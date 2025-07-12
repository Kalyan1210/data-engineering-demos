#!/usr/bin/env python3
"""
Setup DuckDB data warehouse
"""

import duckdb
import pandas as pd
import os
from datetime import datetime

def setup_warehouse():
    """Initialize DuckDB warehouse"""
    print("🦆 Setting up DuckDB warehouse...")
    
    # Create data directories
    os.makedirs("data/warehouse", exist_ok=True)
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    
    # Connect to DuckDB
    conn = duckdb.connect("data/warehouse/warehouse.db")
    
    # Create tables
    create_tables(conn)
    
    # Insert sample data
    insert_sample_data(conn)
    
    conn.close()
    print("✅ DuckDB warehouse setup complete!")

def create_tables(conn):
    """Create warehouse tables"""
    print("📋 Creating warehouse tables...")
    
    # Weather data table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY,
            city VARCHAR,
            temperature FLOAT,
            humidity INTEGER,
            description VARCHAR,
            timestamp TIMESTAMP
        )
    """)
    
    # Stock data table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS stock_data (
            id INTEGER PRIMARY KEY,
            symbol VARCHAR,
            price FLOAT,
            volume INTEGER,
            change_percent FLOAT,
            timestamp TIMESTAMP
        )
    """)
    
    # News data table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS news_data (
            id INTEGER PRIMARY KEY,
            title VARCHAR,
            content TEXT,
            source VARCHAR,
            published_at TIMESTAMP,
            category VARCHAR
        )
    """)
    
    # Users table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name VARCHAR,
            email VARCHAR,
            age INTEGER,
            city VARCHAR,
            created_at TIMESTAMP
        )
    """)
    
    print("✅ Tables created successfully!")

def insert_sample_data(conn):
    """Insert sample data into tables"""
    print("📊 Inserting sample data...")
    
    # Sample weather data
    weather_data = [
        (1, "New York", 22.5, 65, "Partly Cloudy", "2024-01-15 10:00:00"),
        (2, "Los Angeles", 28.0, 45, "Sunny", "2024-01-15 10:00:00"),
        (3, "Chicago", 15.2, 70, "Cloudy", "2024-01-15 10:00:00"),
        (4, "Miami", 30.5, 80, "Humid", "2024-01-15 10:00:00"),
        (5, "Seattle", 12.8, 85, "Rainy", "2024-01-15 10:00:00")
    ]
    
    conn.execute("DELETE FROM weather_data")
    conn.executemany("""
        INSERT INTO weather_data VALUES (?, ?, ?, ?, ?, ?)
    """, weather_data)
    
    # Sample stock data
    stock_data = [
        (1, "AAPL", 150.25, 1000000, 2.5, "2024-01-15 10:00:00"),
        (2, "GOOGL", 2800.50, 500000, -1.2, "2024-01-15 10:00:00"),
        (3, "MSFT", 320.75, 750000, 0.8, "2024-01-15 10:00:00"),
        (4, "TSLA", 250.00, 1200000, 5.2, "2024-01-15 10:00:00"),
        (5, "AMZN", 3300.25, 300000, -0.5, "2024-01-15 10:00:00")
    ]
    
    conn.execute("DELETE FROM stock_data")
    conn.executemany("""
        INSERT INTO stock_data VALUES (?, ?, ?, ?, ?, ?)
    """, stock_data)
    
    # Sample news data
    news_data = [
        (1, "Tech Innovation", "New AI breakthrough...", "Tech News", "2024-01-15 09:00:00", "Technology"),
        (2, "Market Update", "Stock market trends...", "Financial Times", "2024-01-15 08:30:00", "Finance"),
        (3, "Weather Alert", "Severe weather warning...", "Weather Service", "2024-01-15 08:00:00", "Weather"),
        (4, "Sports News", "Championship results...", "Sports Daily", "2024-01-15 07:30:00", "Sports"),
        (5, "Health Update", "Medical breakthrough...", "Health Journal", "2024-01-15 07:00:00", "Health")
    ]
    
    conn.execute("DELETE FROM news_data")
    conn.executemany("""
        INSERT INTO news_data VALUES (?, ?, ?, ?, ?, ?)
    """, news_data)
    
    # Sample users data
    users_data = [
        (1, "John Doe", "john@email.com", 30, "New York", "2024-01-01 10:00:00"),
        (2, "Jane Smith", "jane@email.com", 25, "Los Angeles", "2024-01-02 11:00:00"),
        (3, "Bob Johnson", "bob@email.com", 35, "Chicago", "2024-01-03 12:00:00"),
        (4, "Alice Brown", "alice@email.com", 28, "Miami", "2024-01-04 13:00:00"),
        (5, "Charlie Wilson", "charlie@email.com", 32, "Seattle", "2024-01-05 14:00:00")
    ]
    
    conn.execute("DELETE FROM users")
    conn.executemany("""
        INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)
    """, users_data)
    
    print("✅ Sample data inserted successfully!")

if __name__ == "__main__":
    setup_warehouse() 