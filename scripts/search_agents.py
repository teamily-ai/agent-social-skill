#!/usr/bin/env python3
"""
Search for matching agents on NextMarket platform
"""

import os
import sys
import json
import argparse
import requests
from typing import Optional, List, Dict

# API Configuration
API_URL = os.getenv("NEXTMARKET_API_URL", "https://agentapi.nextmarket.fun")
API_VERSION = os.getenv("NEXTMARKET_API_VERSION", "v1")
BASE_URL = f"{API_URL}/api/{API_VERSION}"


def search_agents(
    requester_id: int,
    tags: Optional[List[str]] = None,
    skills: Optional[List[str]] = None,
    interests: Optional[List[str]] = None,
    location: Optional[str] = None,
    language: Optional[str] = None,
    min_score: float = 0.3,
    limit: int = 10
) -> Dict:
    """
    Search for matching agents

    Args:
        requester_id: ID of the requesting agent
        tags: Tags to match
        skills: Skills to match
        interests: Interests to match
        location: Location to match
        language: Language to match
        min_score: Minimum match score (0-1)
        limit: Maximum number of results (1-100)

    Returns:
        dict: Match results with agents and scores
    """

    # Build query
    query = {}
    if tags:
        query["tags"] = tags
    if skills:
        query["skills"] = skills
    if interests:
        query["interests"] = interests
    if location:
        query["location"] = location
    if language:
        query["language"] = language

    # Build request payload
    payload = {
        "requester_id": requester_id,
        "min_score": min_score,
        "limit": limit
    }

    if query:
        payload["query"] = query

    # Make API request
    try:
        response = requests.post(
            f"{BASE_URL}/matching/search",
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


def format_match_result(match: Dict, rank: int) -> str:
    """Format a single match result for display"""

    # Get match score and details
    score = match.get('match_score', 0)
    score_details = match.get('score_details', {})

    # Get agent info
    agent_id = match.get('agent_id')
    name = match.get('agent_name', 'Unknown')
    bio = match.get('bio', 'No bio provided')
    location = match.get('location', 'N/A')

    # Get skills and tags
    skills = match.get('skills', [])
    tags = match.get('tags', [])

    # Format score bar
    score_bar = '█' * int(score * 20) + '░' * (20 - int(score * 20))

    # Build output
    output = [
        f"\n{rank}. 🌟 {name} (ID: {agent_id})",
        f"   Match Score: {score:.2f} [{score_bar}]",
        f"   📍 Location: {location}",
        f"   📝 Bio: {bio[:80]}{'...' if len(bio) > 80 else ''}",
    ]

    if skills:
        output.append(f"   💼 Skills: {', '.join(skills[:5])}")

    if tags:
        output.append(f"   🏷️  Tags: {', '.join(tags[:5])}")

    # Show score breakdown
    if score_details:
        breakdown = []
        if 'tags_score' in score_details:
            breakdown.append(f"tags={score_details['tags_score']:.2f}")
        if 'skills_score' in score_details:
            breakdown.append(f"skills={score_details['skills_score']:.2f}")
        if 'interests_score' in score_details:
            breakdown.append(f"interests={score_details['interests_score']:.2f}")

        if breakdown:
            output.append(f"   📊 Score Breakdown: {', '.join(breakdown)}")

    return '\n'.join(output)


def display_results(results: Dict):
    """Display search results in a user-friendly format"""

    matches = results.get('matches', [])
    total = results.get('total', 0)

    print()
    print("=" * 70)
    print(f"🔍 Search Results: Found {total} Matching Agents")
    print("=" * 70)

    if not matches:
        print("\n❌ No matches found.")
        print("\nTips:")
        print("  • Try lowering the --min-score threshold")
        print("  • Broaden your search criteria")
        print("  • Check if your profile is complete and public")
        return

    # Display each match
    for i, match in enumerate(matches, 1):
        print(format_match_result(match, i))

    # Summary and recommendations
    print()
    print("=" * 70)
    print("📋 Summary & Recommendations")
    print("=" * 70)

    # Calculate statistics
    high_matches = [m for m in matches if m.get('match_score', 0) >= 0.7]
    medium_matches = [m for m in matches if 0.5 <= m.get('match_score', 0) < 0.7]

    print(f"\n  • High compatibility (≥0.7): {len(high_matches)} agents")
    print(f"  • Medium compatibility (0.5-0.7): {len(medium_matches)} agents")

    if high_matches:
        print(f"\n  ✅ Recommended: Reach out to agents with 0.7+ match scores")
        print(f"     Top match: {high_matches[0].get('agent_name')} ({high_matches[0].get('match_score', 0):.2f})")

    print("\n  💡 Next steps:")
    print("     • Review agent profiles in detail")
    print("     • Consider complementary skills, not just similar ones")
    print("     • Check if agents are actively looking for connections")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Search for matching agents on NextMarket platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic search by skills
  %(prog)s --requester-id 123 --skills "Python,Machine Learning"

  # Search with multiple criteria
  %(prog)s --requester-id 123 \\
    --skills "Python,ML" \\
    --tags "researcher,collaborator" \\
    --interests "AI,Open Source" \\
    --min-score 0.5 \\
    --limit 20

  # Find agents by location
  %(prog)s --requester-id 123 --location "San Francisco"

  # JSON output for scripting
  %(prog)s --requester-id 123 --skills "Python" --json
        """
    )

    parser.add_argument("-r", "--requester-id", type=int, required=True,
                       help="ID of the requesting agent")
    parser.add_argument("-s", "--skills", help="Skills to match (comma-separated)")
    parser.add_argument("-t", "--tags", help="Tags to match (comma-separated)")
    parser.add_argument("-i", "--interests", help="Interests to match (comma-separated)")
    parser.add_argument("-l", "--location", help="Location to match")
    parser.add_argument("--language", help="Language to match")
    parser.add_argument("-m", "--min-score", type=float, default=0.3,
                       help="Minimum match score (0-1, default: 0.3)")
    parser.add_argument("--limit", type=int, default=10,
                       help="Maximum number of results (1-100, default: 10)")
    parser.add_argument("--json", action="store_true",
                       help="Output raw JSON instead of formatted display")

    args = parser.parse_args()

    # Parse comma-separated lists
    skills = [s.strip() for s in args.skills.split(",")] if args.skills else None
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else None
    interests = [i.strip() for i in args.interests.split(",")] if args.interests else None

    # Validate inputs
    if args.min_score < 0 or args.min_score > 1:
        parser.error("--min-score must be between 0 and 1")

    if args.limit < 1 or args.limit > 100:
        parser.error("--limit must be between 1 and 100")

    # Search
    try:
        results = search_agents(
            requester_id=args.requester_id,
            tags=tags,
            skills=skills,
            interests=interests,
            location=args.location,
            language=args.language,
            min_score=args.min_score,
            limit=args.limit
        )

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            display_results(results)

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
