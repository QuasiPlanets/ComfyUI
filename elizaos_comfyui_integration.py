"""
ElizaOS ComfyUI Integration Helper

This module provides helper functions for integrating ComfyUI API nodes with ElizaOS.
It handles authentication and provides easy-to-use functions for the LLM to call.
"""

import json
import requests
from typing import Dict, Any, Optional
from api_config import get_api_config

class ElizaOSComfyUIHelper:
    def __init__(self, comfyui_url="http://localhost:8188"):
        self.comfyui_url = comfyui_url
        self.api_config = get_api_config()
    
    def check_api_configuration(self) -> Dict[str, Any]:
        """
        Checks if the API is properly configured.
        Returns status information for the LLM.
        """
        config = get_api_config()
        is_configured = config['api_key_comfy_org'] != "your_comfy_org_api_key_here"
        
        return {
            "configured": is_configured,
            "services_available": [
                "Kling (Text-to-Video, Image-to-Video, Video Effects)",
                "Luma (Text-to-Video, Image-to-Video)",
                "Flux (Image Generation)",
                "Pika (Video Generation)",
                "Stability AI (Image Generation)",
                "OpenAI (Chat, Image Generation)",
                "Gemini (Text Generation)",
                "And many more..."
            ],
            "setup_instructions": [
                "1. Get an API key from https://platform.comfy.org/login",
                "2. Update api_config.py with your API key",
                "3. Or set COMFY_ORG_API_KEY environment variable",
                "4. Restart ComfyUI after configuration"
            ] if not is_configured else []
        }
    
    def generate_video_with_kling(self, prompt: str, negative_prompt: str = "", 
                                 aspect_ratio: str = "16:9", duration: str = "5s") -> Dict[str, Any]:
        """
        Generates a video using Kling Text-to-Video API.
        """
        if not self._is_api_configured():
            return {"error": "API not configured. Please set up authentication first."}
        
        workflow = {
            "1": {
                "class_type": "KlingTextToVideoNode",
                "inputs": {
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "cfg_scale": 0.75,
                    "aspect_ratio": aspect_ratio,
                    "mode": f"standard mode / {duration} / kling-v1"
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
        
        return self._queue_workflow(workflow, "Kling Text-to-Video")
    
    def generate_image_with_flux(self, prompt: str, negative_prompt: str = "", 
                                aspect_ratio: str = "1:1") -> Dict[str, Any]:
        """
        Generates an image using Flux Image Generation API.
        """
        if not self._is_api_configured():
            return {"error": "API not configured. Please set up authentication first."}
        
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
        
        return self._queue_workflow(workflow, "Flux Image Generation")
    
    def generate_video_with_luma(self, prompt: str, negative_prompt: str = "", 
                                aspect_ratio: str = "16:9") -> Dict[str, Any]:
        """
        Generates a video using Luma Text-to-Video API.
        """
        if not self._is_api_configured():
            return {"error": "API not configured. Please set up authentication first."}
        
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
        
        return self._queue_workflow(workflow, "Luma Text-to-Video")
    
    def get_queue_status(self) -> Dict[str, Any]:
        """
        Gets the current queue status.
        """
        try:
            response = requests.get(f"{self.comfyui_url}/queue")
            response.raise_for_status()
            return {"status": "success", "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get queue status: {str(e)}"}
    
    def get_history(self, prompt_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Gets the execution history.
        """
        try:
            url = f"{self.comfyui_url}/history"
            if prompt_id:
                url += f"/{prompt_id}"
            
            response = requests.get(url)
            response.raise_for_status()
            return {"status": "success", "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get history: {str(e)}"}
    
    def _is_api_configured(self) -> bool:
        """
        Checks if the API is properly configured.
        """
        config = get_api_config()
        return config['api_key_comfy_org'] != "your_comfy_org_api_key_here"
    
    def _queue_workflow(self, workflow: Dict[str, Any], workflow_type: str) -> Dict[str, Any]:
        """
        Queues a workflow with authentication.
        """
        payload = {
            "prompt": workflow,
            "extra_data": self.api_config
        }
        
        try:
            response = requests.post(
                f"{self.comfyui_url}/prompt",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            result = response.json()
            
            return {
                "status": "success",
                "workflow_type": workflow_type,
                "prompt_id": result.get('prompt_id'),
                "message": f"{workflow_type} workflow queued successfully"
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to queue {workflow_type} workflow: {str(e)}"}

# Global instance for ElizaOS to use
elizaos_comfyui = ElizaOSComfyUIHelper()

# Convenience functions for the LLM to call
def check_comfyui_api_status():
    """Check if ComfyUI API is properly configured."""
    return elizaos_comfyui.check_api_configuration()

def generate_video(prompt: str, service: str = "kling", **kwargs):
    """Generate a video using the specified service."""
    if service.lower() == "kling":
        return elizaos_comfyui.generate_video_with_kling(prompt, **kwargs)
    elif service.lower() == "luma":
        return elizaos_comfyui.generate_video_with_luma(prompt, **kwargs)
    else:
        return {"error": f"Unknown service: {service}. Available: kling, luma"}

def generate_image(prompt: str, service: str = "flux", **kwargs):
    """Generate an image using the specified service."""
    if service.lower() == "flux":
        return elizaos_comfyui.generate_image_with_flux(prompt, **kwargs)
    else:
        return {"error": f"Unknown service: {service}. Available: flux"}

def get_comfyui_queue():
    """Get the current ComfyUI queue status."""
    return elizaos_comfyui.get_queue_status()

def get_comfyui_history(prompt_id: Optional[str] = None):
    """Get ComfyUI execution history."""
    return elizaos_comfyui.get_history(prompt_id)

# Example usage for testing
if __name__ == "__main__":
    print("ElizaOS ComfyUI Integration Helper")
    print("=" * 40)
    
    # Check API configuration
    status = check_comfyui_api_status()
    print(f"API Configured: {status['configured']}")
    
    if not status['configured']:
        print("\nSetup Instructions:")
        for instruction in status['setup_instructions']:
            print(f"  {instruction}")
    else:
        print("\nAvailable Services:")
        for service in status['services_available']:
            print(f"  • {service}")
        
        # Test video generation
        print("\nTesting video generation...")
        result = generate_video(
            "A beautiful sunset over mountains, cinematic lighting",
            service="kling",
            negative_prompt="blurry, low quality"
        )
        print(f"Result: {json.dumps(result, indent=2)}") 