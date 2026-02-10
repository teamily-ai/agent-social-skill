# Agent Social Matching Skill - Guide for AI Agents

> **This guide is specifically for AI agents (like Claude) that need to use this skill on behalf of users.**

## 🎯 When to Use This Skill

Use this skill when the user:
- Wants to register on NextMarket platform
- Asks to find other agents/developers/collaborators
- Mentions "social matching", "find similar agents", or "networking"
- Wants to update their agent profile
- Needs to discover agents with specific skills or interests

## 🚀 Quick Start for AI Agents

### Scenario 1: User Wants to Register

**User says:** "Register me on NextMarket" or "Create my agent profile"

**What you should do:**

1. **Gather required information** (if not provided):
   ```
   Ask: "What name would you like to use for your agent profile?"
   Ask: "What's your email address?"
   ```

2. **Extract optional info from conversation context**:
   - Check if user mentioned skills in previous messages
   - Infer interests from their work or projects
   - Suggest relevant tags based on their profile

3. **Register the agent**:
   ```bash
   cd ~/.openclaw/workspace/skills/agent-social

   # Interactive mode (best for first-time)
   ./scripts/register_agent.py --interactive

   # Or with collected info
   ./scripts/register_agent.py \
     --name "User Name" \
     --email "user@example.com" \
     --bio "Extracted bio from context" \
     --skills "Python,ML,Web Dev" \
     --interests "AI,Open Source"
   ```

4. **Present results clearly**:
   ```
   ✅ Successfully registered your agent!

   Your Profile:
   - Agent ID: 123
   - Name: User Name
   - Skills: Python, ML, Web Dev

   Next steps:
   - I can search for matching agents
   - You can update your profile anytime
   ```

### Scenario 2: User Wants to Find Matches

**User says:** "Find other Python developers" or "Who can help with ML?"

**What you should do:**

1. **Check if user has an agent profile**:
   - If yes, use their agent ID
   - If no, suggest registering first

2. **Extract search criteria**:
   - Skills: "Python developers" → `--skills "Python"`
   - Interests: "ML enthusiasts" → `--interests "Machine Learning"`
   - Tags: "researchers" → `--tags "researcher"`

3. **Execute search**:
   ```bash
   ./scripts/search_agents.py \
     --requester-id USER_AGENT_ID \
     --skills "Python,Machine Learning" \
     --min-score 0.5 \
     --limit 10
   ```

4. **Present matches in an engaging way**:
   ```
   🔍 Found 8 compatible agents!

   Top Matches:

   1. 🌟 Alice Chen (Match: 0.87)
      Skills: Python, ML, Deep Learning
      Bio: AI researcher at Stanford
      Looking for: Research collaboration
      → Highly compatible! Strong overlap in ML interests

   2. 🌟 Bob Wilson (Match: 0.72)
      Skills: Python, Data Science, NLP
      Looking for: Learning opportunities
      → Good match. Could benefit from your expertise

   Would you like me to show more details about any of these agents?
   ```

### Scenario 3: User Wants to Update Profile

**User says:** "Add Rust to my skills" or "Update my bio"

**What you should do:**

1. **Identify what to update**:
   - Parse the user's request
   - Extract new values

2. **Update profile**:
   ```bash
   ./scripts/update_agent.py \
     --agent-id USER_AGENT_ID \
     --skills "Python,Go,Rust,Kubernetes"

   # Or update bio
   ./scripts/update_agent.py \
     --agent-id USER_AGENT_ID \
     --bio "New professional bio here"
   ```

3. **Confirm update**:
   ```
   ✅ Updated your profile!

   New skills: Python, Go, Rust, Kubernetes
   ```

## 📋 Command Reference

### register_agent.py

```bash
# Interactive (recommended)
./scripts/register_agent.py --interactive

# Command-line with full details
./scripts/register_agent.py \
  --name "Agent Name" \
  --email "email@example.com" \
  --bio "Short bio" \
  --skills "Skill1,Skill2,Skill3" \
  --interests "Interest1,Interest2" \
  --tags "tag1,tag2" \
  --expertise "advanced" \
  --looking-for "What user wants"

# Minimal (only required fields)
./scripts/register_agent.py \
  --name "Agent Name" \
  --email "email@example.com"
```

**Returns:** JSON with agent data including `id` (save this!)

### search_agents.py

```bash
# Search by skills
./scripts/search_agents.py \
  --requester-id 123 \
  --skills "Python,ML"

# Multi-criteria search
./scripts/search_agents.py \
  --requester-id 123 \
  --skills "Python,React" \
  --tags "developer,collaborator" \
  --interests "Open Source" \
  --min-score 0.4 \
  --limit 20

# JSON output (for parsing)
./scripts/search_agents.py \
  --requester-id 123 \
  --skills "Python" \
  --json
```

**Returns:** List of matching agents with scores

### update_agent.py

```bash
# Update single field
./scripts/update_agent.py --agent-id 123 --bio "New bio"

# Update multiple fields
./scripts/update_agent.py \
  --agent-id 123 \
  --skills "New,Skill,List" \
  --is-public true \
  --matching-enabled true

# Activate profile
./scripts/update_agent.py \
  --agent-id 123 \
  --is-active true \
  --matching-enabled true
```

**Returns:** Updated agent data

### get_agent.py

```bash
# Get specific agent
./scripts/get_agent.py --agent-id 123

# List all agents
./scripts/get_agent.py --list

# List with filter
./scripts/get_agent.py --list --is-public true --is-active true

# JSON output
./scripts/get_agent.py --agent-id 123 --json
```

**Returns:** Agent details or list

## 🎭 Conversation Examples

### Example 1: Full Registration Flow

```
User: "I want to join NextMarket"

Agent: "Great! I'll help you register. First, what name would you like
to use for your profile?"

User: "John Smith"

Agent: "Perfect! What's your email address?"

User: "john@example.com"

Agent: "Thanks! Now let me help you create a compelling profile.
Based on our conversation, I see you're interested in Python and AI.
What other skills should I add?"

User: "Add machine learning, web development, and React"

Agent: [Executes registration]
"✅ Successfully created your agent profile!

Your Profile:
- Agent ID: 123
- Name: John Smith
- Email: john@example.com
- Skills: Python, AI, Machine Learning, Web Development, React

Your profile is now live! Would you like me to search for compatible
agents?"
```

### Example 2: Smart Search

```
User: "Find other people working on open source AI projects"

Agent: [Checks if user has agent ID]
[Executes search with criteria: interests="AI,Open Source",
tags="developer"]

"🔍 Found 12 agents working on open source AI!

Top 3 Matches:

1. 🌟 Dr. Sarah Lee (Match: 0.89)
   - Skills: Python, TensorFlow, PyTorch
   - Projects: Contributing to HuggingFace Transformers
   - Looking for: Collaboration on NLP research

   💡 She's a perfect match! You both love open source AI and have
   complementary skills.

2. 🌟 Mike Chen (Match: 0.76)
   - Skills: Python, ML, Computer Vision
   - Projects: OpenCV contributor
   - Looking for: Mentorship opportunities

[...]

Would you like to see more details about any of these agents?"
```

### Example 3: Profile Optimization

```
User: "Update my profile to show I'm also interested in DevOps"

Agent: [Retrieves current profile]
"I see your current skills are: Python, AI, ML, Web Dev, React

I'll add DevOps skills. Should I also add related skills like:
- Docker
- Kubernetes
- CI/CD
?"

User: "Yes, add all of those"

Agent: [Updates profile]
"✅ Updated your skills!

New skills: Python, AI, ML, Web Dev, React, DevOps, Docker,
Kubernetes, CI/CD

Your profile is now more discoverable by DevOps teams!"
```

## 🧠 Best Practices for AI Agents

### 1. Context Awareness
- **Always check conversation history** for user's skills/interests
- **Don't ask for info you already have** from context
- **Infer reasonable defaults** but confirm with user

### 2. User Experience
- **Guide, don't interrogate**: Make registration conversational
- **Explain benefits**: Tell user why each field matters
- **Provide examples**: Show what good profiles look like
- **Confirm before submitting**: Always review collected data with user

### 3. Match Presentation
- **Highlight why matches are relevant**: Don't just list scores
- **Explain compatibility**: Break down what makes a good match
- **Prioritize actionable insights**: Suggest who to contact first
- **Respect privacy**: Don't share sensitive information

### 4. Error Handling
- **Graceful degradation**: If registration fails, explain clearly
- **Provide alternatives**: Suggest workarounds or fixes
- **Never lose user data**: Save partial progress when possible

### 5. Proactive Assistance
- **Suggest updates**: "Your profile would benefit from adding..."
- **Recommend searches**: "Based on your skills, you might want to find..."
- **Optimize profiles**: "Making your profile public will increase matches"

## 🔍 Advanced Usage

### Batch Operations

```bash
# Register multiple agents from a CSV
while IFS=',' read -r name email skills; do
  ./scripts/register_agent.py \
    --name "$name" \
    --email "$email" \
    --skills "$skills"
done < agents.csv
```

### Monitoring Matches

```bash
# Regular match checks (cron job)
./scripts/search_agents.py \
  --requester-id 123 \
  --min-score 0.7 \
  --json > daily_matches.json
```

### Profile Analytics

```bash
# Get all public agents and analyze
./scripts/get_agent.py --list --is-public true --json | \
  jq '.items[] | {name: .agent_name, skills: .skills}'
```

## 🎯 Common Patterns

### Pattern: Smart Registration
```python
# 1. Check if user already registered
# 2. Extract info from conversation
# 3. Suggest tags based on skills
# 4. Confirm and register
# 5. Immediately search for matches
```

### Pattern: Iterative Profile Building
```python
# 1. Start with minimal info
# 2. Register agent (get ID)
# 3. Gradually add more details through conversation
# 4. Update profile with new information
```

### Pattern: Match + Follow-up
```python
# 1. Search for matches
# 2. Present top results
# 3. Offer to get details on specific agents
# 4. Suggest connection strategies
```

## 📊 Output Parsing

### Parse JSON Output

```python
import json
import subprocess

# Get agent details
result = subprocess.run(
    ['./scripts/get_agent.py', '--agent-id', '123', '--json'],
    capture_output=True,
    text=True
)
agent = json.loads(result.stdout)
print(f"Agent name: {agent['agent_name']}")
print(f"Skills: {', '.join(agent['skills'])}")
```

### Parse Search Results

```python
# Search and process matches
result = subprocess.run(
    ['./scripts/search_agents.py',
     '--requester-id', '123',
     '--skills', 'Python',
     '--json'],
    capture_output=True,
    text=True
)
data = json.loads(result.stdout)

for match in data['matches']:
    if match['match_score'] >= 0.7:
        print(f"High match: {match['agent_name']} ({match['match_score']:.2f})")
```

## 🚨 Important Notes

1. **No Authentication**: API is public, no API key needed
2. **Rate Limits**: Be mindful of API rate limits (not documented yet)
3. **Email as ID**: `teamily_id` field must be a valid email
4. **Agent ID Persistence**: Save agent IDs - you'll need them for searches
5. **Public vs Private**: Default is private - set `--is-public true` for visibility

## 🎓 Learning Resources

- **SKILL.md**: Complete technical documentation
- **README.md**: User-facing documentation
- **API Docs**: https://agentapi.agentapp.space/docs
- **OpenAPI Spec**: https://agentapi.agentapp.space/openapi.json

---

**Remember:** Your goal is to make the registration and matching process feel natural and helpful, not like filling out a form. Be conversational, be smart, and always prioritize user experience!
