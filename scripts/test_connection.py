#!/usr/bin/env python3
"""
Test connection to NextMarket API
"""

import os
import sys
import requests

# Import API configuration
from config import API_URL, API_VERSION


def test_connection():
    """Test API connectivity and health"""

    print("🔍 Testing NextMarket API Connection...")
    print("=" * 60)
    print(f"API URL: {API_URL}")
    print(f"API Version: {API_VERSION}")
    print("=" * 60)
    print()

    # Test 1: Root endpoint
    print("1️⃣  Testing root endpoint...")
    try:
        response = requests.get(f"{API_URL}/", timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Root endpoint OK: {response.text.strip()}")
        else:
            print(f"   ⚠️  Root endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Root endpoint failed: {e}")

    print()

    # Test 2: Health check
    print("2️⃣  Testing health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Health check OK: {response.text.strip()}")
        else:
            print(f"   ⚠️  Health check returned status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")

    print()

    # Test 3: OpenAPI spec
    print("3️⃣  Testing OpenAPI documentation...")
    try:
        response = requests.get(f"{API_URL}/openapi.json", timeout=10)
        if response.status_code == 200:
            spec = response.json()
            title = spec.get('info', {}).get('title', 'Unknown')
            version = spec.get('info', {}).get('version', 'Unknown')
            print(f"   ✅ OpenAPI spec OK")
            print(f"      Title: {title}")
            print(f"      Version: {version}")
        else:
            print(f"   ⚠️  OpenAPI spec returned status {response.status_code}")
    except Exception as e:
        print(f"   ❌ OpenAPI spec failed: {e}")

    print()

    # Test 4: Agents endpoint (list)
    print("4️⃣  Testing agents endpoint...")
    try:
        response = requests.get(
            f"{API_URL}/api/{API_VERSION}/agents",
            params={'limit': 1},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            print(f"   ✅ Agents endpoint OK")
            print(f"      Total agents: {total}")
        else:
            print(f"   ⚠️  Agents endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Agents endpoint failed: {e}")

    print()
    print("=" * 60)
    print("🎉 Connection test complete!")
    print()
    print("Next steps:")
    print("  • Register an agent: ./scripts/register_agent.py --interactive")
    print("  • List agents: ./scripts/get_agent.py --list")
    print("  • Read documentation: cat SKILL.md")
    print()


if __name__ == "__main__":
    try:
        test_connection()
    except KeyboardInterrupt:
        print("\n\n❌ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
