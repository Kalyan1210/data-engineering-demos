#!/usr/bin/env python3
"""
Kafka Topic Setup Script
Creates the required Kafka topics for the streaming demo
"""

import sys
import os
import time
import logging
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
TOPICS = [
    'user_events',
    'sensor_data', 
    'transactions'
]

def wait_for_kafka():
    """Wait for Kafka to be ready"""
    logger.info("Waiting for Kafka to be ready...")
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
            admin_client.list_topics()
            admin_client.close()
            logger.info("Kafka is ready!")
            return True
        except Exception as e:
            retry_count += 1
            logger.info(f"Waiting for Kafka... ({retry_count}/{max_retries})")
            time.sleep(2)
    
    logger.error("Kafka did not become ready in time")
    return False

def create_topics():
    """Create Kafka topics"""
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        
        # Create topic configurations
        topic_list = []
        for topic_name in TOPICS:
            topic = NewTopic(
                name=topic_name,
                num_partitions=3,
                replication_factor=1
            )
            topic_list.append(topic)
        
        # Create topics
        logger.info("Creating Kafka topics...")
        admin_client.create_topics(topic_list)
        
        # List created topics
        existing_topics = admin_client.list_topics()
        logger.info(f"Available topics: {existing_topics}")
        
        admin_client.close()
        logger.info("Kafka topics created successfully!")
        
    except TopicAlreadyExistsError:
        logger.info("Topics already exist, skipping creation")
    except Exception as e:
        logger.error(f"Error creating topics: {e}")
        sys.exit(1)

def main():
    """Main function"""
    logger.info("Setting up Kafka topics...")
    
    # Wait for Kafka to be ready
    if not wait_for_kafka():
        sys.exit(1)
    
    # Create topics
    create_topics()
    
    logger.info("Kafka setup completed successfully!")

if __name__ == "__main__":
    main() 