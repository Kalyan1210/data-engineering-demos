#!/usr/bin/env python3
"""
Spark Streaming Job Runner
Runs the Spark Structured Streaming job for Kafka data processing
"""

import sys
import os
import subprocess
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_spark_job():
    """Run the Spark streaming job"""
    try:
        # Set environment variables for Spark
        env = os.environ.copy()
        env['SPARK_HOME'] = '/opt/bitnami/spark'
        
        # Path to the Spark streaming script
        script_path = os.path.join(os.path.dirname(__file__), '../app/spark_streaming.py')
        
        logger.info("Starting Spark Structured Streaming job...")
        logger.info(f"Script path: {script_path}")
        
        # Run the Spark job
        process = subprocess.Popen([
            'python', script_path
        ], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        logger.info("Spark job started successfully")
        logger.info("Press Ctrl+C to stop")
        
        # Wait for the process
        process.wait()
        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, stopping Spark job...")
        if 'process' in locals():
            process.terminate()
            process.wait()
    except Exception as e:
        logger.error(f"Error running Spark job: {e}")
        sys.exit(1)

def check_spark_environment():
    """Check if Spark environment is properly set up"""
    try:
        # Check if Spark is available
        result = subprocess.run(['spark-submit', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("Spark environment is ready")
            return True
        else:
            logger.error("Spark environment not found")
            return False
    except FileNotFoundError:
        logger.error("spark-submit not found. Please ensure Spark is installed.")
        return False

def main():
    """Main function"""
    logger.info("Checking Spark environment...")
    
    if not check_spark_environment():
        logger.error("Spark environment check failed. Please ensure Spark is properly installed.")
        sys.exit(1)
    
    # Wait a bit for Kafka to be ready
    logger.info("Waiting for Kafka to be ready...")
    time.sleep(10)
    
    # Run the Spark job
    run_spark_job()

if __name__ == "__main__":
    main() 