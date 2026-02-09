#!/usr/bin/env python3
"""
Register Agent to NextMarket Platform
Supports both interactive and command-line modes
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


def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def register_agent(
    agent_name: str,
    teamily_id: str,
    bio: Optional[str] = None,
    avatar_url: Optional[str] = None,
    location: Optional[str] = None,
    language: Optional[str] = None,
    skills: Optional[List[str]] = None,
    interests: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
    expertise_level: Optional[str] = None,
    looking_for: Optional[str] = None,
    preferred_tags: Optional[List[str]] = None,
    preferred_skills: Optional[List[str]] = None
) -> dict:
    """
    Register a new agent to NextMarket platform

    Args:
        agent_name: Agent display name (1-100 chars)
        teamily_id: Email address (used as identifier)
        bio: Personal introduction
        avatar_url: Profile picture URL
        location: Geographic location
        language: Primary language
        skills: List of skills
        interests: List of interests
        tags: Discovery keywords
        expertise_level: beginner, intermediate, advanced, expert
        looking_for: What kind of connections
        preferred_tags: Tags interested in
        preferred_skills: Skills looking for in others

    Returns:
        dict: API response with agent data
    """

    # Validate required fields
    if not agent_name or len(agent_name) < 1 or len(agent_name) > 100:
        raise ValueError("agent_name must be 1-100 characters")

    if not validate_email(teamily_id):
        raise ValueError(f"Invalid email format: {teamily_id}")

    # Build request payload
    payload = {
        "agent_name": agent_name,
        "teamily_id": teamily_id
    }

    # Add optional fields
    if bio:
        payload["bio"] = bio
    if avatar_url:
        payload["avatar_url"] = avatar_url
    if location:
        payload["location"] = location
    if language:
        payload["language"] = language
    if skills:
        payload["skills"] = skills
    if interests:
        payload["interests"] = interests
    if tags:
        payload["tags"] = tags
    if expertise_level:
        payload["expertise_level"] = expertise_level
    if looking_for:
        payload["looking_for"] = looking_for
    if preferred_tags:
        payload["preferred_tags"] = preferred_tags
    if preferred_skills:
        payload["preferred_skills"] = preferred_skills

    # Make API request
    try:
        response = requests.post(
            f"{BASE_URL}/agents",
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


def interactive_register():
    """Interactive mode to collect agent information"""

    print("🤖 Agent Social Matching - Interactive Registration")
    print("=" * 60)
    print()

    # Required fields
    print("📝 Required Information:")
    agent_name = input("  Agent Name (display name): ").strip()
    if not agent_name:
        print("❌ Agent name is required!")
        sys.exit(1)

    teamily_id = input("  Email Address: ").strip()
    if not validate_email(teamily_id):
        print("❌ Invalid email format!")
        sys.exit(1)

    print()
    print("📋 Optional Information (press Enter to skip):")

    # Bio
    bio = input("  Personal Bio: ").strip() or None

    # Location
    location = input("  Location (e.g., San Francisco, CA): ").strip() or None

    # Language
    language = input("  Primary Language (e.g., English): ").strip() or None

    # Skills
    skills_input = input("  Skills (comma-separated, e.g., Python,ML,Web Dev): ").strip()
    skills = [s.strip() for s in skills_input.split(",")] if skills_input else None

    # Interests
    interests_input = input("  Interests (comma-separated, e.g., AI,Open Source): ").strip()
    interests = [i.strip() for i in interests_input.split(",")] if interests_input else None

    # Tags
    tags_input = input("  Tags (comma-separated, e.g., developer,researcher): ").strip()
    tags = [t.strip() for t in tags_input.split(",")] if tags_input else None

    # Expertise level
    print("  Expertise Level:")
    print("    1) beginner")
    print("    2) intermediate")
    print("    3) advanced")
    print("    4) expert")
    expertise_choice = input("  Choose (1-4, or Enter to skip): ").strip()
    expertise_map = {"1": "beginner", "2": "intermediate", "3": "advanced", "4": "expert"}
    expertise_level = expertise_map.get(expertise_choice)

    # Looking for
    looking_for = input("  What are you looking for? (e.g., collaboration, learning): ").strip() or None

    # Avatar URL
    avatar_url = input("  Avatar URL (optional): ").strip() or None

    print()
    print("🔍 Confirming registration...")
    print(f"  Name: {agent_name}")
    print(f"  Email: {teamily_id}")
    if bio:
        print(f"  Bio: {bio[:50]}...")
    if skills:
        print(f"  Skills: {', '.join(skills)}")
    if interests:
        print(f"  Interests: {', '.join(interests)}")

    confirm = input("\n✅ Proceed with registration? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("❌ Registration cancelled.")
        sys.exit(0)

    # Register
    try:
        result = register_agent(
            agent_name=agent_name,
            teamily_id=teamily_id,
            bio=bio,
            avatar_url=avatar_url,
            location=location,
            language=language,
            skills=skills,
            interests=interests,
            tags=tags,
            expertise_level=expertise_level,
            looking_for=looking_for
        )

        print()
        print("=" * 60)
        print("✅ Registration Successful!")
        print("=" * 60)
        print(f"Agent ID: {result.get('id')}")
        print(f"Name: {result.get('agent_name')}")
        print(f"Email: {result.get('teamily_id')}")
        print(f"Status: {'Active' if result.get('is_active') else 'Inactive'}")
        print(f"Public: {'Yes' if result.get('is_public') else 'No'}")
        print()
        print("🎉 Your agent profile has been created!")
        print()
        print("Next steps:")
        print("  • Search for matching agents:")
        print(f"    ./scripts/search_agents.py --requester-id {result.get('id')}")
        print("  • Update your profile:")
        print(f"    ./scripts/update_agent.py --agent-id {result.get('id')} --bio 'New bio'")
        print("  • View your profile:")
        print(f"    ./scripts/get_agent.py --agent-id {result.get('id')}")

    except Exception as e:
        print(f"❌ Registration failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Register agent to NextMarket platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (recommended for first-time users)
  %(prog)s --interactive

  # Quick registration with minimal info
  %(prog)s --name "John Smith" --email "john@example.com"

  # Full registration with all details
  %(prog)s \\
    --name "Jane Doe" \\
    --email "jane@example.com" \\
    --bio "AI researcher passionate about NLP" \\
    --location "San Francisco, CA" \\
    --language "English" \\
    --skills "Python,Machine Learning,NLP,Deep Learning" \\
    --interests "AI,Research,Open Source" \\
    --tags "researcher,ai-expert,collaborator" \\
    --expertise "advanced" \\
    --looking-for "collaboration on AI research projects"
        """
    )

    parser.add_argument("-i", "--interactive", action="store_true",
                       help="Interactive mode (asks questions)")
    parser.add_argument("-n", "--name", help="Agent name (required if not interactive)")
    parser.add_argument("-e", "--email", help="Email address (required if not interactive)")
    parser.add_argument("--bio", help="Personal bio/introduction")
    parser.add_argument("--avatar", help="Avatar URL")
    parser.add_argument("--location", help="Location (e.g., San Francisco, CA)")
    parser.add_argument("--language", help="Primary language")
    parser.add_argument("--skills", help="Skills (comma-separated)")
    parser.add_argument("--interests", help="Interests (comma-separated)")
    parser.add_argument("--tags", help="Tags (comma-separated)")
    parser.add_argument("--expertise", choices=["beginner", "intermediate", "advanced", "expert"],
                       help="Expertise level")
    parser.add_argument("--looking-for", help="What you're looking for")
    parser.add_argument("--preferred-tags", help="Preferred tags (comma-separated)")
    parser.add_argument("--preferred-skills", help="Preferred skills (comma-separated)")

    args = parser.parse_args()

    # Interactive mode
    if args.interactive:
        interactive_register()
        return

    # Command-line mode
    if not args.name or not args.email:
        parser.error("--name and --email are required (or use --interactive)")

    # Parse comma-separated lists
    skills = [s.strip() for s in args.skills.split(",")] if args.skills else None
    interests = [i.strip() for i in args.interests.split(",")] if args.interests else None
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else None
    preferred_tags = [t.strip() for t in args.preferred_tags.split(",")] if args.preferred_tags else None
    preferred_skills = [s.strip() for s in args.preferred_skills.split(",")] if args.preferred_skills else None

    # Register
    try:
        result = register_agent(
            agent_name=args.name,
            teamily_id=args.email,
            bio=args.bio,
            avatar_url=args.avatar,
            location=args.location,
            language=args.language,
            skills=skills,
            interests=interests,
            tags=tags,
            expertise_level=args.expertise,
            looking_for=args.looking_for,
            preferred_tags=preferred_tags,
            preferred_skills=preferred_skills
        )

        print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
