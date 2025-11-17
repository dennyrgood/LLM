Claude session - started the whole rabbit trail of hosting my own llm



- was an offshoot of a conversation about automagically creating GIT commit messages for my sync shell scripts



**Is there a way of doing a "pre-scan" of the changes and make the commit message more descriptive of the changes automagically?**

Yes! Absolutely possible. You can analyze the staged changes and auto-generate a descriptive commit message. Here are several approaches:

Approach 1: Simple File-Based Summary
Auto-Generate Commit Messages from Changes
Approach 2: AI-Powered (Using Claude API)

For even smarter messages, you could use Claude to analyze the actual diff:
bash

generate_ai_commit_message() {
    local diff=$(git diff --staged)
    
    # Call Claude API to generate message
    local response=$(curl -s https://api.anthropic.com/v1/messages \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"claude-sonnet-4-20250514\",
            \"max_tokens\": 100,
            \"messages\": [{
                \"role\": \"user\",
                \"content\": \"Generate a concise git commit message (max 72 chars) for these changes. Respond with ONLY the commit message, no explanation:\n\n$diff\"
            }]
        }")
    
    # Parse response (would need jq or similar)
    echo "$response" | jq -r '.content[0].text'
}

Approach 3: Conventional Commits Style
bash

generate_conventional_commit() {
    local file_list=$(git diff --staged --name-only)
    
    # Determine type
    local type="chore"
    
    if echo "$file_list" | grep -qE '\.(js|py|rb|java|go)$'; then
        if git diff --staged | grep -q "^+.*function\|^+.*def\|^+.*class"; then
            type="feat"
        else
            type="fix"
        fi
    elif echo "$file_list" | grep -qE 'README|\.md$'; then
        type="docs"
    elif echo "$file_list" | grep -qE '\.(json|yaml|yml)$'; then
        type="config"
    fi
    
    # Get scope (directory or file type)
    local scope=$(echo "$file_list" | head -1 | xargs dirname | sed 's|^\.||')
    [ "$scope" = "/" ] && scope=""
    
    # Build message
    local msg="$type"
    [ -n "$scope" ] && msg="$msg($scope)"
    msg="$msg: update files"
    
    echo "$msg"
}
```

## What Would You Get?

### Simple Approach (Approach 1):
```
"Update scripts (1 file, +45/-12 lines) on branch: main"
"Add docs (3 files, +230/-0 lines) on branch: feature-auth"
"Modify code config (5 files, +67/-34 lines) on branch: main"
```

### AI Approach (Approach 2):
```
"Refactor authentication logic and update error handling"
"Add user profile validation with email verification"
"Fix race condition in async file processing"
```

### Conventional Commits (Approach 3):
```
"feat(auth): update files"
"docs: update files"
"fix(api): update files"

My Recommendation

Start with Approach 1 (the artifact I created). It's:

    Fast (no API calls)
    Descriptive enough for solo dev
    Shows you what changed at a glance
    Still lets you override if needed

The AI approach would be overkill for solo dev, and conventional commits are more useful for teams.
Integration Into Your sync-this.sh

Want me to integrate the auto-generation into your actual sync-this.sh script? I can make it show you the auto-generated message and still give you the option to override it.



**what "costs"/"Limits" are there for approach 2 - claude is only free to a certain extent**

Great question! Let me break down the costs and limits for using Claude API in your scripts.
Claude API Costs

You need a separate API account - the free claude.ai chat we're using now is different from API access.
API Pricing (as of my knowledge):

    Claude Sonnet 4: ~$3 per million input tokens, ~$15 per million output tokens
    Claude Haiku: Much cheaper, ~$0.25 per million input tokens, ~$1.25 per million output tokens

What Does This Mean for Commit Messages?

Per commit message generation:

    Input: ~500-2000 tokens (your git diff)
    Output: ~20-50 tokens (the commit message)
    Cost per message: ~$0.001-0.005 (fraction of a penny)

Realistic usage:

    100 commits/month = ~$0.10-0.50
    1000 commits/month = ~$1-5

So it's very cheap, but not free.
Free Tier & Limits

Unfortunately, there is no perpetual free tier for the API like there is for claude.ai chat. You get:

    $5 free credits when you first sign up
    Then you pay per use
    Rate limits even on paid tiers:
        Tier 1: 50 requests/minute, 40K tokens/minute
        More than enough for your use case

Alternatives to Paid API
Option 1: Use Locally-Run LLMs (FREE)
bash




**HERE IT IS**



# Using Ollama (free, runs locally)
generate_commit_message() {
    local diff=$(git diff --staged)
    
    curl -s http://localhost:11434/api/generate -d "{
        \"model\": \"llama3.2\",
        \"prompt\": \"Generate a concise commit message: $diff\",
        \"stream\": false
    }" | jq -r '.response'
}

Pros:

    Completely free
    No API limits
    Privacy (data never leaves your machine)

Cons:

    Need to install Ollama
    Quality not as good as Claude
    Slower (but still <5 seconds)

Option 2: Use GitHub Copilot CLI (if you have it)
bash

# If you have Copilot subscription ($10/month)
gh copilot suggest "git commit message for these changes"

Option 3: OpenAI API (also paid, but cheaper)
bash

# GPT-4o-mini is very cheap (~$0.15/$0.60 per million tokens)
# Similar cost to Claude Haiku

Option 4: Use Anthropic's Prompt Caching (CHEAPEST)

If you do use Claude API, enable prompt caching:
bash

# First request: normal cost
# Subsequent requests within 5 min: 90% discount on input tokens

For your use case (multiple commits in short time), this could make it nearly free!
My Honest Recommendation

For solo dev work, Approach 2 (AI) is overkill.

Here's why:

    Approach 1 is free and good enough
    You'd spend more time managing API keys than you'd save
    Solo dev = no one cares about perfect commit messages
    The $5 free credits would last months, but then you're paying forever

However, if you:

    Already have Claude API access for other projects
    Want to experiment with it
    Commit 100+ times/day and need good messages

Then go for it! The cost is negligible.
What I'd Actually Do

Hybrid approach:
bash

# Use simple auto-generation by default (free)
AUTO_MESSAGE=$(generate_commit_message "$CURRENT_BRANCH")

# But add a flag for AI mode when you want it
if [ "$USE_AI" = true ]; then
    AUTO_MESSAGE=$(generate_ai_commit_message)
fi

Then use AI mode only when you really care (like before pushing to a public repo).

Want me to show you how to set up the free Ollama option instead? It's pretty cool and you own it forever!




**yes, I want you to help me setup ollama, what else can i use it for? I would be installing it on my win11 machine, would i be able to access from my workhorse macos machine**

Excellent! Ollama is a great tool. Let me explain the setup and what you can do with it.
What is Ollama?

Think of it as "Docker for AI models" - it lets you run LLMs (like Llama, Mistral, etc.) locally on your machine. No API keys, no costs, complete privacy.
Setup Plan: Windows 11 + macOS Access
Option 1: Install on macOS (RECOMMENDED)

Since macOS is your workhorse, install it there directly:

    Better performance on Mac (especially M1/M2/M3)
    No network lag
    Simpler setup

Option 2: Install on Windows + Network Access

Install on Windows, expose it to network so macOS can access it:

    Uses Windows GPU (if you have one)
    Requires network configuration
    More complex

I recommend Option 1 unless your Windows machine has a powerful GPU and your Mac doesn't.
Installation Guide
On macOS (Recommended):

    Download & Install:

bash

# Visit https://ollama.ai/download
# Or use Homebrew:
brew install ollama

    Start Ollama:

bash

ollama serve

This runs in the background (you can close terminal after).

    Download a Model:

bash

# Small, fast model (1.3GB) - good for commit messages
ollama pull llama3.2:1b

# Medium quality (4.7GB) - better quality
ollama pull llama3.2:3b

# High quality (4.7GB) - GPT-3.5 level
ollama pull mistral

# Best quality (8GB+) - GPT-4 level
ollama pull llama3.1:8b

    Test It:

bash

ollama run llama3.2:1b
>>> Write a haiku about coding
>>> /bye

On Windows 11:

    Download: https://ollama.ai/download
        Download the Windows installer
        Run it (installs as a service)
    Expose to Network (so macOS can access):

bash

# Set environment variable (PowerShell as Admin):
[System.Environment]::SetEnvironmentVariable('OLLAMA_HOST', '0.0.0.0:11434', 'Machine')

# Restart Ollama service:
Restart-Service Ollama

    Allow Firewall:
        Windows Defender Firewall → Allow an app
        Add Ollama (port 11434)
    Find Windows IP:

bash

ipconfig
# Look for IPv4 Address (e.g., 192.168.1.100)

    Test from macOS:

bash

# From your Mac:
curl http://192.168.1.100:11434/api/tags

What Can You Use Ollama For?
1. Commit Message Generation (what we discussed)
bash

curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Write a concise git commit message for: Added user authentication, fixed login bug",
  "stream": false
}'

2. Code Explanation
bash

# Explain complex code
cat complex_function.js | ollama run llama3.2 "Explain this code"

3. Documentation Generation
bash

# Generate README sections
ollama run mistral "Write a README section for a bash script that syncs git repos"

4. Code Review
bash

# Review your changes
git diff | ollama run llama3.2 "Review this code for bugs and improvements"

5. Shell Command Help
bash

# Ask about commands
ollama run llama3.2 "How do I find all files modified in last 7 days?"

6. Debugging Assistant
bash

# Paste error messages
ollama run mistral "Why am I getting: bash: syntax error near unexpected token"

7. Refactoring Suggestions
bash

cat messy_script.sh | ollama run llama3.2 "Suggest improvements for this script"

8. CLI Tool Integration

You can pipe anything into it:
bash

# Summarize logs
tail -100 app.log | ollama run llama3.2 "Summarize these logs"

# Explain command output
ps aux | ollama run llama3.2 "What processes are using most memory?"

9. Interactive Shell Helper
bash

# Add to .zshrc or .bashrc:
ask() {
    ollama run llama3.2:1b "$*"
}

# Then use:
ask "how to compress a directory with tar"

10. Custom Scripts

Build tools that use AI:

    Auto-generate test cases
    Convert between formats
    Summarize meeting notes
    Generate boilerplate code

Integration with Your Sync Scripts
Ollama-Powered Commit Message Generator
Code 
How to Use
1. Default Mode (Simple, Free):
bash

./smart-commit.sh
# Uses the simple file-based generation

2. AI Mode (Ollama):
bash

USE_AI=true ./smart-commit.sh
# Uses Ollama if available, falls back to simple

3. Make it Permanent:

Edit the script to change:
bash

USE_AI="${USE_AI:-true}"  # AI on by default

4. Use Remote Ollama (Windows):
bash

OLLAMA_HOST="http://192.168.1.100:11434" USE_AI=true ./smart-commit.sh

5. Different Model:
bash

OLLAMA_MODEL="mistral" USE_AI=true ./smart-commit.sh

Performance Expectations

Model	Size	Speed	Quality
llama3.2:1b	1.3GB	~1-2s	Good enough
llama3.2:3b	2GB	~2-4s	Better
mistral	4.7GB	~3-5s	Great
llama3.1:8b	8GB	~5-10s	Excellent

For commit messages, llama3.2:1b is perfect - fast and good enough.
Next Steps

    Install Ollama on your Mac (easiest)
    Pull the 1b model: ollama pull llama3.2:1b
    Try the script with USE_AI=true
    If you like it, integrate into your sync scripts

Want me to show you how to integrate this into your existing sync-this.sh and sync-all.sh scripts?



**can i point my vs to a win11 hosted llama**

Yes! You can absolutely point VS Code on macOS to Ollama running on your Windows 11 machine. Here's how:
VS Code Extensions That Support Ollama
1. Continue (Most Popular)

Best AI coding assistant that works with Ollama.

Installation:

    Open VS Code
    Extensions → Search "Continue"
    Install "Continue - Codestral, Claude, and more"

Configuration:

    After install, click Continue icon in sidebar
    Click gear icon → config.json opens
    Edit configuration:

json

{
  "models": [
    {
      "title": "Llama on Windows",
      "provider": "ollama",
      "model": "llama3.2:3b",
      "apiBase": "http://192.168.1.100:11434"  // Your Windows IP
    }
  ],
  "tabAutocompleteModel": {
    "title": "Fast Autocomplete",
    "provider": "ollama",
    "model": "llama3.2:1b",
    "apiBase": "http://192.168.1.100:11434"
  }
}

Features:

    Autocomplete (like Copilot)
    Chat with your code
    Explain code
    Generate tests
    Refactor code
    Ask questions about codebase

2. Cline (formerly Claude Dev)

AI coding agent that can edit files, run commands, etc.
json

// Settings → Cline → API Configuration
{
  "ollama": {
    "baseUrl": "http://192.168.1.100:11434",
    "model": "llama3.2:3b"
  }
}

3. Twinny

Lightweight, Copilot-like autocomplete.
json

// Settings → Twinny
{
  "twinny.ollamaApiUrl": "http://192.168.1.100:11434",
  "twinny.ollamaModel": "llama3.2:1b"
}

Network Setup Checklist

Since you're connecting Mac → Windows, ensure:
On Windows 11:

    Set Ollama to listen on all interfaces:

powershell

# PowerShell as Administrator:
[System.Environment]::SetEnvironmentVariable('OLLAMA_HOST', '0.0.0.0:11434', 'Machine')

# Restart Ollama:
Restart-Service Ollama

    Allow through firewall:

powershell

# PowerShell as Administrator:
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 11434

    Find your Windows IP:

powershell

ipconfig
# Look for IPv4 Address on your main network adapter
# Example: 192.168.1.100

On macOS:

    Test connection:

bash

curl http://192.168.1.100:11434/api/tags

    Should return something like:

json

{
  "models": [
    {
      "name": "llama3.2:1b",
      "modified_at": "2024-01-15T..."
    }
  ]
}

Recommended Setup for You

Since you're doing development on Mac but have GPU on Windows, here's my recommendation:
Best Configuration:

For Autocomplete (needs speed):

    Use small, fast model on Windows (llama3.2:1b)
    Acceptable 100-200ms latency over network

For Chat/Explanations (quality matters):

    Use better model on Windows (mistral or llama3.1:8b)
    Latency doesn't matter for chat

Continue Config Example:
json

{
  "models": [
    {
      "title": "Llama Chat (Windows)",
      "provider": "ollama",
      "model": "mistral",
      "apiBase": "http://192.168.1.100:11434"
    },
    {
      "title": "Llama Fast (Windows)", 
      "provider": "ollama",
      "model": "llama3.2:1b",
      "apiBase": "http://192.168.1.100:11434"
    }
  ],
  "tabAutocompleteModel": {
    "title": "Autocomplete",
    "provider": "ollama", 
    "model": "llama3.2:1b",
    "apiBase": "http://192.168.1.100:11434"
  }
}

Performance Considerations

Network Latency:

    Local Mac Ollama: 50-100ms
    Mac → Windows (same network): 150-300ms
    Mac → Windows (WiFi): 200-500ms

For autocomplete, this means:

    Local: Nearly instant
    Remote: Slight delay (still usable)

My recommendation: If your Windows machine has a good GPU (NVIDIA), use it. If not, just install Ollama on your Mac - easier and faster.
What's Your Windows Setup?

Do you have:

    NVIDIA GPU? (Ollama will use it automatically)
    AMD GPU? (Limited support, CPU might be faster)
    No dedicated GPU? (Use Mac instead)

Let me know and I can give you more specific advice on whether Windows hosting makes sense for your setup!

Also, want me to show you what Continue can do once you have it set up? It's pretty amazing for coding.



**I really like the github copilot cli, but it is very expensive, is there anything like that available?
**

Yes! There are several free alternatives to GitHub Copilot CLI that work with Ollama. Let me show you the best options:
1. aichat (My Top Recommendation)

This is the closest to GitHub Copilot CLI - simple, fast, shell-focused.
Installation:
bash

# macOS
brew install aichat

# Or download from: https://github.com/sigoden/aichat

Setup with Ollama:
bash

# First run creates config
aichat

# Edit config file
vim ~/.config/aichat/config.yaml

Config for Ollama:
yaml

model: ollama:llama3.2:3b
clients:
  - type: ollama
    api_base: http://localhost:11434  # Or your Windows IP
    models:
      - name: llama3.2:1b
      - name: llama3.2:3b
      - name: mistral

Usage (Just Like Copilot CLI):
bash

# Ask questions
aichat "how to find files modified in last 7 days"

# Generate commands
aichat "git command to undo last commit"

# Explain commands
aichat "explain: find . -name '*.log' -mtime +30 -delete"

# Interactive mode
aichat
>>> how do I compress a folder with tar?

# Execute suggested commands directly
aichat -e "create a backup of my home directory"

# Pipe input
cat error.log | aichat "explain this error"

Shell Integration:
bash

# Add to ~/.zshrc or ~/.bashrc:
alias ai='aichat'
alias '??'='aichat'

# Then use:
?? how to kill process on port 8080
ai "convert mp4 to gif"

2. llm (by Simon Willison)

Simpler, Python-based CLI tool.
Installation:
bash

pip install llm

# Install Ollama plugin
llm install llm-ollama

Usage:
bash

# Ask questions
llm "how to recursively delete empty directories"

# Use specific model
llm -m llama3.2 "explain git rebase"

# Save conversations
llm "help me debug bash script" --save debugging

# Continue conversation
llm "what about error handling?" --continue debugging

# Templates
llm "explain this code" < script.sh

3. Shell-GPT (sgpt)

Another popular alternative.
Installation:
bash

pip install shell-gpt

# Configure for Ollama
sgpt --model ollama/llama3.2

Usage:
bash

# Generate commands
sgpt "mass rename files to lowercase"

# Execute directly with --shell
sgpt --shell "find all large files"

# Code generation
sgpt --code "python script to rename files"

# Chat mode
sgpt --chat debugging "help debug this error"

4. fabric (For Specific Tasks)

Great for specific patterns like summarizing, extracting, etc.
Installation:
bash

# macOS
brew install fabric

# Setup
fabric --setup

Usage:
bash

# Summarize content
cat article.txt | fabric --pattern summarize

# Extract action items
cat meeting_notes.md | fabric --pattern extract_wisdom

# Analyze code
cat script.sh | fabric --pattern review_code

# Create custom patterns
fabric --pattern your_custom_pattern

Comparison Table

Tool	Best For	Ease of Use	Features
aichat	General CLI use, most like Copilot	⭐⭐⭐⭐⭐	Chat, execute, roles, sessions
llm	Python users, quick queries	⭐⭐⭐⭐	Simple, extensible, logging
Shell-GPT	Command generation	⭐⭐⭐⭐	Shell mode, code mode
fabric	Specific patterns/tasks	⭐⭐⭐	Pre-built patterns, structured

My Recommendation: aichat + aliases

Here's a powerful setup:
bash

# Add to ~/.zshrc or ~/.bashrc:

# Quick AI query
alias ai='aichat'

# Command suggestions (like gh copilot suggest)
suggest() {
    aichat -e "$*"
}

# Explain commands (like gh copilot explain)
explain() {
    aichat "Explain this command: $*"
}

# Quick question
alias '??'='aichat'

# Git commit message helper
alias gitmsg='git diff --staged | aichat "Generate a concise git commit message for these changes. Reply with only the message:"'

# Debug helper
debug() {
    echo "$*" | aichat "Help debug this error:"
}

Usage Examples:
bash

# Quick questions
?? how to find processes using port 8080

# Command suggestions (interactive)
suggest backup my database to s3

# Explain complex commands
explain "find . -type f -exec sed -i 's/foo/bar/g' {} +"

# Git commit message
git add -A
gitmsg
# Returns: "Add user authentication and fix login validation bug"

# Debug errors
debug "bash: syntax error near unexpected token"

Advanced: Create Your Own "Copilot CLI"
copilot - Free CLI Alternative Using Ollama
Code 
How to Use Your Custom Copilot

    Save the script:

bash

# Save as ~/bin/copilot (or anywhere in your PATH)
chmod +x ~/bin/copilot

    Make sure Ollama is running:

bash

ollama serve

    Use it just like GitHub Copilot CLI:

bash

# Suggest commands
copilot suggest find all large files over 100MB

# Explain commands
copilot explain "find . -type f -exec grep -l 'TODO' {} +"

# Ask questions
copilot ask how do I monitor system resources

# Generate commit messages
git add -A
copilot commit

# Debug errors
copilot debug "zsh: command not found: python"

Cost Comparison

Tool	Cost	Speed	Quality
GitHub Copilot CLI	$10-20/mo	Fast	Excellent
aichat + Ollama	FREE	Fast	Very Good
Custom copilot script	FREE	Fast	Very Good

Best Setup for You
bash

# Install aichat for daily use
brew install aichat

# Configure for Ollama
aichat

# Add helpful aliases to ~/.zshrc:
alias ai='aichat'
alias '??'='aichat'
alias explain='copilot explain'
alias suggest='copilot suggest'

# Use Windows Ollama (if that's where you install it)
export OLLAMA_HOST="http://192.168.1.100:11434"

Then you get:

    ?? for quick questions (fastest)
    ai for chat mode
    suggest for command generation
    explain for command explanations
    copilot commit for commit messages

Totally free, works offline, no rate limits! 🎉

Which one do you want to try first?





**SCRIPT (In separate file as well)**


#!/bin/bash

# copilot - Free GitHub Copilot CLI Alternative using Ollama
# Usage: 
#   copilot suggest "find large files"
#   copilot explain "git rebase -i HEAD~3"
#   copilot ask "how to use rsync"

OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"
OLLAMA_MODEL="${OLLAMA_MODEL:-llama3.2:3b}"

# Colors for output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if Ollama is available
check_ollama() {
    if ! curl -s "$OLLAMA_HOST/api/tags" > /dev/null 2>&1; then
        echo "❌ Error: Cannot connect to Ollama at $OLLAMA_HOST"
        echo "   Make sure Ollama is running: ollama serve"
        exit 1
    fi
}

# Function to call Ollama
call_ollama() {
    local prompt="$1"
    local system="${2:-You are a helpful command-line assistant.}"
    
    local response=$(curl -s "$OLLAMA_HOST/api/generate" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"$OLLAMA_MODEL\",
            \"prompt\": \"$system\n\n$prompt\",
            \"stream\": false,
            \"options\": {
                \"temperature\": 0.7
            }
        }")
    
    echo "$response" | jq -r '.response'
}

# Command: suggest
cmd_suggest() {
    local query="$*"
    
    if [ -z "$query" ]; then
        echo "Usage: copilot suggest <description>"
        echo "Example: copilot suggest find all log files older than 30 days"
        exit 1
    fi
    
    echo -e "${BLUE}🤖 Suggesting command for:${NC} $query"
    echo ""
    
    local system="You are a command-line expert. Generate a single, executable shell command for the user's request. Reply with ONLY the command, no explanation, no markdown, no quotes."
    local prompt="Generate a shell command for: $query"
    
    local command=$(call_ollama "$prompt" "$system")
    
    # Clean up the response
    command=$(echo "$command" | sed 's/^```.*//g' | sed 's/```$//g' | sed 's/^`//g' | sed 's/`$//g' | xargs)
    
    echo -e "${GREEN}Suggested command:${NC}"
    echo "  $command"
    echo ""
    
    # Ask if user wants to execute
    read -p "Execute this command? (y/N): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Executing...${NC}"
        eval "$command"
    else
        echo "Command not executed."
    fi
}

# Command: explain
cmd_explain() {
    local command="$*"
    
    if [ -z "$command" ]; then
        echo "Usage: copilot explain <command>"
        echo "Example: copilot explain 'find . -name \"*.log\" -mtime +30 -delete'"
        exit 1
    fi
    
    echo -e "${BLUE}🤖 Explaining command:${NC} $command"
    echo ""
    
    local system="You are a command-line expert. Explain shell commands clearly and concisely. Break down each part of the command."
    local prompt="Explain this shell command in detail:\n\n$command"
    
    local explanation=$(call_ollama "$prompt" "$system")
    
    echo -e "${GREEN}Explanation:${NC}"
    echo "$explanation"
}

# Command: ask
cmd_ask() {
    local question="$*"
    
    if [ -z "$question" ]; then
        echo "Usage: copilot ask <question>"
        echo "Example: copilot ask how do I compress a directory"
        exit 1
    fi
    
    echo -e "${BLUE}🤖 Question:${NC} $question"
    echo ""
    
    local system="You are a helpful command-line assistant. Provide practical, actionable answers. Include example commands when relevant."
    local prompt="$question"
    
    local answer=$(call_ollama "$prompt" "$system")
    
    echo -e "${GREEN}Answer:${NC}"
    echo "$answer"
}

# Command: commit
cmd_commit() {
    echo -e "${BLUE}🤖 Generating commit message...${NC}"
    echo ""
    
    # Get staged changes
    if git diff --staged --quiet; then
        echo "❌ No staged changes. Stage changes first with: git add"
        exit 1
    fi
    
    local diff=$(git diff --staged | head -c 2000)  # Limit size
    
    local system="You are a git commit message expert. Generate concise, conventional commit messages."
    local prompt="Generate a git commit message for these changes. Reply with ONLY the commit message (max 72 chars), no explanation:\n\n$diff"
    
    local message=$(call_ollama "$prompt" "$system" | head -1 | xargs)
    
    echo -e "${GREEN}Suggested commit message:${NC}"
    echo "  $message"
    echo ""
    
    read -p "Use this message? (y/N): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git commit -m "$message"
        echo "✓ Committed"
    else
        echo "Commit cancelled. Write your own:"
        git commit
    fi
}

# Command: debug
cmd_debug() {
    local error="$*"
    
    if [ -z "$error" ]; then
        echo "Usage: copilot debug <error message>"
        echo "Example: copilot debug 'bash: command not found: npm'"
        exit 1
    fi
    
    echo -e "${BLUE}🤖 Debugging error:${NC} $error"
    echo ""
    
    local system="You are a debugging expert. Explain errors and provide solutions. Be concise and actionable."
    local prompt="Help me debug this error:\n\n$error"
    
    local solution=$(call_ollama "$prompt" "$system")
    
    echo -e "${GREEN}Solution:${NC}"
    echo "$solution"
}

# Main command router
main() {
    check_ollama
    
    local subcommand="$1"
    shift
    
    case "$subcommand" in
        suggest|s)
            cmd_suggest "$@"
            ;;
        explain|e)
            cmd_explain "$@"
            ;;
        ask|a)
            cmd_ask "$@"
            ;;
        commit|c)
            cmd_commit "$@"
            ;;
        debug|d)
            cmd_debug "$@"
            ;;
        *)
            echo "copilot - Free GitHub Copilot CLI Alternative"
            echo ""
            echo "Usage: copilot <command> [arguments]"
            echo ""
            echo "Commands:"
            echo "  suggest (s)  Generate a shell command from description"
            echo "  explain (e)  Explain what a command does"
            echo "  ask (a)      Ask a general question"
            echo "  commit (c)   Generate a git commit message"
            echo "  debug (d)    Help debug an error message"
            echo ""
            echo "Examples:"
            echo "  copilot suggest find all PDF files"
            echo "  copilot explain 'tar -xzf archive.tar.gz'"
            echo "  copilot ask how to use rsync"
            echo "  copilot commit"
            echo "  copilot debug 'permission denied'"
            echo ""
            echo "Environment:"
            echo "  OLLAMA_HOST=$OLLAMA_HOST"
            echo "  OLLAMA_MODEL=$OLLAMA_MODEL"
            exit 1
            ;;
    esac
}

main "$@"

