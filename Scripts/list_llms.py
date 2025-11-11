#!/usr/bin/env python3
"""
Simple script to extract and list LLMs from JSON input
Accepts JSON from stdin or a file
"""

import json
import sys

def list_llms(json_input):
    """Extract and list LLMs from JSON data"""
    try:
        if isinstance(json_input, str):
            data = json.loads(json_input)
        else:
            data = json.load(json_input)
        
        if 'data' in data and isinstance(data['data'], list):
            llms = []
            for item in data['data']:
                if 'id' in item:
                    llms.append(item['id'])
            
            print(f"Found {len(llms)} ollama active LLMs:")
            for i, llm in enumerate(llms, 1):
                print(f"{i}. {llm}")
            
            return llms
        else:
            print("Error: Unexpected JSON structure")
            return []
            
    except json.JSONDecodeError:
        print("Error: Invalid JSON input")
        return []

if __name__ == "__main__":
    # Check if reading from stdin (pipe)
    if not sys.stdin.isatty():
        # Read from stdin
        json_data = sys.stdin.read()
        list_llms(json_data)
    elif len(sys.argv) > 1:
        # Read from file
        json_file = sys.argv[1]
        try:
            with open(json_file, 'r') as f:
                list_llms(f)
        except FileNotFoundError:
            print(f"Error: File {json_file} not found")
    else:
        print("Usage:")
        print("  curl https://ollama.ldmathes.cc/v1/models | python3 list_llms.py")
        print("  python3 list_llms.py filename.json")
