#!/usr/bin/env python3
"""
Superset Initialization Script
Sets up the Superset database and basic configuration
"""

import os
import subprocess
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def wait_for_superset():
    """Wait for Superset to be ready"""
    logger.info("Waiting for Superset to be ready...")
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            import requests
            response = requests.get("http://localhost:8088/health")
            if response.status_code == 200:
                logger.info("Superset is ready!")
                return True
        except Exception:
            pass
        
        retry_count += 1
        logger.info(f"Waiting for Superset... ({retry_count}/{max_retries})")
        time.sleep(2)
    
    logger.error("Superset did not become ready in time")
    return False

def init_superset():
    """Initialize Superset database"""
    try:
        logger.info("Initializing Superset database...")
        
        # Run Superset database upgrade
        subprocess.run([
            "docker-compose", "exec", "superset", 
            "superset", "db", "upgrade"
        ], check=True)
        
        logger.info("Superset database upgraded successfully")
        
        # Initialize Superset
        subprocess.run([
            "docker-compose", "exec", "superset", 
            "superset", "init"
        ], check=True)
        
        logger.info("Superset initialized successfully")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error initializing Superset: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False
    
    return True

def main():
    """Main function"""
    logger.info("Starting Superset initialization...")
    
    # Wait for Superset to be ready
    if not wait_for_superset():
        logger.error("Superset is not available")
        return False
    
    # Initialize Superset
    if not init_superset():
        logger.error("Failed to initialize Superset")
        return False
    
    logger.info("Superset initialization completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 