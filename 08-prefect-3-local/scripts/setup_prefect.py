#!/usr/bin/env python3
"""
Prefect Setup Script
Configures and initializes Prefect for local deployment
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

def check_prefect_installation():
    """Check if Prefect is installed"""
    try:
        import prefect
        logger.info(f"Prefect version: {prefect.__version__}")
        return True
    except ImportError:
        logger.error("Prefect is not installed. Please install it first:")
        logger.error("pip install prefect")
        return False

def create_prefect_config():
    """Create Prefect configuration"""
    logger.info("Creating Prefect configuration...")
    
    # Create config directory
    config_dir = Path("configs")
    config_dir.mkdir(exist_ok=True)
    
    # Create prefect.yaml configuration
    prefect_config = """
# Prefect Configuration
name: "prefect-3-local"
description: "Local Prefect deployment for data engineering demos"

# Work pools
work_pools:
  - name: "default"
    work_queues:
      - name: "default"
        description: "Default work queue"

# Deployments
deployments:
  - name: "data-pipeline"
    entrypoint: "workflows/data_pipeline.py:data_pipeline"
    work_pool:
      name: "default"
      work_queue_name: "default"
    schedule:
      cron: "0 2 * * *"  # Daily at 2 AM
    
  - name: "etl-workflow"
    entrypoint: "workflows/etl_workflow.py:etl_workflow"
    work_pool:
      name: "default"
      work_queue_name: "default"
    schedule:
      cron: "0 4 * * *"  # Daily at 4 AM
    
  - name: "scheduled-workflow"
    entrypoint: "workflows/scheduled_workflow.py:scheduled_daily_workflow"
    work_pool:
      name: "default"
      work_queue_name: "default"
    schedule:
      cron: "0 6 * * *"  # Daily at 6 AM

# Storage
storage:
  type: "local"
  path: "./data"

# Logging
logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
"""
    
    with open(config_dir / "prefect.yaml", "w") as f:
        f.write(prefect_config)
    
    logger.info("Prefect configuration created")

def create_data_directories():
    """Create necessary data directories"""
    logger.info("Creating data directories...")
    
    directories = [
        "data/raw",
        "data/processed", 
        "data/logs",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")

def start_prefect_server():
    """Start Prefect server"""
    logger.info("Starting Prefect server...")
    
    try:
        # Start server in background
        process = subprocess.Popen(
            ["prefect", "server", "start"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a bit for server to start
        time.sleep(5)
        
        # Check if server is running
        try:
            response = requests.get("http://localhost:4200/api/health")
            if response.status_code == 200:
                logger.info("Prefect server started successfully")
                return True
            else:
                logger.error("Prefect server health check failed")
                return False
        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to Prefect server")
            return False
            
    except Exception as e:
        logger.error(f"Error starting Prefect server: {e}")
        return False

def create_work_pool():
    """Create work pool for task execution"""
    logger.info("Creating work pool...")
    
    try:
        subprocess.run([
            "prefect", "work-pool", "create", "default"
        ], check=True)
        logger.info("Work pool 'default' created")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error creating work pool: {e}")
        return False

def deploy_workflows():
    """Deploy workflows to Prefect"""
    logger.info("Deploying workflows...")
    
    workflows = [
        "workflows/data_pipeline.py",
        "workflows/etl_workflow.py", 
        "workflows/scheduled_workflow.py"
    ]
    
    for workflow in workflows:
        if os.path.exists(workflow):
            try:
                logger.info(f"Deploying {workflow}...")
                subprocess.run([
                    "prefect", "deploy", workflow
                ], check=True)
                logger.info(f"Successfully deployed {workflow}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Error deploying {workflow}: {e}")
        else:
            logger.warning(f"Workflow file not found: {workflow}")

def create_sample_data():
    """Create sample data for workflows"""
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
    """Run health check on Prefect setup"""
    logger.info("Running health check...")
    
    checks = {
        'prefect_installed': check_prefect_installation(),
        'directories_exist': all(Path(d).exists() for d in ['data', 'configs', 'workflows']),
        'sample_data_exists': Path('data/raw/sample_sales.csv').exists()
    }
    
    # Check server if running
    try:
        response = requests.get("http://localhost:4200/api/health", timeout=5)
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
    logger.info("Starting Prefect setup...")
    
    # Check Prefect installation
    if not check_prefect_installation():
        return False
    
    # Create configuration
    create_prefect_config()
    
    # Create directories
    create_data_directories()
    
    # Create sample data
    create_sample_data()
    
    # Start server (optional - user can start manually)
    logger.info("Note: Prefect server can be started manually with 'prefect server start'")
    
    # Create work pool
    create_work_pool()
    
    # Deploy workflows
    deploy_workflows()
    
    # Run health check
    health_passed = run_health_check()
    
    if health_passed:
        logger.info("Prefect setup completed successfully!")
        logger.info("Next steps:")
        logger.info("1. Start Prefect server: prefect server start")
        logger.info("2. Start worker: prefect worker start --pool default")
        logger.info("3. Access UI: http://localhost:4200")
        logger.info("4. Run workflows: python workflows/data_pipeline.py")
    else:
        logger.error("Prefect setup completed with issues. Please check the logs above.")
    
    return health_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 