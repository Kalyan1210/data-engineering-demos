#!/usr/bin/env python3
"""
Superset Admin User Creation Script
Creates the admin user for Superset access
"""

import subprocess
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_admin_user():
    """Create Superset admin user"""
    try:
        logger.info("Creating Superset admin user...")
        
        # Create admin user
        subprocess.run([
            "docker-compose", "exec", "superset",
            "superset", "fab", "create-admin",
            "--username", "admin",
            "--firstname", "Superset",
            "--lastname", "Admin",
            "--email", "admin@superset.com",
            "--password", "admin"
        ], check=True)
        
        logger.info("Admin user created successfully!")
        logger.info("Username: admin")
        logger.info("Password: admin")
        
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error creating admin user: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

def main():
    """Main function"""
    logger.info("Starting admin user creation...")
    
    # Wait a bit for Superset to be ready
    logger.info("Waiting for Superset to be ready...")
    time.sleep(10)
    
    # Create admin user
    if not create_admin_user():
        logger.error("Failed to create admin user")
        return False
    
    logger.info("Admin user creation completed successfully!")
    logger.info("You can now access Superset at http://localhost:8088")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 