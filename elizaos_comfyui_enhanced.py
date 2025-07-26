"""
Enhanced ElizaOS ComfyUI Integration with URL Mapping

This module provides enhanced integration between ElizaOS and ComfyUI with automatic
URL mapping to ensure generated images are accessible from the browser.
"""

import json
import time
from typing import Dict, Any, Optional
from local_workflow_client import (
    local_comfyui,
    generate_image_with_flux,
    get_comfyui_queue,
    get_comfyui_history,
    check_comfyui_status,
    get_image_urls
)

class EnhancedComfyUIHelper:
    def __init__(self):
        self.client = local_comfyui
    
    def generate_image_and_wait(self, prompt: str, wait_for_completion: bool = False, 
                               max_wait_time: int = 300, **kwargs) -> Dict[str, Any]:
        """
        Generate an image and optionally wait for completion with browser-accessible URLs.
        
        Args:
            prompt: The image description
            wait_for_completion: Whether to wait for the image to be generated
            max_wait_time: Maximum time to wait in seconds
            **kwargs: Additional parameters for image generation
            
        Returns:
            Dict with status, prompt_id, and browser-accessible image URLs
        """
        # Generate the image
        result = generate_image_with_flux(prompt, **kwargs)
        
        if result.get('status') != 'success':
            return result
        
        prompt_id = result.get('prompt_id')
        
        if not wait_for_completion:
            return {
                **result,
                'message': f'Image generation started for: "{prompt}"',
                'check_status': f'Use get_image_status("{prompt_id}") to check completion',
                'browser_note': 'Images will be accessible at http://localhost:8188 once completed'
            }
        
        # Wait for completion
        start_time = time.time()
        while time.time() - start_time < max_wait_time:
            # Check if generation is complete
            image_info = get_image_urls(prompt_id)
            
            if image_info.get('status') == 'success' and image_info.get('images'):
                return {
                    'status': 'success',
                    'prompt': prompt,
                    'prompt_id': prompt_id,
                    'message': f'Image generation completed for: "{prompt}"',
                    'images': image_info['images'],
                    'total_images': image_info['total_images'],
                    'browser_urls': [img['browser_url'] for img in image_info['images']],
                    'generation_time': f"{time.time() - start_time:.1f} seconds"
                }
            
            time.sleep(2)  # Check every 2 seconds
        
        # Timeout
        return {
            'status': 'timeout',
            'prompt': prompt,
            'prompt_id': prompt_id,
            'message': f'Image generation timed out after {max_wait_time} seconds',
            'check_status': f'Use get_image_status("{prompt_id}") to check completion manually'
        }
    
    def get_image_status(self, prompt_id: str) -> Dict[str, Any]:
        """
        Get the current status of an image generation with browser-accessible URLs.
        
        Args:
            prompt_id: The ComfyUI prompt ID
            
        Returns:
            Dict with current status and browser-accessible URLs if completed
        """
        # Check queue status
        queue_status = get_comfyui_queue()
        if queue_status.get('status') != 'success':
            return {"error": "Failed to get queue status", "details": queue_status}
        
        queue_data = queue_status.get('data', {})
        
        # Check if still in queue
        queue_running = queue_data.get('queue_running', [])
        queue_pending = queue_data.get('queue_pending', [])
        
        for item in queue_running:
            if len(item) > 1 and item[1] == prompt_id:
                return {
                    'status': 'running',
                    'prompt_id': prompt_id,
                    'message': 'Image generation is currently running',
                    'position': 'Currently executing'
                }
        
        for i, item in enumerate(queue_pending):
            if len(item) > 1 and item[1] == prompt_id:
                return {
                    'status': 'pending',
                    'prompt_id': prompt_id,
                    'message': f'Image generation is pending (position {i + 1} in queue)',
                    'position': f'{i + 1} of {len(queue_pending)}'
                }
        
        # Not in queue, check history for completion
        image_info = get_image_urls(prompt_id)
        
        if image_info.get('status') == 'success' and image_info.get('images'):
            return {
                'status': 'completed',
                'prompt_id': prompt_id,
                'message': 'Image generation completed',
                'images': image_info['images'],
                'total_images': image_info['total_images'],
                'browser_urls': [img['browser_url'] for img in image_info['images']]
            }
        else:
            return {
                'status': 'unknown',
                'prompt_id': prompt_id,
                'message': 'Image generation status unknown - may have failed or been cancelled',
                'details': image_info
            }
    
    def list_recent_images(self, limit: int = 10) -> Dict[str, Any]:
        """
        List recent generated images with browser-accessible URLs.
        
        Args:
            limit: Maximum number of recent images to retrieve
            
        Returns:
            Dict with recent images and their browser-accessible URLs
        """
        try:
            history_response = get_comfyui_history()
            
            if history_response.get('status') != 'success':
                return {"error": "Failed to get history", "details": history_response}
            
            history_data = history_response.get('data', {})
            
            recent_images = []
            count = 0
            
            # Get recent prompts (sorted by most recent)
            for prompt_id in sorted(history_data.keys(), reverse=True):
                if count >= limit:
                    break
                
                image_info = get_image_urls(prompt_id)
                if image_info.get('status') == 'success' and image_info.get('images'):
                    prompt_data = history_data[prompt_id]
                    prompt_text = "Unknown prompt"
                    
                    # Try to extract prompt text
                    try:
                        workflow = prompt_data.get('prompt', {})
                        for node_id, node_data in workflow.items():
                            if node_data.get('class_type') == 'CLIPTextEncode':
                                inputs = node_data.get('inputs', {})
                                if 'text' in inputs and inputs['text'].strip():
                                    prompt_text = inputs['text'][:100] + "..." if len(inputs['text']) > 100 else inputs['text']
                                    break
                    except:
                        pass
                    
                    recent_images.append({
                        'prompt_id': prompt_id,
                        'prompt_text': prompt_text,
                        'images': image_info['images'],
                        'total_images': image_info['total_images'],
                        'browser_urls': [img['browser_url'] for img in image_info['images']]
                    })
                    count += 1
            
            return {
                'status': 'success',
                'recent_images': recent_images,
                'total_found': len(recent_images),
                'message': f'Found {len(recent_images)} recent image generations'
            }
            
        except Exception as e:
            return {"error": "Exception occurred", "details": str(e)}

# Global enhanced helper instance
enhanced_comfyui = EnhancedComfyUIHelper()

# Enhanced convenience functions for ElizaOS
def generate_image_for_eliza(prompt: str, wait_for_completion: bool = True, **kwargs):
    """
    Generate an image for ElizaOS with automatic URL mapping and optional waiting.
    
    This is the main function ElizaOS should use for image generation.
    """
    return enhanced_comfyui.generate_image_and_wait(prompt, wait_for_completion, **kwargs)

def check_image_generation_status(prompt_id: str):
    """
    Check the status of an image generation with browser-accessible URLs.
    """
    return enhanced_comfyui.get_image_status(prompt_id)

def get_recent_generated_images(limit: int = 10):
    """
    Get recent generated images with browser-accessible URLs.
    """
    return enhanced_comfyui.list_recent_images(limit)

def quick_generate_image(prompt: str, **kwargs):
    """
    Quickly generate an image without waiting for completion.
    """
    return enhanced_comfyui.generate_image_and_wait(prompt, wait_for_completion=False, **kwargs)

# Example usage for testing
if __name__ == "__main__":
    print("Enhanced ElizaOS ComfyUI Integration")
    print("=" * 50)
    
    # Check if ComfyUI is running
    status = check_comfyui_status()
    print(f"ComfyUI Status: {status['status']}")
    
    if status['status'] == 'success':
        print("\n🎨 Testing quick image generation...")
        result = quick_generate_image(
            "A beautiful cyberpunk cityscape at night, neon lights, futuristic",
            negative_prompt="blurry, low quality",
            width=1024,
            height=1024
        )
        print(f"Result: {json.dumps(result, indent=2)}")
        
        if result.get('status') == 'success':
            prompt_id = result.get('prompt_id')
            print(f"\n📊 Checking status for prompt {prompt_id}...")
            
            # Wait a moment and check status
            import time
            time.sleep(5)
            status_result = check_image_generation_status(prompt_id)
            print(f"Status: {json.dumps(status_result, indent=2)}")
        
        print("\n📸 Getting recent images...")
        recent = get_recent_generated_images(limit=3)
        print(f"Recent images: {json.dumps(recent, indent=2)}")
    else:
        print(f"❌ ComfyUI is not accessible: {status['message']}")
        print("Please start ComfyUI first:") 