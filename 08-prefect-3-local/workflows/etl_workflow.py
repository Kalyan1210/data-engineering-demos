#!/usr/bin/env python3
"""
Complex ETL Workflow
Demonstrates advanced ETL pipeline with multiple data sources and transformations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import logging
import json
from prefect import flow, task, get_run_logger
from prefect.artifacts import create_markdown_artifact
from prefect.filesystems import LocalFileSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@task(name="extract_customer_data")
def extract_customer_data() -> pd.DataFrame:
    """Extract customer data from source"""
    logger = get_run_logger()
    logger.info("Extracting customer data...")
    
    # Generate customer data
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
    logger.info(f"Extracted {len(df)} customer records")
    return df

@task(name="extract_product_data")
def extract_product_data() -> pd.DataFrame:
    """Extract product data from source"""
    logger = get_run_logger()
    logger.info("Extracting product data...")
    
    # Generate product data
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
    logger.info(f"Extracted {len(df)} product records")
    return df

@task(name="extract_sales_data")
def extract_sales_data() -> pd.DataFrame:
    """Extract sales data from source"""
    logger = get_run_logger()
    logger.info("Extracting sales data...")
    
    # Generate sales data
    np.random.seed(42)
    n_records = 2000
    
    # Date range for the last 6 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    sales_data = []
    for i in range(n_records):
        sale_date = np.random.choice(date_range)
        product_id = np.random.randint(1, 51)
        customer_id = np.random.randint(1, 201)
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
            'total_amount': round(total_amount, 2),
            'payment_method': np.random.choice(['Credit Card', 'Debit Card', 'Cash', 'PayPal']),
            'shipping_method': np.random.choice(['Standard', 'Express', 'Overnight'])
        })
    
    df = pd.DataFrame(sales_data)
    logger.info(f"Extracted {len(df)} sales records")
    return df

@task(name="transform_customer_data")
def transform_customer_data(customers_df: pd.DataFrame) -> pd.DataFrame:
    """Transform customer data"""
    logger = get_run_logger()
    logger.info("Transforming customer data...")
    
    # Convert date
    customers_df['registration_date'] = pd.to_datetime(customers_df['registration_date'])
    
    # Add derived columns
    customers_df['full_name'] = customers_df['first_name'] + ' ' + customers_df['last_name']
    customers_df['age_group'] = pd.cut(customers_df['age'], 
                                      bins=[0, 25, 35, 50, 65, 100], 
                                      labels=['18-25', '26-35', '36-50', '51-65', '65+'])
    customers_df['customer_lifetime_days'] = (datetime.now() - customers_df['registration_date']).dt.days
    
    # Clean data
    customers_df = customers_df.dropna()
    
    logger.info(f"Transformed {len(customers_df)} customer records")
    return customers_df

@task(name="transform_product_data")
def transform_product_data(products_df: pd.DataFrame) -> pd.DataFrame:
    """Transform product data"""
    logger = get_run_logger()
    logger.info("Transforming product data...")
    
    # Convert date
    products_df['created_date'] = pd.to_datetime(products_df['created_date'])
    
    # Add derived columns
    products_df['profit_margin'] = products_df['price'] - products_df['cost']
    products_df['profit_margin_pct'] = (products_df['profit_margin'] / products_df['price']) * 100
    products_df['inventory_status'] = np.where(products_df['inventory'] > 10, 'In Stock', 
                                             np.where(products_df['inventory'] > 0, 'Low Stock', 'Out of Stock'))
    
    # Clean data
    products_df = products_df.dropna()
    
    logger.info(f"Transformed {len(products_df)} product records")
    return products_df

@task(name="transform_sales_data")
def transform_sales_data(sales_df: pd.DataFrame) -> pd.DataFrame:
    """Transform sales data"""
    logger = get_run_logger()
    logger.info("Transforming sales data...")
    
    # Convert date
    sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])
    
    # Add derived columns
    sales_df['month'] = sales_df['sale_date'].dt.month
    sales_df['year'] = sales_df['sale_date'].dt.year
    sales_df['day_of_week'] = sales_df['sale_date'].dt.dayofweek
    sales_df['quarter'] = sales_df['sale_date'].dt.quarter
    sales_df['profit'] = sales_df['total_amount'] * 0.3  # Assume 30% profit margin
    
    # Clean data
    sales_df = sales_df.dropna()
    sales_df = sales_df[sales_df['total_amount'] > 0]
    
    logger.info(f"Transformed {len(sales_df)} sales records")
    return sales_df

@task(name="create_analytics_views")
def create_analytics_views(customers_df: pd.DataFrame, 
                          products_df: pd.DataFrame, 
                          sales_df: pd.DataFrame) -> dict:
    """Create analytics views and aggregations"""
    logger = get_run_logger()
    logger.info("Creating analytics views...")
    
    # Customer analytics
    customer_analytics = customers_df.groupby('customer_segment').agg({
        'customer_id': 'count',
        'age': 'mean',
        'customer_lifetime_days': 'mean'
    }).rename(columns={'customer_id': 'customer_count'})
    
    # Product analytics
    product_analytics = products_df.groupby('category').agg({
        'product_id': 'count',
        'price': 'mean',
        'inventory': 'sum',
        'profit_margin': 'sum'
    }).rename(columns={'product_id': 'product_count'})
    
    # Sales analytics
    sales_analytics = sales_df.groupby(['year', 'month']).agg({
        'sale_id': 'count',
        'total_amount': 'sum',
        'profit': 'sum'
    }).rename(columns={'sale_id': 'transaction_count'})
    
    # Top customers
    top_customers = sales_df.groupby('customer_id').agg({
        'total_amount': 'sum',
        'sale_id': 'count'
    }).rename(columns={'sale_id': 'transaction_count'}).sort_values('total_amount', ascending=False).head(10)
    
    # Top products
    top_products = sales_df.groupby('product_id').agg({
        'total_amount': 'sum',
        'quantity': 'sum'
    }).rename(columns={'quantity': 'units_sold'}).sort_values('total_amount', ascending=False).head(10)
    
    analytics = {
        'customer_analytics': customer_analytics,
        'product_analytics': product_analytics,
        'sales_analytics': sales_analytics,
        'top_customers': top_customers,
        'top_products': top_products
    }
    
    logger.info("Analytics views created successfully")
    return analytics

@task(name="load_to_destination")
def load_to_destination(customers_df: pd.DataFrame, 
                       products_df: pd.DataFrame, 
                       sales_df: pd.DataFrame, 
                       analytics: dict) -> str:
    """Load all data to destination"""
    logger = get_run_logger()
    logger.info("Loading data to destination...")
    
    # Create output directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = f'data/processed/etl_run_{timestamp}'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save main data
    customers_df.to_csv(f'{output_dir}/customers.csv', index=False)
    products_df.to_csv(f'{output_dir}/products.csv', index=False)
    sales_df.to_csv(f'{output_dir}/sales.csv', index=False)
    
    # Save analytics
    for name, df in analytics.items():
        df.to_csv(f'{output_dir}/{name}.csv')
    
    # Create summary report
    summary = {
        'run_timestamp': timestamp,
        'customers_count': len(customers_df),
        'products_count': len(products_df),
        'sales_count': len(sales_df),
        'total_revenue': sales_df['total_amount'].sum(),
        'total_profit': sales_df['profit'].sum(),
        'unique_customers': sales_df['customer_id'].nunique(),
        'unique_products': sales_df['product_id'].nunique(),
        'date_range': f"{sales_df['sale_date'].min()} to {sales_df['sale_date'].max()}"
    }
    
    with open(f'{output_dir}/summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Create markdown artifact
    markdown_content = f"""
    # ETL Pipeline Summary
    
    ## Run Details
    - **Timestamp**: {timestamp}
    - **Total Records Processed**: {len(customers_df) + len(products_df) + len(sales_df)}
    
    ## Data Summary
    - **Customers**: {len(customers_df)} records
    - **Products**: {len(products_df)} records  
    - **Sales**: {len(sales_df)} records
    
    ## Financial Summary
    - **Total Revenue**: ${summary['total_revenue']:,.2f}
    - **Total Profit**: ${summary['total_profit']:,.2f}
    - **Average Order Value**: ${summary['total_revenue'] / summary['sales_count']:,.2f}
    
    ## Analytics Created
    - Customer Analytics
    - Product Analytics  
    - Sales Analytics
    - Top Customers
    - Top Products
    """
    
    create_markdown_artifact(
        key=f"etl-summary-{timestamp}",
        markdown=markdown_content,
        description="ETL Pipeline Summary Report"
    )
    
    logger.info(f"Data loaded to {output_dir}")
    logger.info(f"Summary: {summary}")
    
    return output_dir

@flow(name="etl-workflow", description="Complex ETL workflow with multiple data sources")
def etl_workflow():
    """Main ETL workflow"""
    logger = get_run_logger()
    logger.info("Starting ETL workflow...")
    
    try:
        # Extract data from multiple sources
        customers_raw = extract_customer_data()
        products_raw = extract_product_data()
        sales_raw = extract_sales_data()
        
        # Transform data
        customers_transformed = transform_customer_data(customers_raw)
        products_transformed = transform_product_data(products_raw)
        sales_transformed = transform_sales_data(sales_raw)
        
        # Create analytics views
        analytics = create_analytics_views(customers_transformed, products_transformed, sales_transformed)
        
        # Load to destination
        output_dir = load_to_destination(customers_transformed, products_transformed, sales_transformed, analytics)
        
        logger.info(f"ETL workflow completed successfully. Output: {output_dir}")
        return output_dir
        
    except Exception as e:
        logger.error(f"ETL workflow failed with error: {e}")
        raise

if __name__ == "__main__":
    # Run the ETL workflow
    result = etl_workflow()
    print(f"ETL workflow result: {result}") 