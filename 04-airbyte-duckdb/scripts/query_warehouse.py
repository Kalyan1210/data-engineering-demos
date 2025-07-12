#!/usr/bin/env python3
"""
Query DuckDB warehouse with sample analytics
"""

import duckdb
import pandas as pd
import os

def connect_warehouse():
    """Connect to DuckDB warehouse"""
    return duckdb.connect("data/warehouse/warehouse.db")

def basic_queries(conn):
    """Run basic queries on warehouse data"""
    print("🔍 Running basic queries...")
    
    # Weather data summary
    print("\n🌤️ Weather Data Summary:")
    weather_summary = conn.execute("""
        SELECT 
            COUNT(*) as total_records,
            AVG(temperature) as avg_temperature,
            AVG(humidity) as avg_humidity,
            COUNT(DISTINCT city) as unique_cities
        FROM weather_data
    """).fetchdf()
    print(weather_summary)
    
    # Stock data summary
    print("\n📈 Stock Data Summary:")
    stock_summary = conn.execute("""
        SELECT 
            COUNT(*) as total_records,
            AVG(price) as avg_price,
            SUM(volume) as total_volume,
            COUNT(DISTINCT symbol) as unique_symbols
        FROM stock_data
    """).fetchdf()
    print(stock_summary)
    
    # News data summary
    print("\n📰 News Data Summary:")
    news_summary = conn.execute("""
        SELECT 
            COUNT(*) as total_records,
            COUNT(DISTINCT source) as unique_sources,
            COUNT(DISTINCT category) as unique_categories
        FROM news_data
    """).fetchdf()
    print(news_summary)

def advanced_analytics(conn):
    """Run advanced analytics queries"""
    print("\n📊 Advanced Analytics:")
    
    # Weather analysis by city
    print("\n🌡️ Temperature Analysis by City:")
    weather_analysis = conn.execute("""
        SELECT 
            city,
            temperature,
            humidity,
            description,
            CASE 
                WHEN temperature > 25 THEN 'Hot'
                WHEN temperature > 15 THEN 'Warm'
                ELSE 'Cold'
            END as temperature_category
        FROM weather_data
        ORDER BY temperature DESC
    """).fetchdf()
    print(weather_analysis)
    
    # Stock performance analysis
    print("\n💰 Stock Performance Analysis:")
    stock_analysis = conn.execute("""
        SELECT 
            symbol,
            price,
            volume,
            change_percent,
            CASE 
                WHEN change_percent > 0 THEN 'Positive'
                WHEN change_percent < 0 THEN 'Negative'
                ELSE 'Neutral'
            END as performance
        FROM stock_data
        ORDER BY change_percent DESC
    """).fetchdf()
    print(stock_analysis)
    
    # News category distribution
    print("\n📰 News Category Distribution:")
    news_analysis = conn.execute("""
        SELECT 
            category,
            COUNT(*) as article_count,
            COUNT(DISTINCT source) as source_count
        FROM news_data
        GROUP BY category
        ORDER BY article_count DESC
    """).fetchdf()
    print(news_analysis)

def cross_table_analytics(conn):
    """Run cross-table analytics"""
    print("\n🔗 Cross-Table Analytics:")
    
    # Weather and stock correlation (simulated)
    print("\n🌤️📈 Weather-Stock Correlation (Simulated):")
    correlation_analysis = conn.execute("""
        SELECT 
            w.city,
            w.temperature,
            w.humidity,
            s.symbol,
            s.price,
            s.change_percent
        FROM weather_data w
        CROSS JOIN stock_data s
        WHERE w.city = 'New York' AND s.symbol = 'AAPL'
    """).fetchdf()
    print(correlation_analysis)
    
    # User engagement with news
    print("\n👥📰 User-News Engagement (Simulated):")
    engagement_analysis = conn.execute("""
        SELECT 
            u.name,
            u.city,
            n.category,
            n.title,
            n.source
        FROM users u
        CROSS JOIN news_data n
        WHERE u.city = 'New York' AND n.category = 'Technology'
        LIMIT 3
    """).fetchdf()
    print(engagement_analysis)

def data_quality_checks(conn):
    """Run data quality checks"""
    print("\n🔍 Data Quality Checks:")
    
    # Check for null values
    print("\n❓ Null Value Check:")
    null_check = conn.execute("""
        SELECT 
            'weather_data' as table_name,
            COUNT(*) as total_rows,
            COUNT(CASE WHEN temperature IS NULL THEN 1 END) as null_temperature,
            COUNT(CASE WHEN humidity IS NULL THEN 1 END) as null_humidity
        FROM weather_data
        UNION ALL
        SELECT 
            'stock_data' as table_name,
            COUNT(*) as total_rows,
            COUNT(CASE WHEN price IS NULL THEN 1 END) as null_price,
            COUNT(CASE WHEN volume IS NULL THEN 1 END) as null_volume
        FROM stock_data
    """).fetchdf()
    print(null_check)
    
    # Check for data freshness
    print("\n⏰ Data Freshness Check:")
    freshness_check = conn.execute("""
        SELECT 
            'weather_data' as table_name,
            MAX(timestamp) as latest_update
        FROM weather_data
        UNION ALL
        SELECT 
            'stock_data' as table_name,
            MAX(timestamp) as latest_update
        FROM stock_data
        UNION ALL
        SELECT 
            'news_data' as table_name,
            MAX(published_at) as latest_update
        FROM news_data
    """).fetchdf()
    print(freshness_check)

def export_results(conn):
    """Export query results to files"""
    print("\n📁 Exporting Results...")
    
    os.makedirs("data/exports", exist_ok=True)
    
    # Export weather summary
    weather_summary = conn.execute("""
        SELECT * FROM weather_data
    """).fetchdf()
    weather_summary.to_csv("data/exports/weather_summary.csv", index=False)
    
    # Export stock summary
    stock_summary = conn.execute("""
        SELECT * FROM stock_data
    """).fetchdf()
    stock_summary.to_csv("data/exports/stock_summary.csv", index=False)
    
    # Export news summary
    news_summary = conn.execute("""
        SELECT * FROM news_data
    """).fetchdf()
    news_summary.to_csv("data/exports/news_summary.csv", index=False)
    
    print("✅ Results exported to data/exports/")

def main():
    """Main query function"""
    print("🚀 Querying DuckDB warehouse...")
    
    # Connect to warehouse
    conn = connect_warehouse()
    
    # Run different types of queries
    basic_queries(conn)
    advanced_analytics(conn)
    cross_table_analytics(conn)
    data_quality_checks(conn)
    export_results(conn)
    
    conn.close()
    
    print("\n🎉 Warehouse queries completed!")
    print("📊 Query results:")
    print("   - Basic summaries generated")
    print("   - Advanced analytics completed")
    print("   - Cross-table analysis performed")
    print("   - Data quality checks run")
    print("   - Results exported to data/exports/")

if __name__ == "__main__":
    main() 