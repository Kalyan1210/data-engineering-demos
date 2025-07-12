#!/usr/bin/env python3
"""
Data Loading Script
Generates and loads sample business data for the Superset demo
"""

import sys
import os
import logging

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))

from data_generator import main as generate_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to generate and load data"""
    try:
        logger.info("Starting data generation...")
        
        # Generate sample data
        generate_data()
        
        logger.info("Data generation completed successfully!")
        logger.info("Sample data files created in data/ directory")
        logger.info("SQLite database created at data/database/business.db")
        
    except Exception as e:
        logger.error(f"Error generating data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 