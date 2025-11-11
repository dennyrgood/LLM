#!/usr/bin/env python3
"""
Compare ollama_llm_fetcher output with aichat config and output missing models.
Usage: python3 model_differ.py [fetcher_output.txt]
       ./ollama_llm_fetcher.py | python3 model_differ.py
"""

import sys
import re
from pathlib import Path

def parse_fetcher_output(text):
    """Extract model IDs from fetcher output."""
    models = set()
    pattern = r'^([a-z0-9\-_.]+:[a-z0-9\-_.]+)\s+\|'
    
    for line in text.split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            models.add(match.group(1))
    
    return models

def parse_config_models(config_path):
    """Extract model names from aichat config."""
    models = set()
    
    try:
        with open(config_path, 'r') as f:
            content = f.read()
        
        pattern = r'^\s*-?\s*name:\s*["\']?([a-z0-9\-_.]+:[a-z0-9\-_.]+)["\']?'
        
        for line in content.split('\n'):
            match = re.match(pattern, line)
            if match:
                models.add(match.group(1))
    
    except FileNotFoundError:
        print(f"Error: Config file not found at {config_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading config: {e}", file=sys.stderr)
        sys.exit(1)
    
    return models

def format_display_name(model_id):
    """Create a readable display name from model ID."""
    base_name = model_id.replace(':latest', '').replace(':cloud', '')
    parts = [p.capitalize() for p in base_name.split('-')]
    
    if ':cloud' in model_id:
        return f"{' '.join(parts)} (Cloud)"
    elif ':latest' in model_id:
        return ' '.join(parts)
    else:
        name, variant = model_id.split(':', 1)
        return f"{' '.join([p.capitalize() for p in name.split('-')])} ({variant})"

def main():
    # Read input from file argument or stdin
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            fetcher_output = f.read()
    else:
        fetcher_output = sys.stdin.read()
    
    fetcher_models = parse_fetcher_output(fetcher_output)
    
    config_path = Path.home() / "Library/Application Support/aichat/config.yaml"
    config_models = parse_config_models(config_path)
    
    missing_models = fetcher_models - config_models
    
    if not missing_models:
        print("# No missing models - config is up to date!", file=sys.stderr)
        return
    
    # Sort: cloud models first, then alphabetically
    cloud = sorted([m for m in missing_models if ':cloud' in m])
    local = sorted([m for m in missing_models if ':cloud' not in m])
    
    print("# Missing models found. Add these to your config.yaml:\n")
    
    if cloud:
        print("      # --- Cloud Models (Missing) ---")
        for model in cloud:
            print(f"      - name: {model}")
            print(f"        display_name: {format_display_name(model)}\n")
    
    if local:
        if cloud:
            print()
        print("      # --- Local Models (Missing) ---")
        for model in local:
            print(f"      - name: {model}")
            print(f"        display_name: {format_display_name(model)}\n")

if __name__ == "__main__":
    main()
