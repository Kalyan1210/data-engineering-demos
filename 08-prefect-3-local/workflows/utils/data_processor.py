#!/usr/bin/env python3
"""
Data Processing Utilities
Common data processing functions for Prefect workflows
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Any, Optional
from prefect import get_run_logger

def validate_dataframe(df: pd.DataFrame, required_columns: List[str] = None) -> bool:
    """Validate dataframe structure and content"""
    logger = get_run_logger()
    
    if df.empty:
        logger.error("DataFrame is empty")
        return False
    
    if required_columns:
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            logger.error(f"Missing required columns: {missing_columns}")
            return False
    
    # Check for all null rows
    if df.isnull().all(axis=1).any():
        logger.warning("Found rows with all null values")
    
    # Check for duplicate rows
    if df.duplicated().any():
        logger.warning("Found duplicate rows")
    
    return True

def clean_dataframe(df: pd.DataFrame, 
                   drop_duplicates: bool = True,
                   fill_nulls: bool = True,
                   remove_outliers: bool = False) -> pd.DataFrame:
    """Clean and prepare dataframe"""
    logger = get_run_logger()
    original_count = len(df)
    
    # Remove duplicates
    if drop_duplicates:
        df = df.drop_duplicates()
        logger.info(f"Removed {original_count - len(df)} duplicate rows")
    
    # Fill nulls
    if fill_nulls:
        # Fill numeric columns with 0
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].fillna(0)
        
        # Fill string columns with 'Unknown'
        string_columns = df.select_dtypes(include=['object']).columns
        df[string_columns] = df[string_columns].fillna('Unknown')
        
        logger.info("Filled null values")
    
    # Remove outliers (optional)
    if remove_outliers:
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        
        logger.info(f"Removed outliers, remaining rows: {len(df)}")
    
    return df

def add_timestamp_columns(df: pd.DataFrame, 
                         date_column: str = None,
                         add_processing_time: bool = True) -> pd.DataFrame:
    """Add timestamp and derived date columns"""
    logger = get_run_logger()
    
    # Add processing timestamp
    if add_processing_time:
        df['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Add date columns if date column exists
    if date_column and date_column in df.columns:
        try:
            df[date_column] = pd.to_datetime(df[date_column])
            df['year'] = df[date_column].dt.year
            df['month'] = df[date_column].dt.month
            df['day'] = df[date_column].dt.day
            df['day_of_week'] = df[date_column].dt.dayofweek
            df['quarter'] = df[date_column].dt.quarter
            df['is_weekend'] = df[date_column].dt.dayofweek >= 5
            
            logger.info(f"Added date columns from {date_column}")
        except Exception as e:
            logger.warning(f"Could not parse date column {date_column}: {e}")
    
    return df

def calculate_summary_statistics(df: pd.DataFrame, 
                               group_columns: List[str] = None,
                               value_columns: List[str] = None) -> Dict[str, Any]:
    """Calculate summary statistics for dataframe"""
    logger = get_run_logger()
    
    if value_columns is None:
        value_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    summary = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'data_types': df.dtypes.to_dict()
    }
    
    # Calculate statistics for numeric columns
    if value_columns:
        numeric_df = df[value_columns]
        summary['numeric_summary'] = {
            'mean': numeric_df.mean().to_dict(),
            'median': numeric_df.median().to_dict(),
            'std': numeric_df.std().to_dict(),
            'min': numeric_df.min().to_dict(),
            'max': numeric_df.max().to_dict()
        }
    
    # Group statistics
    if group_columns:
        for group_col in group_columns:
            if group_col in df.columns:
                group_stats = df.groupby(group_col).agg({
                    col: ['count', 'mean', 'sum'] 
                    for col in value_columns if col in df.columns
                }).round(2)
                summary[f'{group_col}_summary'] = group_stats.to_dict()
    
    logger.info(f"Calculated summary statistics for {len(df)} rows")
    return summary

def detect_data_quality_issues(df: pd.DataFrame) -> Dict[str, Any]:
    """Detect potential data quality issues"""
    logger = get_run_logger()
    
    issues = {
        'missing_values': df.isnull().sum().to_dict(),
        'duplicate_rows': df.duplicated().sum(),
        'empty_strings': (df == '').sum().to_dict(),
        'zero_values': (df == 0).sum().to_dict(),
        'negative_values': (df < 0).sum().to_dict(),
        'outliers': {}
    }
    
    # Detect outliers for numeric columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
        issues['outliers'][col] = outliers
    
    # Calculate quality score
    total_cells = len(df) * len(df.columns)
    problematic_cells = sum(issues['missing_values'].values()) + issues['duplicate_rows']
    quality_score = (total_cells - problematic_cells) / total_cells * 100
    
    issues['quality_score'] = quality_score
    
    logger.info(f"Data quality score: {quality_score:.2f}%")
    return issues

def generate_data_profile(df: pd.DataFrame, 
                         output_file: str = None) -> str:
    """Generate comprehensive data profile"""
    logger = get_run_logger()
    
    profile = {
        'basic_info': {
            'shape': df.shape,
            'memory_usage': df.memory_usage(deep=True).sum(),
            'data_types': df.dtypes.to_dict()
        },
        'summary_statistics': calculate_summary_statistics(df),
        'quality_issues': detect_data_quality_issues(df),
        'column_info': {}
    }
    
    # Detailed column information
    for col in df.columns:
        profile['column_info'][col] = {
            'data_type': str(df[col].dtype),
            'unique_values': df[col].nunique(),
            'missing_values': df[col].isnull().sum(),
            'most_common': df[col].value_counts().head(5).to_dict() if df[col].dtype == 'object' else None
        }
    
    # Convert to JSON string
    import json
    profile_json = json.dumps(profile, indent=2, default=str)
    
    # Save to file if specified
    if output_file:
        with open(output_file, 'w') as f:
            f.write(profile_json)
        logger.info(f"Data profile saved to {output_file}")
    
    return profile_json

def sample_data(df: pd.DataFrame, 
                sample_size: int = 1000,
                random_state: int = 42) -> pd.DataFrame:
    """Sample data for testing or analysis"""
    logger = get_run_logger()
    
    if len(df) <= sample_size:
        logger.info("Dataframe smaller than sample size, returning full dataset")
        return df
    
    sampled_df = df.sample(n=sample_size, random_state=random_state)
    logger.info(f"Sampled {len(sampled_df)} rows from {len(df)} total rows")
    
    return sampled_df

def split_dataframe(df: pd.DataFrame, 
                   split_ratio: float = 0.8,
                   random_state: int = 42) -> tuple:
    """Split dataframe into training and testing sets"""
    logger = get_run_logger()
    
    split_index = int(len(df) * split_ratio)
    train_df = df.iloc[:split_index]
    test_df = df.iloc[split_index:]
    
    logger.info(f"Split dataframe: {len(train_df)} training, {len(test_df)} testing")
    
    return train_df, test_df 