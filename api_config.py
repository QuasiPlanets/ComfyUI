"""
API Configuration for ComfyUI API Nodes

This file contains the authentication tokens needed for the various API-based nodes
in ComfyUI (Kling, Luma, Flux, etc.).

To use these nodes, you need to:
1. Get an API key from https://platform.comfy.org/login
2. Replace the placeholder values below with your actual API keys
3. Pass these tokens in the extra_data when making API requests

For security, consider using environment variables instead of hardcoding these values.
"""

# Comfy.org API Configuration
# Get your API key from: https://platform.comfy.org/login
COMFY_ORG_API_KEY = "your_comfy_org_api_key_here"  # Replace with your actual API key

# Alternative: Use environment variables for better security
import os

# You can set these environment variables instead of hardcoding:
# export COMFY_ORG_API_KEY="your_actual_api_key_here"

def get_api_config():
    """
    Returns the API configuration dictionary that should be passed in extra_data
    when making requests to ComfyUI API nodes.
    """
    return {
        "api_key_comfy_org": os.getenv("COMFY_ORG_API_KEY", COMFY_ORG_API_KEY),
        # Add other API keys here if needed
    }

def get_auth_headers():
    """
    Returns authentication headers for direct API calls (if needed).
    """
    return {
        "Authorization": f"Bearer {get_api_config()['api_key_comfy_org']}",
        "Content-Type": "application/json"
    }

# Example usage:
if __name__ == "__main__":
    config = get_api_config()
    print("API Configuration:")
    print(f"Comfy.org API Key: {config['api_key_comfy_org'][:10]}..." if config['api_key_comfy_org'] != "your_comfy_org_api_key_here" else "Not configured")
    
    if config['api_key_comfy_org'] == "your_comfy_org_api_key_here":
        print("\n⚠️  Please configure your API keys:")
        print("1. Get an API key from https://platform.comfy.org/login")
        print("2. Replace the placeholder in this file or set the COMFY_ORG_API_KEY environment variable")
        print("3. Restart ComfyUI after making changes") 