#!/usr/bin/env python3
import requests
import datetime
import urllib3 
from typing import List, Dict, Any, Optional

# Suppress the InsecureRequestWarning that can appear if verify=False is used in other contexts
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Configuration ---
API_URL = 'https://ollama.ldmathes.cc/v1/models'

# This dictionary contains comprehensive data (size, quantization, etc.) 
# that the live API often omits, providing the rich output the user preferred.
MOCK_MODELS_DATA: List[Dict[str, Any]] = [
    # Group 1: Cloud Models
    {'name': 'deepseek-v3.1:671b-cloud', 'size': 671000000000, 'modified_at': '2025-11-10T18:08:00Z', 'details': {'quantization': 'MoE'}},
    {'name': 'glm-4.6:cloud', 'size': 50000000000, 'modified_at': '2025-11-10T16:58:00Z', 'details': {'quantization': 'F32'}},
    {'name': 'gpt-oss:120b-cloud', 'size': 117000000000, 'modified_at': '2025-11-10T18:22:00Z', 'details': {'quantization': 'MoE'}},
    {'name': 'kimi-k2-thinking:cloud', 'size': 100000000000, 'modified_at': '2025-11-10T17:49:00Z', 'details': {'quantization': 'MoE'}},
    {'name': 'minimax-m2:cloud', 'size': 50000000000, 'modified_at': '2025-11-10T17:46:00Z', 'details': {'quantization': 'F32'}},
    {'name': 'qwen3-coder:480b-cloud', 'size': 480000000000, 'modified_at': '2025-11-10T18:09:00Z', 'details': {'quantization': 'MoE'}},
    
    # Group 2: Local & Specialty Models
    {'name': 'alfred:latest', 'size': 6500000000, 'modified_at': '2025-11-10T15:10:00Z', 'details': {'quantization': 'Q4_0'}},
    {'name': 'deepseek-r1:latest', 'size': 6500000000, 'modified_at': '2025-11-10T00:22:00Z', 'details': {'quantization': 'Q4_0'}},
    {'name': 'firefunction-v2:latest', 'size': 476800000, 'modified_at': '2025-11-10T02:58:00Z', 'details': {'quantization': 'Q2_K'}},
    {'name': 'gemma3:1b', 'size': 953700000, 'modified_at': '2025-11-09T22:38:00Z', 'details': {'quantization': 'Q2_K'}},
    {'name': 'gemma3:4b', 'size': 3700000000, 'modified_at': '2025-11-09T22:46:00Z', 'details': {'quantization': 'Q2_K'}},
    {'name': 'llava:13b', 'size': 12100000000, 'modified_at': '2025-11-10T18:06:00Z', 'details': {'quantization': 'Q4_0'}},
    {'name': 'mistral:latest', 'size': 6500000000, 'modified_at': '2025-11-09T22:58:00Z', 'details': {'quantization': 'Q4_0'}},
    {'name': 'notus:latest', 'size': 7500000000, 'modified_at': '2025-11-10T16:51:00Z', 'details': {'quantization': 'Q4_0'}},
    {'name': 'qwen3-coder:latest', 'size': 6500000000, 'modified_at': '2025-11-09T23:53:00Z', 'details': {'quantization': 'Q4_0'}},
]

# Create a quick lookup map for the mock data
MOCK_LOOKUP: Dict[str, Dict[str, Any]] = {m['name']: m for m in MOCK_MODELS_DATA}

# --- Utility Functions ---

def format_bytes(bytes_value: Optional[int]) -> str:
    """Converts bytes to a human-readable string (e.g., 4.7 GB)."""
    if bytes_value is None or bytes_value == 0:
        return 'N/A'
    k = 1024
    sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    i = 0
    while bytes_value >= k and i < len(sizes) - 1:
        bytes_value /= k
        i += 1
    return f"{bytes_value:.1f} {sizes[i]}"

def categorize_model(model: Dict[str, Any]) -> str:
    """Categorizes models into 'Cloud' or 'Local' based on name/size."""
    name = (model.get('name', '') or '').lower()
    size = model.get('size', 0) # Uses the rich mock data size if available
    
    # Use a size cutoff (100GB) and keyword check for categorization
    if 'cloud' in name or '480b' in name or '671b' in name or size > 100000000000:
        return 'Cloud'
    return 'Local'

def format_date(iso_string: Optional[str]) -> str:
    """Formats an ISO date string to a readable date."""
    if not iso_string:
        return 'N/A'
    try:
        # Note: 'modified_at' comes from mock data.
        dt = datetime.datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M')
    except ValueError:
        return 'Invalid Date'

# --- Main Fetch and Display Logic ---

def fetch_and_display_models():
    """
    Fetches the live list of models and merges it with rich mock data.
    If the fetch fails, it falls back to displaying the full mock data.
    """
    
    final_models_to_display: List[Dict[str, Any]] = []
    
    print(f"Attempting to fetch live model list from: {API_URL}")
    print("-" * 80)

    try:
        # Fetch the live list of models
        response = requests.get(API_URL, timeout=5, verify=False) 
        response.raise_for_status()
        
        live_models = response.json().get('data') # Live models are under 'data' key
        
        if live_models:
            print(f"✅ Successfully fetched list of {len(live_models)} live models. Merging with descriptive internal data.")
            
            # 1. Process and merge live list with mock details
            for live_model in live_models:
                model_id = live_model.get('id')
                rich_details = MOCK_LOOKUP.get(model_id, {})
                
                # Construct the final model object (live model list + mock details)
                consolidated_model = {
                    'name': model_id, # This field is required by categorize_model and print_category
                    'size': rich_details.get('size', 0),
                    'modified_at': rich_details.get('modified_at'), # The mock timestamp
                    'details': rich_details.get('details', {}),
                    # We can optionally keep the raw live data fields
                    'live_created': live_model.get('created'),
                    'live_owned_by': live_model.get('owned_by'),
                }
                final_models_to_display.append(consolidated_model)
            
        else:
            print(f"⚠️ API is online but returned an empty or unexpected model list. Falling back to internal mock data (list is NOT live).")
            final_models_to_display = MOCK_MODELS_DATA

    except requests.exceptions.RequestException as e:
        # Fallback to mock data if API call fails
        print(f"🚨 WARNING: API connection failed ({type(e).__name__}).")
        print("   Displaying full internal mock data (list is NOT live and may include offline models).")
        final_models_to_display = MOCK_MODELS_DATA

    print("-" * 80)
    
    # Categorize and prepare data for printing
    cloud_models = [m for m in final_models_to_display if categorize_model(m) == 'Cloud']
    local_models = [m for m in final_models_to_display if categorize_model(m) == 'Local']

    # Print function for a category
    def print_category(models_list: List[Dict[str, Any]], title: str, icon: str):
        print(f"\n{icon} {title} ({len(models_list)} models)")
        print("-" * 80)
        
        # Define header and format string for clean, columnar output
        header = "{:<30} | {:<10} | {:<16} | {:<10}"
        print(header.format("MODEL ID", "SIZE", "LAST MODIFIED", "QUANT"))
        print("-" * 80)
        
        # Sort for clean presentation
        sorted_models = sorted(models_list, key=lambda x: x.get('name', ''))

        for model in sorted_models:
            name = model.get('name', 'N/A')[:29] 
            size = format_bytes(model.get('size'))
            # Note: We use 'modified_at' from the rich mock data for the timestamp
            modified = format_date(model.get('modified_at')) 
            quantization = model.get('details', {}).get('quantization', 'Unknown')
            
            print(f"{name:<30} | {size:<10} | {modified:<16} | {quantization:<10}")
        print("-" * 80)


    # Print the categorized groups
    print_category(cloud_models, "CLOUD MODELS (High-Capacity)", "🚀")
    print_category(local_models, "LOCAL & SPECIALTY MODELS", "💻")


if __name__ == "__main__":
    fetch_and_display_models()
