#!/usr/bin/env python3
"""
Kafka Data Producer Script
Generates sample streaming data for the Kafka + Spark demo
"""

import sys
import os
import logging
from time import sleep

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))

from kafka_producer import produce_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the Kafka producer"""
    try:
        logger.info("Starting Kafka data producer...")
        logger.info("Press Ctrl+C to stop")
        
        # Start producing data
        produce_data()
        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Error in data producer: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 