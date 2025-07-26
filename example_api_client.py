"""
Example API Client for ComfyUI with Authentication

This script demonstrates how to use ComfyUI API nodes with proper authentication.
It shows how to create workflows with API-based nodes and pass authentication tokens.
"""

import json
import requests
from api_config import get_api_config

class ComfyUIAPIClient:
    def __init__(self, base_url="http://localhost:8188"):
        self.base_url = base_url
        self.api_config = get_api_config()
    
    def create_kling_text_to_video_workflow(self, prompt, negative_prompt="", aspect_ratio="16:9"):
        """
        Creates a workflow using the Kling Text to Video node.
        """
        workflow = {
            "1": {
                "class_type": "KlingTextToVideoNode",
                "inputs": {
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "cfg_scale": 0.75,
                    "aspect_ratio": aspect_ratio,
                    "mode": "standard mode / 5s duration / kling-v1"
                }
            },
            "2": {
                "class_type": "SaveVideo",
                "inputs": {
                    "filename_prefix": "KlingVideo",
                    "video": ["1", 0]
                }
            }
        }
        return workflow
    
    def create_luma_text_to_video_workflow(self, prompt, negative_prompt="", aspect_ratio="16:9"):
        """
        Creates a workflow using the Luma Text to Video node.
        """
        workflow = {
            "1": {
                "class_type": "LumaTextToVideoNode",
                "inputs": {
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "aspect_ratio": aspect_ratio,
                    "model": "luma-v1",
                    "duration": "5"
                }
            },
            "2": {
                "class_type": "SaveVideo",
                "inputs": {
                    "filename_prefix": "LumaVideo",
                    "video": ["1", 0]
                }
            }
        }
        return workflow
    
    def create_flux_image_generation_workflow(self, prompt, negative_prompt="", aspect_ratio="1:1"):
        """
        Creates a workflow using the Flux Image Generation node.
        """
        workflow = {
            "1": {
                "class_type": "FluxKontextProImageNode",
                "inputs": {
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "aspect_ratio": aspect_ratio,
                    "seed": 1234
                }
            },
            "2": {
                "class_type": "SaveImage",
                "inputs": {
                    "filename_prefix": "FluxImage",
                    "images": ["1", 0]
                }
            }
        }
        return workflow
    
    def queue_prompt(self, workflow, extra_data=None):
        """
        Queues a prompt with the given workflow and authentication.
        """
        if extra_data is None:
            extra_data = {}
        
        # Add API authentication to extra_data
        extra_data.update(self.api_config)
        
        payload = {
            "prompt": workflow,
            "extra_data": extra_data
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/prompt",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error queuing prompt: {e}")
            return None
    
    def get_queue_status(self):
        """
        Gets the current queue status.
        """
        try:
            response = requests.get(f"{self.base_url}/queue")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting queue status: {e}")
            return None
    
    def get_history(self, prompt_id=None):
        """
        Gets the execution history.
        """
        url = f"{self.base_url}/history"
        if prompt_id:
            url += f"/{prompt_id}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting history: {e}")
            return None

def main():
    """
    Example usage of the ComfyUI API client.
    """
    client = ComfyUIAPIClient()
    
    # Check if API is configured
    config = get_api_config()
    if config['api_key_comfy_org'] == "your_comfy_org_api_key_here":
        print("❌ API not configured. Please set up your API keys first.")
        print("1. Get an API key from https://platform.comfy.org/login")
        print("2. Update api_config.py or set COMFY_ORG_API_KEY environment variable")
        return
    
    print("✅ API configured successfully!")
    
    # Example 1: Kling Text to Video
    print("\n🎬 Creating Kling Text to Video workflow...")
    kling_workflow = client.create_kling_text_to_video_workflow(
        prompt="A beautiful sunset over mountains, cinematic lighting",
        negative_prompt="blurry, low quality",
        aspect_ratio="16:9"
    )
    
    result = client.queue_prompt(kling_workflow)
    if result:
        print(f"✅ Kling workflow queued successfully!")
        print(f"Prompt ID: {result.get('prompt_id', 'N/A')}")
    
    # Example 2: Flux Image Generation
    print("\n🖼️  Creating Flux Image Generation workflow...")
    flux_workflow = client.create_flux_image_generation_workflow(
        prompt="A majestic dragon flying over a medieval castle, fantasy art",
        negative_prompt="cartoon, anime, low quality",
        aspect_ratio="1:1"
    )
    
    result = client.queue_prompt(flux_workflow)
    if result:
        print(f"✅ Flux workflow queued successfully!")
        print(f"Prompt ID: {result.get('prompt_id', 'N/A')}")
    
    # Check queue status
    print("\n📊 Current queue status:")
    queue_status = client.get_queue_status()
    if queue_status:
        print(json.dumps(queue_status, indent=2))

if __name__ == "__main__":
    main() 