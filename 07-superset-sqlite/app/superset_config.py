# Superset Configuration for SQLite Demo

import os

# Flask App Builder configuration
APP_NAME = "Superset SQLite Demo"
APP_ICON = "/static/assets/images/superset-logo-horiz.png"

# Database configuration
SQLALCHEMY_DATABASE_URI = "sqlite:////app/superset_home/superset.db"

# Security settings
SECRET_KEY = "your-secret-key-here"
WTF_CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = None

# Feature flags
FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
    "DASHBOARD_NATIVE_FILTERS": True,
    "DASHBOARD_CROSS_FILTERS": True,
    "DASHBOARD_RBAC": True,
    "ENABLE_EXPLORE_JSON_CSRF_PROTECTION": False,
    "ENABLE_EXPLORE_DRAG_AND_DROP": True,
    "ENABLE_DASHBOARD_NATIVE_FILTERS_SET": True,
}

# Cache configuration
CACHE_CONFIG = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
}

# SQL Lab settings
SQLLAB_CTAS_NO_LIMIT = True
SQLLAB_TIMEOUT = 300
SQLLAB_DEFAULT_DBID = None

# Row limit
ROW_LIMIT = 5000
VIZ_ROW_LIMIT = 10000

# Webdriver configuration
WEBDRIVER_BASEURL = "http://superset:8088/"
WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL

# Custom CSS
CUSTOM_CSS = """
.navbar-brand {
    font-weight: bold;
}
"""

# Custom JavaScript
CUSTOM_JS = """
console.log('Superset SQLite Demo loaded');
""" 