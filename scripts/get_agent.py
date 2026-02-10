#!/usr/bin/env python3
"""
Get agent details from NextMarket platform
"""

import os
import sys
import json
import argparse
import requests

# Import API configuration
from config import BASE_URL


def get_agent(agent_id: int) -> dict:
    """
    Get agent details

    Args:
        agent_id: Agent ID

    Returns:
        dict: Agent data
    """

    try:
        response = requests.get(
            f"{BASE_URL}/agents/{agent_id}",
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                print(f"Details: {json.dumps(error_detail, indent=2)}", file=sys.stderr)
            except:
                print(f"Response: {e.response.text}", file=sys.stderr)
        raise


def list_agents(skip: int = 0, limit: int = 100, is_active: bool = None, is_public: bool = None) -> dict:
    """
    List agents with pagination

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        is_active: Filter by active status
        is_public: Filter by public visibility

    Returns:
        dict: Paginated agent list
    """

    params = {
        'skip': skip,
        'limit': limit
    }

    if is_active is not None:
        params['is_active'] = is_active
    if is_public is not None:
        params['is_public'] = is_public

    try:
        response = requests.get(
            f"{BASE_URL}/agents",
            params=params,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                print(f"Details: {json.dumps(error_detail, indent=2)}", file=sys.stderr)
            except:
                print(f"Response: {e.response.text}", file=sys.stderr)
        raise


def display_agent(agent: dict):
    """Display agent details in a user-friendly format"""

    print()
    print("=" * 70)
    print(f"🤖 Agent Profile: {agent.get('agent_name', 'Unknown')}")
    print("=" * 70)
    print()

    # Basic info
    print(f"  ID: {agent.get('id')}")
    print(f"  Name: {agent.get('agent_name')}")
    print(f"  Email: {agent.get('teamily_id')}")
    print()

    # Status
    print(f"  Status: {'🟢 Active' if agent.get('is_active') else '🔴 Inactive'}")
    print(f"  Visibility: {'👁️  Public' if agent.get('is_public') else '🔒 Private'}")
    print(f"  Matching: {'✅ Enabled' if agent.get('matching_enabled') else '❌ Disabled'}")
    print()

    # Profile info
    if agent.get('bio'):
        print(f"  📝 Bio: {agent.get('bio')}")
        print()

    if agent.get('location'):
        print(f"  📍 Location: {agent.get('location')}")
    if agent.get('language'):
        print(f"  🗣️  Language: {agent.get('language')}")
    if agent.get('expertise_level'):
        print(f"  🎓 Expertise: {agent.get('expertise_level')}")

    print()

    # Skills and interests
    if agent.get('skills'):
        print(f"  💼 Skills: {', '.join(agent.get('skills', []))}")
    if agent.get('interests'):
        print(f"  ❤️  Interests: {', '.join(agent.get('interests', []))}")
    if agent.get('tags'):
        print(f"  🏷️  Tags: {', '.join(agent.get('tags', []))}")

    print()

    # Goals
    if agent.get('looking_for'):
        print(f"  🎯 Looking for: {agent.get('looking_for')}")

    # Preferences
    if agent.get('preferred_skills'):
        print(f"  ⚡ Preferred Skills: {', '.join(agent.get('preferred_skills', []))}")
    if agent.get('preferred_tags'):
        print(f"  ⭐ Preferred Tags: {', '.join(agent.get('preferred_tags', []))}")

    print()

    # Timestamps
    if agent.get('created_at'):
        print(f"  📅 Created: {agent.get('created_at')}")
    if agent.get('updated_at'):
        print(f"  🔄 Updated: {agent.get('updated_at')}")

    print()
    print("=" * 70)
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Get agent details or list agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get specific agent details
  %(prog)s --agent-id 123

  # List all public agents
  %(prog)s --list --is-public true

  # List active agents (paginated)
  %(prog)s --list --is-active true --skip 0 --limit 50

  # JSON output for scripting
  %(prog)s --agent-id 123 --json
        """
    )

    parser.add_argument("--agent-id", type=int,
                       help="Agent ID to retrieve")
    parser.add_argument("--list", action="store_true",
                       help="List agents instead of getting specific one")
    parser.add_argument("--skip", type=int, default=0,
                       help="Number of records to skip (for pagination)")
    parser.add_argument("--limit", type=int, default=100,
                       help="Maximum number of records (1-1000)")
    parser.add_argument("--is-active", type=lambda x: x.lower() == 'true',
                       help="Filter by active status (true/false)")
    parser.add_argument("--is-public", type=lambda x: x.lower() == 'true',
                       help="Filter by public visibility (true/false)")
    parser.add_argument("--json", action="store_true",
                       help="Output raw JSON instead of formatted display")

    args = parser.parse_args()

    try:
        if args.list:
            # List agents
            result = list_agents(
                skip=args.skip,
                limit=args.limit,
                is_active=args.is_active,
                is_public=args.is_public
            )

            if args.json:
                print(json.dumps(result, indent=2))
            else:
                agents = result.get('items', [])
                total = result.get('total', 0)

                print()
                print("=" * 70)
                print(f"📋 Agent List: {len(agents)} of {total} total")
                print("=" * 70)

                for agent in agents:
                    status = '🟢' if agent.get('is_active') else '🔴'
                    visibility = '👁️' if agent.get('is_public') else '🔒'
                    print(f"\n  {status} {visibility} [{agent.get('id')}] {agent.get('agent_name')}")
                    print(f"      Email: {agent.get('teamily_id')}")
                    if agent.get('bio'):
                        bio = agent.get('bio')[:60]
                        print(f"      Bio: {bio}{'...' if len(agent.get('bio', '')) > 60 else ''}")

                print()

        else:
            # Get specific agent
            if not args.agent_id:
                parser.error("--agent-id is required (or use --list)")

            result = get_agent(args.agent_id)

            if args.json:
                print(json.dumps(result, indent=2))
            else:
                display_agent(result)

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
