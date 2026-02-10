#!/usr/bin/env python3
"""
Global Configuration for Agent Social Skill
Centralized API configuration management
"""

import os

# API Configuration
# Default API URL - can be overridden by NEXTMARKET_API_URL environment variable
DEFAULT_API_URL = "https://agentapi.agentapp.space"
DEFAULT_API_VERSION = "v1"

# Load from environment or use defaults
API_URL = os.getenv("NEXTMARKET_API_URL", DEFAULT_API_URL)
API_VERSION = os.getenv("NEXTMARKET_API_VERSION", DEFAULT_API_VERSION)

# Construct base URL for API endpoints
BASE_URL = f"{API_URL}/api/{API_VERSION}"


def get_api_url() -> str:
    """Get the configured API URL"""
    return API_URL


def get_base_url() -> str:
    """Get the full base URL for API endpoints"""
    return BASE_URL


def get_api_version() -> str:
    """Get the API version"""
    return API_VERSION
