#!/usr/bin/env python3
"""
Dagster Setup Script
Configures and initializes Dagster for local deployment
"""

import os
import subprocess
import logging
import time
import requests
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_dagster_installation():
    """Check if Dagster is installed"""
    try:
        import dagster
        logger.info(f"Dagster version: {dagster.__version__}")
        return True
    except ImportError:
        logger.error("Dagster is not installed. Please install it first:")
        logger.error("pip install dagster dagster-webserver")
        return False

def create_dagster_config():
    """Create Dagster configuration"""
    logger.info("Creating Dagster configuration...")
    
    # Create config directory
    config_dir = Path("configs")
    config_dir.mkdir(exist_ok=True)
    
    # Create dagster.yaml configuration
    dagster_config = """
# Dagster Configuration
instance:
  local_artifact_storage:
    base_dir: "./data/dagster"

run_storage:
  sqlite:
    base_dir: "./data/dagster/runs"

event_log_storage:
  sqlite:
    base_dir: "./data/dagster/events"

schedule_storage:
  sqlite:
    base_dir: "./data/dagster/schedules"

sensor_storage:
  sqlite:
    base_dir: "./data/dagster/sensors"

asset_storage:
  sqlite:
    base_dir: "./data/dagster/assets"

logging:
  python_logs:
    managed_python_loggers:
      - dagster
      - dagster.core
      - dagster.daemon
    dagster_handler_config:
      handlers:
        console:
          config:
            log_level: INFO
        file:
          config:
            log_level: INFO
            filename: "./logs/dagster.log"

telemetry:
  enabled: false

feature_flags:
  enable_asset_observability: true
  enable_asset_checks: true
  enable_asset_auto_materialize: true

ui:
  brand_title: "Data Engineering Demos"
  feature_flags:
    enable_asset_graph: true
    enable_asset_checks: true
    enable_asset_observability: true
"""
    
    with open(config_dir / "dagster.yaml", "w") as f:
        f.write(dagster_config)
    
    logger.info("Dagster configuration created")

def create_data_directories():
    """Create necessary data directories"""
    logger.info("Creating data directories...")
    
    directories = [
        "data/raw",
        "data/processed", 
        "data/analytics",
        "data/logs",
        "data/dagster",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")

def start_dagster_server():
    """Start Dagster server"""
    logger.info("Starting Dagster server...")
    
    try:
        # Start server in background
        process = subprocess.Popen(
            ["dagster", "dev"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a bit for server to start
        time.sleep(5)
        
        # Check if server is running
        try:
            response = requests.get("http://localhost:3000/health")
            if response.status_code == 200:
                logger.info("Dagster server started successfully")
                return True
            else:
                logger.error("Dagster server health check failed")
                return False
        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to Dagster server")
            return False
            
    except Exception as e:
        logger.error(f"Error starting Dagster server: {e}")
        return False

def create_sample_data():
    """Create sample data for assets"""
    logger.info("Creating sample data...")
    
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    
    # Create sample sales data
    np.random.seed(42)
    n_records = 100
    
    sales_data = []
    for i in range(n_records):
        sales_data.append({
            'sale_id': i + 1,
            'sale_date': (datetime.now() - timedelta(days=np.random.randint(1, 30))).strftime('%Y-%m-%d'),
            'product_id': np.random.randint(1, 21),
            'customer_id': np.random.randint(1, 101),
            'quantity': np.random.randint(1, 10),
            'unit_price': round(np.random.uniform(10, 500), 2),
            'total_amount': 0  # Will be calculated
        })
    
    df = pd.DataFrame(sales_data)
    df['total_amount'] = df['quantity'] * df['unit_price']
    
    # Save to data directory
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/sample_sales.csv', index=False)
    logger.info(f"Created sample data: {len(df)} records")

def run_health_check():
    """Run health check on Dagster setup"""
    logger.info("Running health check...")
    
    checks = {
        'dagster_installed': check_dagster_installation(),
        'directories_exist': all(Path(d).exists() for d in ['data', 'configs', 'assets']),
        'sample_data_exists': Path('data/raw/sample_sales.csv').exists()
    }
    
    # Check server if running
    try:
        response = requests.get("http://localhost:3000/health", timeout=5)
        checks['server_running'] = response.status_code == 200
    except:
        checks['server_running'] = False
    
    # Report results
    logger.info("Health check results:")
    for check, status in checks.items():
        status_str = "✓ PASS" if status else "✗ FAIL"
        logger.info(f"  {check}: {status_str}")
    
    all_passed = all(checks.values())
    logger.info(f"Overall status: {'✓ PASS' if all_passed else '✗ FAIL'}")
    
    return all_passed

def main():
    """Main setup function"""
    logger.info("Starting Dagster setup...")
    
    # Check Dagster installation
    if not check_dagster_installation():
        return False
    
    # Create configuration
    create_dagster_config()
    
    # Create directories
    create_data_directories()
    
    # Create sample data
    create_sample_data()
    
    # Start server (optional - user can start manually)
    logger.info("Note: Dagster server can be started manually with 'dagster dev'")
    
    # Run health check
    health_passed = run_health_check()
    
    if health_passed:
        logger.info("Dagster setup completed successfully!")
        logger.info("Next steps:")
        logger.info("1. Start Dagster server: dagster dev")
        logger.info("2. Access UI: http://localhost:3000")
        logger.info("3. Materialize assets: dagster asset materialize --select data_assets")
    else:
        logger.error("Dagster setup completed with issues. Please check the logs above.")
    
    return health_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 