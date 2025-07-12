#!/usr/bin/env python3
"""
Basic Data Pipeline Workflow
Demonstrates a simple ETL pipeline using Prefect 3
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import logging
from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash
from prefect.filesystems import LocalFileSystem
from prefect.blocks.system import Secret

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@task(name="extract_data", retries=3, retry_delay_seconds=30)
def extract_data() -> pd.DataFrame:
    """Extract sample data from various sources"""
    logger = get_run_logger()
    logger.info("Starting data extraction...")
    
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
    logger.info(f"Extracted {len(df)} records")
    
    # Save raw data
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/sales_raw.csv', index=False)
    logger.info("Raw data saved to data/raw/sales_raw.csv")
    
    return df

@task(name="transform_data", retries=2)
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform and clean the data"""
    logger = get_run_logger()
    logger.info("Starting data transformation...")
    
    # Convert date column
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    
    # Add derived columns
    df['month'] = df['sale_date'].dt.month
    df['year'] = df['sale_date'].dt.year
    df['day_of_week'] = df['sale_date'].dt.dayofweek
    
    # Calculate additional metrics
    df['profit_margin'] = df['total_amount'] * 0.3  # Assume 30% margin
    df['revenue_per_unit'] = df['total_amount'] / df['quantity']
    
    # Clean data
    df = df.dropna()
    df = df[df['total_amount'] > 0]
    
    logger.info(f"Transformed {len(df)} records")
    logger.info(f"Columns: {list(df.columns)}")
    
    return df

@task(name="load_data")
def load_data(df: pd.DataFrame) -> str:
    """Load transformed data to destination"""
    logger = get_run_logger()
    logger.info("Starting data loading...")
    
    # Create processed data directory
    os.makedirs('data/processed', exist_ok=True)
    
    # Save processed data
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'data/processed/sales_processed_{timestamp}.csv'
    df.to_csv(output_file, index=False)
    
    # Create summary statistics
    summary = {
        'total_records': len(df),
        'total_revenue': df['total_amount'].sum(),
        'avg_order_value': df['total_amount'].mean(),
        'unique_customers': df['customer_id'].nunique(),
        'unique_products': df['product_id'].nunique(),
        'date_range': f"{df['sale_date'].min()} to {df['sale_date'].max()}"
    }
    
    # Save summary
    summary_file = f'data/processed/summary_{timestamp}.json'
    import json
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info(f"Data loaded to {output_file}")
    logger.info(f"Summary saved to {summary_file}")
    logger.info(f"Summary: {summary}")
    
    return output_file

@task(name="validate_data")
def validate_data(df: pd.DataFrame) -> bool:
    """Validate the transformed data"""
    logger = get_run_logger()
    logger.info("Starting data validation...")
    
    # Check for required columns
    required_columns = ['sale_id', 'sale_date', 'product_id', 'customer_id', 'total_amount']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        logger.error(f"Missing required columns: {missing_columns}")
        return False
    
    # Check for data quality
    validation_results = {
        'has_duplicates': df.duplicated().any(),
        'has_nulls': df.isnull().any().any(),
        'negative_amounts': (df['total_amount'] < 0).any(),
        'zero_quantities': (df['quantity'] <= 0).any(),
        'valid_date_range': df['sale_date'].min() <= df['sale_date'].max()
    }
    
    # Log validation results
    for check, result in validation_results.items():
        if result:
            logger.warning(f"Validation failed: {check}")
        else:
            logger.info(f"Validation passed: {check}")
    
    # Overall validation
    is_valid = not any(validation_results.values())
    logger.info(f"Data validation {'passed' if is_valid else 'failed'}")
    
    return is_valid

@flow(name="data-pipeline", description="Basic ETL data pipeline")
def data_pipeline():
    """Main data pipeline flow"""
    logger = get_run_logger()
    logger.info("Starting data pipeline workflow...")
    
    try:
        # Extract data
        raw_data = extract_data()
        
        # Transform data
        transformed_data = transform_data(raw_data)
        
        # Validate data
        is_valid = validate_data(transformed_data)
        
        if is_valid:
            # Load data
            output_file = load_data(transformed_data)
            logger.info(f"Data pipeline completed successfully. Output: {output_file}")
            return output_file
        else:
            logger.error("Data validation failed. Pipeline aborted.")
            return None
            
    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}")
        raise

if __name__ == "__main__":
    # Run the pipeline
    result = data_pipeline()
    print(f"Pipeline result: {result}") 