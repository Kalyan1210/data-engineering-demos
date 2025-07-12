#!/usr/bin/env python3
"""
Dagster Definitions for Data Assets
Defines the asset groups and configurations for data assets
"""

from dagster import Definitions, load_assets_from_modules
from . import data_assets, etl_assets, analytics_assets

# Load all assets from modules
all_assets = load_assets_from_modules([data_assets, etl_assets, analytics_assets])

# Create definitions
defs = Definitions(
    assets=all_assets,
    resources={
        # Add resources here if needed
    }
) 