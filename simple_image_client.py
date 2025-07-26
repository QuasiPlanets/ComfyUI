"""
Simple Image Client for ElizaOS Web UI

This provides a simple interface that returns image URLs in a format
compatible with web UIs, ensuring the URLs are browser-accessible.
"""

import json
import time
from typing import Dict, Any, List, Optional
from local_workflow_client import (
    local_comfyui,
    generate_image_with_flux,
    get_comfyui_queue,
    get_comfyui_history,
    check_comfyui_status
)

def generate_image_simple(prompt: str, **kwargs) -> Dict[str, Any]:
    """
    Generate an image and return simple, web UI compatible results.
    
    Args:
        prompt: The image description
        **kwargs: Additional parameters (negative_prompt, width, height, etc.)
    
    Returns:
        Dict with simple structure for web UI
    """
    try:
        # Generate the image
        result = generate_image_with_flux(prompt, **kwargs)
        
        if result.get('status') != 'success':
            return {
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'message': result.get('message', 'Failed to generate image')
            }
        
        prompt_id = result.get('prompt_id')
        
        return {
            'success': True,
            'prompt_id': prompt_id,
            'message': f'Image generation started: {prompt}',
            'status': 'queued',
            'image_urls': [],  # Will be populated when complete
            'note': 'Check status with get_image_status()'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': 'Exception occurred during image generation'
        }

def get_image_status_simple(prompt_id: str) -> Dict[str, Any]:
    """
    Get image status in a simple, web UI compatible format.
    
    Args:
        prompt_id: The ComfyUI prompt ID
    
    Returns:
        Dict with status and image URLs if available
    """
    try:
        # Check queue status
        queue_response = get_comfyui_queue()
        if queue_response.get('status') != 'success':
            return {
                'success': False,
                'error': 'Failed to get queue status',
                'status': 'unknown'
            }
        
        queue_data = queue_response.get('data', {})
        queue_running = queue_data.get('queue_running', [])
        queue_pending = queue_data.get('queue_pending', [])
        
        # Check if still in queue
        for item in queue_running:
            if len(item) > 1 and item[1] == prompt_id:
                return {
                    'success': True,
                    'status': 'running',
                    'message': 'Image is currently being generated',
                    'image_urls': []
                }
        
        for i, item in enumerate(queue_pending):
            if len(item) > 1 and item[1] == prompt_id:
                return {
                    'success': True,
                    'status': 'pending',
                    'message': f'Image is in queue (position {i + 1})',
                    'image_urls': []
                }
        
        # Not in queue, check if completed
        history_response = get_comfyui_history(prompt_id)
        if history_response.get('status') != 'success':
            return {
                'success': False,
                'error': 'Failed to get history',
                'status': 'unknown'
            }
        
        history_data = history_response.get('data', {})
        if prompt_id not in history_data:
            return {
                'success': False,
                'error': 'Prompt not found in history',
                'status': 'unknown'
            }
        
        prompt_history = history_data[prompt_id]
        outputs = prompt_history.get('outputs', {})
        
        # Extract image URLs
        image_urls = []
        for node_id, output in outputs.items():
            if 'images' in output:
                for image_info in output['images']:
                    filename = image_info.get('filename', '')
                    subfolder = image_info.get('subfolder', '')
                    type_param = image_info.get('type', 'output')
                    
                    # Create browser-accessible URL
                    browser_url = f"http://localhost:8188/view?filename={filename}&subfolder={subfolder}&type={type_param}"
                    image_urls.append(browser_url)
        
        if image_urls:
            return {
                'success': True,
                'status': 'completed',
                'message': 'Image generation completed',
                'image_urls': image_urls,
                'total_images': len(image_urls)
            }
        else:
            return {
                'success': False,
                'status': 'failed',
                'message': 'No images found in output',
                'image_urls': []
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'status': 'error'
        }

def get_recent_images_simple(limit: int = 5) -> Dict[str, Any]:
    """
    Get recent images in a simple format.
    
    Args:
        limit: Maximum number of recent images to retrieve
    
    Returns:
        Dict with recent images and their URLs
    """
    try:
        history_response = get_comfyui_history()
        if history_response.get('status') != 'success':
            return {
                'success': False,
                'error': 'Failed to get history',
                'images': []
            }
        
        history_data = history_response.get('data', {})
        recent_images = []
        count = 0
        
        # Get recent prompts
        for prompt_id in sorted(history_data.keys(), reverse=True):
            if count >= limit:
                break
            
            status_result = get_image_status_simple(prompt_id)
            if status_result.get('success') and status_result.get('status') == 'completed':
                recent_images.append({
                    'prompt_id': prompt_id,
                    'image_urls': status_result.get('image_urls', [])
                })
                count += 1
        
        return {
            'success': True,
            'images': recent_images,
            'total': len(recent_images)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'images': []
        }

def wait_for_image_completion(prompt_id: str, max_wait: int = 300) -> Dict[str, Any]:
    """
    Wait for image generation to complete and return URLs.
    
    Args:
        prompt_id: The ComfyUI prompt ID
        max_wait: Maximum time to wait in seconds
    
    Returns:
        Dict with completion status and image URLs
    """
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        status_result = get_image_status_simple(prompt_id)
        
        if status_result.get('status') == 'completed':
            return status_result
        elif status_result.get('status') in ['failed', 'error']:
            return status_result
        
        time.sleep(2)  # Check every 2 seconds
    
    return {
        'success': False,
        'status': 'timeout',
        'message': f'Image generation timed out after {max_wait} seconds',
        'image_urls': []
    }

# Example usage
if __name__ == "__main__":
    print("Simple Image Client Test")
    print("=" * 30)
    
    # Test image generation
    print("\n🎨 Testing image generation...")
    result = generate_image_simple(
        "A beautiful sunset over mountains, cinematic lighting",
        negative_prompt="blurry, low quality"
    )
    print(f"Generation result: {json.dumps(result, indent=2)}")
    
    if result.get('success'):
        prompt_id = result.get('prompt_id')
        print(f"\n📊 Checking status for {prompt_id}...")
        
        # Wait and check status
        time.sleep(10)
        status = get_image_status_simple(prompt_id)
        print(f"Status: {json.dumps(status, indent=2)}")
        
        if status.get('image_urls'):
            print("\n🌐 Browser-accessible URLs:")
            for url in status['image_urls']:
                print(f"  - {url}")
    
    # Test recent images
    print("\n📸 Getting recent images...")
    recent = get_recent_images_simple(limit=3)
    print(f"Recent images: {json.dumps(recent, indent=2)}") 