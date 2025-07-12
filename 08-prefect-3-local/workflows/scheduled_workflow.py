#!/usr/bin/env python3
"""
Scheduled Workflow
Demonstrates automated workflow execution with scheduling and monitoring
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import logging
import json
import time
from prefect import flow, task, get_run_logger
from prefect.schedules import CronSchedule
from prefect.artifacts import create_markdown_artifact
from prefect.notifications import send_email_notification

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@task(name="health_check", retries=2)
def health_check() -> bool:
    """Check system health before running workflow"""
    logger = get_run_logger()
    logger.info("Performing health check...")
    
    # Simulate health checks
    checks = {
        'disk_space': True,  # Simulate disk space check
        'database_connection': True,  # Simulate DB connection
        'api_availability': True,  # Simulate API check
        'memory_usage': True  # Simulate memory check
    }
    
    all_healthy = all(checks.values())
    
    for check_name, status in checks.items():
        if status:
            logger.info(f"✓ {check_name}: OK")
        else:
            logger.error(f"✗ {check_name}: FAILED")
    
    logger.info(f"Health check {'passed' if all_healthy else 'failed'}")
    return all_healthy

@task(name="extract_daily_data")
def extract_daily_data() -> pd.DataFrame:
    """Extract daily data for processing"""
    logger = get_run_logger()
    logger.info("Extracting daily data...")
    
    # Simulate daily data extraction
    np.random.seed(int(datetime.now().strftime('%Y%m%d')))  # Seed based on date
    
    # Generate today's data
    n_records = np.random.randint(50, 200)
    today = datetime.now().strftime('%Y-%m-%d')
    
    data = []
    for i in range(n_records):
        data.append({
            'record_id': i + 1,
            'date': today,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'value': np.random.uniform(10, 1000),
            'category': np.random.choice(['A', 'B', 'C', 'D']),
            'status': np.random.choice(['active', 'inactive', 'pending']),
            'priority': np.random.choice(['low', 'medium', 'high'])
        })
    
    df = pd.DataFrame(data)
    logger.info(f"Extracted {len(df)} daily records for {today}")
    
    # Save raw data
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv(f'data/raw/daily_data_{today}.csv', index=False)
    
    return df

@task(name="process_daily_data")
def process_daily_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process and transform daily data"""
    logger = get_run_logger()
    logger.info("Processing daily data...")
    
    # Add processing timestamp
    df['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Add derived metrics
    df['value_category'] = pd.cut(df['value'], 
                                 bins=[0, 100, 500, 1000, float('inf')],
                                 labels=['Low', 'Medium', 'High', 'Very High'])
    
    df['processing_time'] = np.random.uniform(0.1, 2.0, len(df))
    
    # Calculate summary metrics
    df['is_high_priority'] = df['priority'] == 'high'
    df['is_active'] = df['status'] == 'active'
    
    logger.info(f"Processed {len(df)} records")
    logger.info(f"Categories: {df['category'].value_counts().to_dict()}")
    logger.info(f"Priorities: {df['priority'].value_counts().to_dict()}")
    
    return df

@task(name="generate_daily_report")
def generate_daily_report(df: pd.DataFrame) -> dict:
    """Generate daily summary report"""
    logger = get_run_logger()
    logger.info("Generating daily report...")
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Calculate metrics
    total_records = len(df)
    total_value = df['value'].sum()
    avg_value = df['value'].mean()
    
    category_summary = df.groupby('category').agg({
        'value': ['sum', 'mean', 'count']
    }).round(2)
    
    priority_summary = df.groupby('priority').agg({
        'value': ['sum', 'count']
    }).round(2)
    
    status_summary = df.groupby('status').agg({
        'value': ['sum', 'count']
    }).round(2)
    
    # Create report
    report = {
        'date': today,
        'total_records': total_records,
        'total_value': total_value,
        'avg_value': avg_value,
        'category_summary': category_summary.to_dict(),
        'priority_summary': priority_summary.to_dict(),
        'status_summary': status_summary.to_dict(),
        'processing_time': df['processing_time'].sum(),
        'high_priority_count': df['is_high_priority'].sum(),
        'active_records': df['is_active'].sum()
    }
    
    logger.info(f"Generated report for {today}")
    logger.info(f"Total value: {total_value:,.2f}")
    logger.info(f"Average value: {avg_value:,.2f}")
    
    return report

@task(name="save_processed_data")
def save_processed_data(df: pd.DataFrame, report: dict) -> str:
    """Save processed data and report"""
    logger = get_run_logger()
    logger.info("Saving processed data...")
    
    today = datetime.now().strftime('%Y%m%d')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create output directory
    output_dir = f'data/processed/daily_run_{timestamp}'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save processed data
    df.to_csv(f'{output_dir}/processed_data.csv', index=False)
    
    # Save report
    with open(f'{output_dir}/daily_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Create markdown summary
    markdown_content = f"""
    # Daily Processing Report
    
    ## Date: {report['date']}
    
    ## Summary
    - **Total Records**: {report['total_records']:,}
    - **Total Value**: ${report['total_value']:,.2f}
    - **Average Value**: ${report['avg_value']:,.2f}
    - **Processing Time**: {report['processing_time']:.2f} seconds
    
    ## Breakdown
    - **High Priority Records**: {report['high_priority_count']}
    - **Active Records**: {report['active_records']}
    
    ## Category Summary
    {pd.DataFrame(report['category_summary']).to_markdown()}
    
    ## Priority Summary  
    {pd.DataFrame(report['priority_summary']).to_markdown()}
    
    ## Status Summary
    {pd.DataFrame(report['status_summary']).to_markdown()}
    """
    
    with open(f'{output_dir}/report.md', 'w') as f:
        f.write(markdown_content)
    
    # Create Prefect artifact
    create_markdown_artifact(
        key=f"daily-report-{today}",
        markdown=markdown_content,
        description=f"Daily Processing Report for {report['date']}"
    )
    
    logger.info(f"Data saved to {output_dir}")
    return output_dir

@task(name="send_notifications")
def send_notifications(report: dict, output_dir: str) -> bool:
    """Send notifications about workflow completion"""
    logger = get_run_logger()
    logger.info("Sending notifications...")
    
    # Simulate notification sending
    notification_data = {
        'recipients': ['admin@example.com', 'data-team@example.com'],
        'subject': f"Daily Processing Complete - {report['date']}",
        'message': f"""
        Daily processing workflow completed successfully.
        
        Summary:
        - Records processed: {report['total_records']:,}
        - Total value: ${report['total_value']:,.2f}
        - Processing time: {report['processing_time']:.2f} seconds
        
        Output location: {output_dir}
        """,
        'timestamp': datetime.now().isoformat()
    }
    
    # Simulate sending notifications
    time.sleep(1)  # Simulate network delay
    
    logger.info(f"Notifications sent to {len(notification_data['recipients'])} recipients")
    return True

@task(name="cleanup_old_data")
def cleanup_old_data() -> int:
    """Clean up old data files"""
    logger = get_run_logger()
    logger.info("Cleaning up old data...")
    
    # Simulate cleanup of files older than 30 days
    cutoff_date = datetime.now() - timedelta(days=30)
    files_removed = 0
    
    # Check raw data directory
    raw_dir = 'data/raw'
    if os.path.exists(raw_dir):
        for file in os.listdir(raw_dir):
            file_path = os.path.join(raw_dir, file)
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_time < cutoff_date:
                    os.remove(file_path)
                    files_removed += 1
                    logger.info(f"Removed old file: {file}")
    
    logger.info(f"Cleanup completed. Removed {files_removed} old files")
    return files_removed

@flow(name="scheduled-daily-workflow", 
      description="Scheduled daily data processing workflow",
      schedule=CronSchedule(cron="0 6 * * *"))  # Run daily at 6 AM
def scheduled_daily_workflow():
    """Main scheduled workflow"""
    logger = get_run_logger()
    logger.info("Starting scheduled daily workflow...")
    
    try:
        # Health check
        is_healthy = health_check()
        if not is_healthy:
            logger.error("Health check failed. Aborting workflow.")
            return None
        
        # Extract data
        daily_data = extract_daily_data()
        
        # Process data
        processed_data = process_daily_data(daily_data)
        
        # Generate report
        daily_report = generate_daily_report(processed_data)
        
        # Save data
        output_dir = save_processed_data(processed_data, daily_report)
        
        # Send notifications
        notifications_sent = send_notifications(daily_report, output_dir)
        
        # Cleanup old data
        files_removed = cleanup_old_data()
        
        logger.info(f"Scheduled workflow completed successfully!")
        logger.info(f"Output: {output_dir}")
        logger.info(f"Files cleaned up: {files_removed}")
        
        return {
            'output_dir': output_dir,
            'records_processed': len(processed_data),
            'notifications_sent': notifications_sent,
            'files_cleaned': files_removed
        }
        
    except Exception as e:
        logger.error(f"Scheduled workflow failed with error: {e}")
        raise

if __name__ == "__main__":
    # Run the scheduled workflow
    result = scheduled_daily_workflow()
    print(f"Scheduled workflow result: {result}") 