#!/usr/bin/env python3
"""
ETL Assets
Demonstrates ETL pipeline using Dagster assets with transformations and data processing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import logging
from dagster import asset, AssetExecutionContext, MetadataValue
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asset(
    description="Transformed sales data with business logic",
    group_name="data_transformation",
    deps=["validated_sales_data"]
)
def transformed_sales_data(context: AssetExecutionContext, validated_sales_data: pd.DataFrame) -> pd.DataFrame:
    """Transform sales data with business logic"""
    context.log.info("Transforming sales data...")
    
    # Apply business transformations
    df = validated_sales_data.copy()
    
    # Add derived columns
    df['month'] = df['sale_date'].dt.month
    df['year'] = df['sale_date'].dt.year
    df['day_of_week'] = df['sale_date'].dt.dayofweek
    df['quarter'] = df['sale_date'].dt.quarter
    df['is_weekend'] = df['sale_date'].dt.dayofweek >= 5
    
    # Calculate business metrics
    df['profit_margin'] = df['total_amount'] * 0.3  # Assume 30% margin
    df['revenue_per_unit'] = df['total_amount'] / df['quantity']
    df['profit_per_unit'] = df['profit_margin'] / df['quantity']
    
    # Add seasonality indicators
    df['is_holiday_season'] = df['month'].isin([11, 12])  # November and December
    df['is_summer'] = df['month'].isin([6, 7, 8])  # Summer months
    
    # Save transformed data
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/sales_transformed.csv', index=False)
    
    # Add metadata
    context.add_output_metadata({
        "total_records": MetadataValue.int(len(df)),
        "total_revenue": MetadataValue.float(df['total_amount'].sum()),
        "total_profit": MetadataValue.float(df['profit_margin'].sum()),
        "avg_order_value": MetadataValue.float(df['total_amount'].mean()),
        "date_range": MetadataValue.text(f"{df['sale_date'].min()} to {df['sale_date'].max()}"),
        "file_path": MetadataValue.text('data/processed/sales_transformed.csv')
    })
    
    context.log.info(f"Transformed {len(df)} sales records")
    return df

@asset(
    description="Transformed customer data with enriched features",
    group_name="data_transformation",
    deps=["validated_customer_data"]
)
def transformed_customer_data(context: AssetExecutionContext, validated_customer_data: pd.DataFrame) -> pd.DataFrame:
    """Transform customer data with enriched features"""
    context.log.info("Transforming customer data...")
    
    # Apply business transformations
    df = validated_customer_data.copy()
    
    # Add derived columns
    df['full_name'] = df['first_name'] + ' ' + df['last_name']
    df['age_group'] = pd.cut(df['age'], 
                             bins=[0, 25, 35, 50, 65, 100], 
                             labels=['18-25', '26-35', '36-50', '51-65', '65+'])
    df['customer_lifetime_days'] = (datetime.now() - df['registration_date']).dt.days
    df['customer_lifetime_years'] = df['customer_lifetime_days'] / 365.25
    
    # Add customer scoring
    df['customer_score'] = np.where(df['customer_segment'] == 'Platinum', 100,
                                   np.where(df['customer_segment'] == 'Gold', 80,
                                           np.where(df['customer_segment'] == 'Silver', 60, 40)))
    
    # Add income level scoring
    income_scores = {'Low': 1, 'Medium': 2, 'High': 3}
    df['income_score'] = df['income_level'].map(income_scores)
    
    # Calculate customer value index
    df['customer_value_index'] = (df['customer_score'] * 0.6 + 
                                 df['income_score'] * 0.3 + 
                                 (df['customer_lifetime_years'] * 10) * 0.1)
    
    # Save transformed data
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/customers_transformed.csv', index=False)
    
    # Add metadata
    context.add_output_metadata({
        "total_records": MetadataValue.int(len(df)),
        "unique_segments": MetadataValue.int(df['customer_segment'].nunique()),
        "avg_age": MetadataValue.float(df['age'].mean()),
        "avg_customer_value": MetadataValue.float(df['customer_value_index'].mean()),
        "file_path": MetadataValue.text('data/processed/customers_transformed.csv')
    })
    
    context.log.info(f"Transformed {len(df)} customer records")
    return df

@asset(
    description="Transformed product data with business metrics",
    group_name="data_transformation",
    deps=["validated_product_data"]
)
def transformed_product_data(context: AssetExecutionContext, validated_product_data: pd.DataFrame) -> pd.DataFrame:
    """Transform product data with business metrics"""
    context.log.info("Transforming product data...")
    
    # Apply business transformations
    df = validated_product_data.copy()
    
    # Add derived columns
    df['profit_margin'] = df['price'] - df['cost']
    df['profit_margin_pct'] = (df['profit_margin'] / df['price']) * 100
    df['inventory_value'] = df['price'] * df['inventory']
    df['inventory_status'] = np.where(df['inventory'] > 10, 'In Stock', 
                                     np.where(df['inventory'] > 0, 'Low Stock', 'Out of Stock'))
    
    # Add product scoring
    df['product_score'] = (df['profit_margin_pct'] * 0.4 + 
                          (100 - df['inventory']) * 0.3 + 
                          df['price'] * 0.3)
    
    # Add category performance metrics
    category_metrics = df.groupby('category').agg({
        'price': 'mean',
        'profit_margin': 'sum',
        'inventory': 'sum'
    }).round(2)
    
    # Save transformed data
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/products_transformed.csv', index=False)
    
    # Add metadata
    context.add_output_metadata({
        "total_records": MetadataValue.int(len(df)),
        "unique_categories": MetadataValue.int(df['category'].nunique()),
        "avg_price": MetadataValue.float(df['price'].mean()),
        "avg_profit_margin": MetadataValue.float(df['profit_margin_pct'].mean()),
        "total_inventory_value": MetadataValue.float(df['inventory_value'].sum()),
        "file_path": MetadataValue.text('data/processed/products_transformed.csv')
    })
    
    context.log.info(f"Transformed {len(df)} product records")
    return df

@asset(
    description="Enriched sales data with customer and product information",
    group_name="data_integration",
    deps=["transformed_sales_data", "transformed_customer_data", "transformed_product_data"]
)
def enriched_sales_data(
    context: AssetExecutionContext,
    transformed_sales_data: pd.DataFrame,
    transformed_customer_data: pd.DataFrame,
    transformed_product_data: pd.DataFrame
) -> pd.DataFrame:
    """Enrich sales data with customer and product information"""
    context.log.info("Enriching sales data...")
    
    # Merge sales with customer data
    df = transformed_sales_data.merge(
        transformed_customer_data[['customer_id', 'customer_segment', 'age_group', 'customer_value_index']],
        on='customer_id',
        how='left'
    )
    
    # Merge with product data
    df = df.merge(
        transformed_product_data[['product_id', 'category', 'brand', 'profit_margin_pct', 'inventory_status']],
        on='product_id',
        how='left'
    )
    
    # Add business insights
    df['customer_product_match'] = np.where(
        (df['customer_segment'] == 'Platinum') & (df['category'].isin(['Electronics', 'Beauty'])), 'Premium Match',
        np.where(df['customer_segment'] == 'Gold', 'Gold Match', 'Standard Match')
    )
    
    # Calculate customer lifetime value contribution
    df['clv_contribution'] = df['total_amount'] * df['customer_value_index'] / 100
    
    # Save enriched data
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/sales_enriched.csv', index=False)
    
    # Add metadata
    context.add_output_metadata({
        "total_records": MetadataValue.int(len(df)),
        "unique_customers": MetadataValue.int(df['customer_id'].nunique()),
        "unique_products": MetadataValue.int(df['product_id'].nunique()),
        "total_revenue": MetadataValue.float(df['total_amount'].sum()),
        "total_clv_contribution": MetadataValue.float(df['clv_contribution'].sum()),
        "file_path": MetadataValue.text('data/processed/sales_enriched.csv')
    })
    
    context.log.info(f"Enriched {len(df)} sales records")
    return df

@asset(
    description="Customer analytics with purchase behavior insights",
    group_name="analytics",
    deps=["enriched_sales_data"]
)
def customer_analytics(context: AssetExecutionContext, enriched_sales_data: pd.DataFrame) -> Dict[str, Any]:
    """Generate customer analytics and insights"""
    context.log.info("Generating customer analytics...")
    
    # Customer segment analysis
    segment_analysis = enriched_sales_data.groupby('customer_segment').agg({
        'sale_id': 'count',
        'total_amount': 'sum',
        'customer_id': 'nunique',
        'profit_margin': 'sum'
    }).rename(columns={
        'sale_id': 'total_orders',
        'customer_id': 'unique_customers',
        'profit_margin': 'total_profit'
    })
    
    # Age group analysis
    age_analysis = enriched_sales_data.groupby('age_group').agg({
        'sale_id': 'count',
        'total_amount': 'sum',
        'customer_id': 'nunique'
    }).rename(columns={
        'sale_id': 'total_orders',
        'customer_id': 'unique_customers'
    })
    
    # Product category preferences by segment
    category_preferences = enriched_sales_data.groupby(['customer_segment', 'category']).agg({
        'sale_id': 'count',
        'total_amount': 'sum'
    }).reset_index()
    
    # Top customers by revenue
    top_customers = enriched_sales_data.groupby('customer_id').agg({
        'total_amount': 'sum',
        'sale_id': 'count',
        'customer_segment': 'first'
    }).sort_values('total_amount', ascending=False).head(10)
    
    # Analytics summary
    analytics = {
        'timestamp': datetime.now().isoformat(),
        'segment_analysis': segment_analysis.to_dict(),
        'age_analysis': age_analysis.to_dict(),
        'category_preferences': category_preferences.to_dict('records'),
        'top_customers': top_customers.to_dict('records'),
        'summary': {
            'total_customers': enriched_sales_data['customer_id'].nunique(),
            'total_revenue': enriched_sales_data['total_amount'].sum(),
            'total_profit': enriched_sales_data['profit_margin'].sum(),
            'avg_order_value': enriched_sales_data['total_amount'].mean()
        }
    }
    
    # Save analytics
    os.makedirs('data/analytics', exist_ok=True)
    import json
    with open('data/analytics/customer_analytics.json', 'w') as f:
        json.dump(analytics, f, indent=2)
    
    # Add metadata
    context.add_output_metadata({
        "total_customers": MetadataValue.int(analytics['summary']['total_customers']),
        "total_revenue": MetadataValue.float(analytics['summary']['total_revenue']),
        "total_profit": MetadataValue.float(analytics['summary']['total_profit']),
        "avg_order_value": MetadataValue.float(analytics['summary']['avg_order_value']),
        "file_path": MetadataValue.text('data/analytics/customer_analytics.json')
    })
    
    context.log.info("Customer analytics generated successfully")
    return analytics

@asset(
    description="Product performance analytics with inventory insights",
    group_name="analytics",
    deps=["enriched_sales_data", "transformed_product_data"]
)
def product_analytics(
    context: AssetExecutionContext,
    enriched_sales_data: pd.DataFrame,
    transformed_product_data: pd.DataFrame
) -> Dict[str, Any]:
    """Generate product performance analytics"""
    context.log.info("Generating product analytics...")
    
    # Product performance analysis
    product_performance = enriched_sales_data.groupby(['product_id', 'category', 'brand']).agg({
        'sale_id': 'count',
        'total_amount': 'sum',
        'quantity': 'sum',
        'profit_margin': 'sum'
    }).reset_index()
    
    # Category performance
    category_performance = enriched_sales_data.groupby('category').agg({
        'sale_id': 'count',
        'total_amount': 'sum',
        'profit_margin': 'sum',
        'customer_id': 'nunique'
    }).rename(columns={
        'sale_id': 'total_orders',
        'customer_id': 'unique_customers'
    })
    
    # Brand performance
    brand_performance = enriched_sales_data.groupby('brand').agg({
        'sale_id': 'count',
        'total_amount': 'sum',
        'profit_margin': 'sum'
    }).rename(columns={
        'sale_id': 'total_orders'
    })
    
    # Inventory analysis
    inventory_analysis = transformed_product_data.groupby('inventory_status').agg({
        'product_id': 'count',
        'inventory_value': 'sum',
        'profit_margin': 'sum'
    }).rename(columns={
        'product_id': 'product_count'
    })
    
    # Top performing products
    top_products = product_performance.sort_values('total_amount', ascending=False).head(10)
    
    # Analytics summary
    analytics = {
        'timestamp': datetime.now().isoformat(),
        'product_performance': product_performance.to_dict('records'),
        'category_performance': category_performance.to_dict(),
        'brand_performance': brand_performance.to_dict(),
        'inventory_analysis': inventory_analysis.to_dict(),
        'top_products': top_products.to_dict('records'),
        'summary': {
            'total_products': len(transformed_product_data),
            'total_categories': transformed_product_data['category'].nunique(),
            'total_brands': transformed_product_data['brand'].nunique(),
            'total_inventory_value': transformed_product_data['inventory_value'].sum()
        }
    }
    
    # Save analytics
    os.makedirs('data/analytics', exist_ok=True)
    import json
    with open('data/analytics/product_analytics.json', 'w') as f:
        json.dump(analytics, f, indent=2)
    
    # Add metadata
    context.add_output_metadata({
        "total_products": MetadataValue.int(analytics['summary']['total_products']),
        "total_categories": MetadataValue.int(analytics['summary']['total_categories']),
        "total_brands": MetadataValue.int(analytics['summary']['total_brands']),
        "total_inventory_value": MetadataValue.float(analytics['summary']['total_inventory_value']),
        "file_path": MetadataValue.text('data/analytics/product_analytics.json')
    })
    
    context.log.info("Product analytics generated successfully")
    return analytics 