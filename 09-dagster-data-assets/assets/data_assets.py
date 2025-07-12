#!/usr/bin/env python3
"""
Basic Data Assets
Demonstrates data asset management using Dagster
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
    description="Raw sales data from external source",
    group_name="data_ingestion"
)
def raw_sales_data(context: AssetExecutionContext) -> pd.DataFrame:
    """Extract raw sales data from source"""
    context.log.info("Extracting raw sales data...")
    
    # Generate sample sales data
    np.random.seed(42)
    n_records = 1000
    
    # Date range for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate sales data
    sales_data = []
    for i in range(n_records):
        sale_date = np.random.choice(date_range)
        product_id = np.random.randint(1, 21)
        customer_id = np.random.randint(1, 101)
        region_id = np.random.randint(1, 6)
        
        base_price = np.random.uniform(10, 500)
        quantity = np.random.randint(1, 10)
        total_amount = base_price * quantity
        
        sales_data.append({
            'sale_id': i + 1,
            'sale_date': sale_date.strftime('%Y-%m-%d'),
            'product_id': product_id,
            'customer_id': customer_id,
            'region_id': region_id,
            'quantity': quantity,
            'unit_price': round(base_price, 2),
            'total_amount': round(total_amount, 2)
        })
    
    df = pd.DataFrame(sales_data)
    
    # Save raw data
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/sales_raw.csv', index=False)
    
    # Add metadata
    context.add_output_metadata({
        "num_records": MetadataValue.int(len(df)),
        "date_range": MetadataValue.text(f"{df['sale_date'].min()} to {df['sale_date'].max()}"),
        "total_revenue": MetadataValue.float(df['total_amount'].sum()),
        "file_path": MetadataValue.text('data/raw/sales_raw.csv')
    })
    
    context.log.info(f"Extracted {len(df)} sales records")
    return df

@asset(
    description="Raw customer data from external source",
    group_name="data_ingestion"
)
def raw_customer_data(context: AssetExecutionContext) -> pd.DataFrame:
    """Extract raw customer data from source"""
    context.log.info("Extracting raw customer data...")
    
    # Generate sample customer data
    np.random.seed(42)
    n_customers = 200
    
    customers = []
    for i in range(n_customers):
        customers.append({
            'customer_id': i + 1,
            'first_name': f'Customer{i+1}',
            'last_name': f'LastName{i+1}',
            'email': f'customer{i+1}@example.com',
            'age': np.random.randint(18, 80),
            'gender': np.random.choice(['M', 'F']),
            'income_level': np.random.choice(['Low', 'Medium', 'High']),
            'customer_segment': np.random.choice(['Bronze', 'Silver', 'Gold', 'Platinum']),
            'registration_date': (datetime.now() - timedelta(days=np.random.randint(1, 1000))).strftime('%Y-%m-%d')
        })
    
    df = pd.DataFrame(customers)
    
    # Save raw data
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/customers_raw.csv', index=False)
    
    # Add metadata
    context.add_output_metadata({
        "num_records": MetadataValue.int(len(df)),
        "unique_segments": MetadataValue.int(df['customer_segment'].nunique()),
        "avg_age": MetadataValue.float(df['age'].mean()),
        "file_path": MetadataValue.text('data/raw/customers_raw.csv')
    })
    
    context.log.info(f"Extracted {len(df)} customer records")
    return df

@asset(
    description="Raw product data from external source",
    group_name="data_ingestion"
)
def raw_product_data(context: AssetExecutionContext) -> pd.DataFrame:
    """Extract raw product data from source"""
    context.log.info("Extracting raw product data...")
    
    # Generate sample product data
    np.random.seed(42)
    n_products = 50
    
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Food', 'Beauty']
    brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE', 'BrandF']
    
    products = []
    for i in range(n_products):
        products.append({
            'product_id': i + 1,
            'product_name': f'Product {i+1}',
            'category': np.random.choice(categories),
            'brand': np.random.choice(brands),
            'price': round(np.random.uniform(10, 500), 2),
            'cost': round(np.random.uniform(5, 250), 2),
            'inventory': np.random.randint(0, 100),
            'supplier_id': np.random.randint(1, 11),
            'created_date': (datetime.now() - timedelta(days=np.random.randint(1, 365))).strftime('%Y-%m-%d')
        })
    
    df = pd.DataFrame(products)
    
    # Save raw data
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/products_raw.csv', index=False)
    
    # Add metadata
    context.add_output_metadata({
        "num_records": MetadataValue.int(len(df)),
        "unique_categories": MetadataValue.int(df['category'].nunique()),
        "avg_price": MetadataValue.float(df['price'].mean()),
        "file_path": MetadataValue.text('data/raw/products_raw.csv')
    })
    
    context.log.info(f"Extracted {len(df)} product records")
    return df

@asset(
    description="Validated sales data with quality checks",
    group_name="data_validation",
    deps=[raw_sales_data]
)
def validated_sales_data(context: AssetExecutionContext, raw_sales_data: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean sales data"""
    context.log.info("Validating sales data...")
    
    # Data validation checks
    validation_results = {
        'total_records': len(raw_sales_data),
        'missing_values': raw_sales_data.isnull().sum().sum(),
        'duplicate_records': raw_sales_data.duplicated().sum(),
        'negative_amounts': (raw_sales_data['total_amount'] < 0).sum(),
        'zero_quantities': (raw_sales_data['quantity'] <= 0).sum(),
        'invalid_dates': 0  # Will be calculated
    }
    
    # Check for invalid dates
    try:
        pd.to_datetime(raw_sales_data['sale_date'])
    except:
        validation_results['invalid_dates'] = len(raw_sales_data)
    
    # Clean data
    df = raw_sales_data.copy()
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Remove invalid records
    df = df[df['total_amount'] > 0]
    df = df[df['quantity'] > 0]
    
    # Convert date
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    
    # Save validated data
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/sales_validated.csv', index=False)
    
    # Add metadata
    context.add_output_metadata({
        "original_records": MetadataValue.int(validation_results['total_records']),
        "validated_records": MetadataValue.int(len(df)),
        "removed_records": MetadataValue.int(validation_results['total_records'] - len(df)),
        "validation_issues": MetadataValue.json(validation_results),
        "file_path": MetadataValue.text('data/processed/sales_validated.csv')
    })
    
    context.log.info(f"Validated {len(df)} sales records")
    return df

@asset(
    description="Validated customer data with quality checks",
    group_name="data_validation",
    deps=[raw_customer_data]
)
def validated_customer_data(context: AssetExecutionContext, raw_customer_data: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean customer data"""
    context.log.info("Validating customer data...")
    
    # Data validation checks
    validation_results = {
        'total_records': len(raw_customer_data),
        'missing_values': raw_customer_data.isnull().sum().sum(),
        'duplicate_records': raw_customer_data.duplicated().sum(),
        'invalid_emails': 0,  # Will be calculated
        'invalid_ages': len(raw_customer_data[raw_customer_data['age'] < 0])
    }
    
    # Clean data
    df = raw_customer_data.copy()
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Remove invalid ages
    df = df[df['age'] >= 0]
    
    # Convert date
    df['registration_date'] = pd.to_datetime(df['registration_date'])
    
    # Save validated data
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/customers_validated.csv', index=False)
    
    # Add metadata
    context.add_output_metadata({
        "original_records": MetadataValue.int(validation_results['total_records']),
        "validated_records": MetadataValue.int(len(df)),
        "removed_records": MetadataValue.int(validation_results['total_records'] - len(df)),
        "validation_issues": MetadataValue.json(validation_results),
        "file_path": MetadataValue.text('data/processed/customers_validated.csv')
    })
    
    context.log.info(f"Validated {len(df)} customer records")
    return df

@asset(
    description="Validated product data with quality checks",
    group_name="data_validation",
    deps=[raw_product_data]
)
def validated_product_data(context: AssetExecutionContext, raw_product_data: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean product data"""
    context.log.info("Validating product data...")
    
    # Data validation checks
    validation_results = {
        'total_records': len(raw_product_data),
        'missing_values': raw_product_data.isnull().sum().sum(),
        'duplicate_records': raw_product_data.duplicated().sum(),
        'negative_prices': (raw_product_data['price'] < 0).sum(),
        'negative_costs': (raw_product_data['cost'] < 0).sum(),
        'negative_inventory': (raw_product_data['inventory'] < 0).sum()
    }
    
    # Clean data
    df = raw_product_data.copy()
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Remove invalid records
    df = df[df['price'] > 0]
    df = df[df['cost'] > 0]
    df = df[df['inventory'] >= 0]
    
    # Convert date
    df['created_date'] = pd.to_datetime(df['created_date'])
    
    # Save validated data
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/products_validated.csv', index=False)
    
    # Add metadata
    context.add_output_metadata({
        "original_records": MetadataValue.int(validation_results['total_records']),
        "validated_records": MetadataValue.int(len(df)),
        "removed_records": MetadataValue.int(validation_results['total_records'] - len(df)),
        "validation_issues": MetadataValue.json(validation_results),
        "file_path": MetadataValue.text('data/processed/products_validated.csv')
    })
    
    context.log.info(f"Validated {len(df)} product records")
    return df

@asset(
    description="Data quality report for all validated assets",
    group_name="data_quality",
    deps=[validated_sales_data, validated_customer_data, validated_product_data]
)
def data_quality_report(
    context: AssetExecutionContext,
    validated_sales_data: pd.DataFrame,
    validated_customer_data: pd.DataFrame,
    validated_product_data: pd.DataFrame
) -> Dict[str, Any]:
    """Generate comprehensive data quality report"""
    context.log.info("Generating data quality report...")
    
    # Calculate quality metrics
    quality_report = {
        'timestamp': datetime.now().isoformat(),
        'sales_data': {
            'total_records': len(validated_sales_data),
            'unique_customers': validated_sales_data['customer_id'].nunique(),
            'unique_products': validated_sales_data['product_id'].nunique(),
            'total_revenue': validated_sales_data['total_amount'].sum(),
            'avg_order_value': validated_sales_data['total_amount'].mean(),
            'date_range': f"{validated_sales_data['sale_date'].min()} to {validated_sales_data['sale_date'].max()}"
        },
        'customer_data': {
            'total_records': len(validated_customer_data),
            'unique_segments': validated_customer_data['customer_segment'].nunique(),
            'avg_age': validated_customer_data['age'].mean(),
            'segment_distribution': validated_customer_data['customer_segment'].value_counts().to_dict()
        },
        'product_data': {
            'total_records': len(validated_product_data),
            'unique_categories': validated_product_data['category'].nunique(),
            'avg_price': validated_product_data['price'].mean(),
            'category_distribution': validated_product_data['category'].value_counts().to_dict()
        }
    }
    
    # Save quality report
    os.makedirs('data/analytics', exist_ok=True)
    import json
    with open('data/analytics/data_quality_report.json', 'w') as f:
        json.dump(quality_report, f, indent=2)
    
    # Add metadata
    context.add_output_metadata({
        "total_assets": MetadataValue.int(3),
        "total_records": MetadataValue.int(
            len(validated_sales_data) + len(validated_customer_data) + len(validated_product_data)
        ),
        "total_revenue": MetadataValue.float(quality_report['sales_data']['total_revenue']),
        "file_path": MetadataValue.text('data/analytics/data_quality_report.json')
    })
    
    context.log.info("Data quality report generated successfully")
    return quality_report 