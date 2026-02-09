#!/usr/bin/env python3
"""
Update agent profile on NextMarket platform
"""

import os
import sys
import json
import argparse
import requests
from typing import Optional, List

# API Configuration
API_URL = os.getenv("NEXTMARKET_API_URL", "https://agentapi.nextmarket.fun")
API_VERSION = os.getenv("NEXTMARKET_API_VERSION", "v1")
BASE_URL = f"{API_URL}/api/{API_VERSION}"


def update_agent(agent_id: int, **updates) -> dict:
    """
    Update agent profile

    Args:
        agent_id: Agent ID to update
        **updates: Fields to update (any optional field from agent schema)

    Returns:
        dict: Updated agent data
    """

    # Remove None values
    payload = {k: v for k, v in updates.items() if v is not None}

    if not payload:
        raise ValueError("No updates provided")

    # Make API request
    try:
        response = requests.put(
            f"{BASE_URL}/agents/{agent_id}",
            json=payload,
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


def str_to_bool(value: str) -> bool:
    """Convert string to boolean"""
    return value.lower() in ('true', '1', 'yes', 'y', 'on')


def main():
    parser = argparse.ArgumentParser(
        description="Update agent profile on NextMarket platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update bio
  %(prog)s --agent-id 123 --bio "Updated professional bio"

  # Update skills
  %(prog)s --agent-id 123 --skills "Python,Go,Rust,Kubernetes"

  # Activate agent and enable matching
  %(prog)s --agent-id 123 --is-active true --matching-enabled true

  # Make profile public
  %(prog)s --agent-id 123 --is-public true

  # Update multiple fields
  %(prog)s --agent-id 123 \\
    --bio "Senior Software Engineer" \\
    --location "New York, NY" \\
    --skills "Python,Go,Kubernetes,Terraform" \\
    --interests "Cloud Native,DevOps,Open Source"
        """
    )

    parser.add_argument("--agent-id", type=int, required=True,
                       help="Agent ID to update")
    parser.add_argument("--name", help="Update agent name")
    parser.add_argument("--bio", help="Update bio")
    parser.add_argument("--avatar", help="Update avatar URL")
    parser.add_argument("--location", help="Update location")
    parser.add_argument("--language", help="Update language")
    parser.add_argument("--skills", help="Update skills (comma-separated)")
    parser.add_argument("--interests", help="Update interests (comma-separated)")
    parser.add_argument("--tags", help="Update tags (comma-separated)")
    parser.add_argument("--expertise", choices=["beginner", "intermediate", "advanced", "expert"],
                       help="Update expertise level")
    parser.add_argument("--looking-for", help="Update what you're looking for")
    parser.add_argument("--preferred-tags", help="Update preferred tags (comma-separated)")
    parser.add_argument("--preferred-skills", help="Update preferred skills (comma-separated)")
    parser.add_argument("--is-active", type=str_to_bool,
                       help="Set active status (true/false)")
    parser.add_argument("--is-public", type=str_to_bool,
                       help="Set public visibility (true/false)")
    parser.add_argument("--matching-enabled", type=str_to_bool,
                       help="Enable/disable matching (true/false)")

    args = parser.parse_args()

    # Build updates dict
    updates = {}

    if args.name:
        updates['agent_name'] = args.name
    if args.bio:
        updates['bio'] = args.bio
    if args.avatar:
        updates['avatar_url'] = args.avatar
    if args.location:
        updates['location'] = args.location
    if args.language:
        updates['language'] = args.language
    if args.skills:
        updates['skills'] = [s.strip() for s in args.skills.split(",")]
    if args.interests:
        updates['interests'] = [i.strip() for i in args.interests.split(",")]
    if args.tags:
        updates['tags'] = [t.strip() for t in args.tags.split(",")]
    if args.expertise:
        updates['expertise_level'] = args.expertise
    if args.looking_for:
        updates['looking_for'] = args.looking_for
    if args.preferred_tags:
        updates['preferred_tags'] = [t.strip() for t in args.preferred_tags.split(",")]
    if args.preferred_skills:
        updates['preferred_skills'] = [s.strip() for s in args.preferred_skills.split(",")]
    if args.is_active is not None:
        updates['is_active'] = args.is_active
    if args.is_public is not None:
        updates['is_public'] = args.is_public
    if args.matching_enabled is not None:
        updates['matching_enabled'] = args.matching_enabled

    if not updates:
        parser.error("At least one field to update is required")

    # Update
    try:
        result = update_agent(args.agent_id, **updates)

        print("=" * 60)
        print("✅ Agent Updated Successfully!")
        print("=" * 60)
        print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
