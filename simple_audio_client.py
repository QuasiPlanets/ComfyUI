"""
Simple Audio Client for ElizaOS

Provides easy-to-use functions for audio generation using ComfyUI's Stable Audio Open model.
All URLs returned are browser-accessible from localhost.
"""

import time
import json
from typing import Dict, Any, Optional, List
from local_workflow_client import (
    local_comfyui,
    generate_audio_with_stable_audio,
    get_comfyui_queue,
    get_comfyui_history,
    check_comfyui_status,
    get_audio_urls
)

def generate_audio_simple(prompt: str, 
                         negative_prompt: str = "distorted, low quality, silence",
                         duration: float = 30.0,
                         steps: int = 50,
                         cfg: float = 4.98,
                         seed: int = -1) -> Dict[str, Any]:
    """
    Generate audio with simple parameters.
    
    Args:
        prompt: Audio description (e.g., "electronic dance music like grimes")
        negative_prompt: Things to avoid in the audio
        duration: Audio duration in seconds
        steps: Quality steps (higher = better quality, slower)
        cfg: CFG scale (creativity vs adherence)
        seed: Random seed (-1 for random)
    
    Returns:
        Dict with success status, prompt_id, and message
    """
    try:
        # Check if ComfyUI is running
        status = check_comfyui_status()
        if status['status'] != 'success':
            return {
                "success": False,
                "error": "ComfyUI is not running",
                "details": status['message']
            }
        
        # Generate audio
        result = generate_audio_with_stable_audio(
            prompt=prompt,
            negative_prompt=negative_prompt,
            duration=duration,
            steps=steps,
            cfg=cfg,
            seed=seed
        )
        
        if result.get('status') == 'success':
            return {
                "success": True,
                "prompt_id": result['prompt_id'],
                "message": f"Audio generation started: {prompt}",
                "status": "queued",
                "audio_urls": [],  # Empty until completed
                "note": "Check status with get_audio_status_simple(prompt_id)"
            }
        else:
            return {
                "success": False,
                "error": "Failed to generate audio",
                "details": result.get('error', 'Unknown error')
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": "Exception occurred",
            "details": str(e)
        }

def get_audio_status_simple(prompt_id: str) -> Dict[str, Any]:
    """
    Check if audio generation is complete and get URLs.
    
    Args:
        prompt_id: The ComfyUI prompt ID from generate_audio_simple()
    
    Returns:
        Dict with status and audio URLs (if completed)
    """
    try:
        # Get history for this specific prompt
        history = get_comfyui_history(prompt_id)
        
        if history.get('status') != 'success':
            return {
                "success": False,
                "error": "Failed to get history",
                "details": history.get('error', 'Unknown error')
            }
        
        history_data = history.get('data', {})
        
        if prompt_id not in history_data:
            # Check if it's still in queue
            queue = get_comfyui_queue()
            if queue.get('status') == 'success':
                queue_data = queue.get('data', {})
                queue_running = queue_data.get('queue_running', [])
                queue_pending = queue_data.get('queue_pending', [])
                
                # Check if prompt is in running queue
                for item in queue_running:
                    if len(item) >= 2 and item[1] == prompt_id:
                        return {
                            "success": True,
                            "status": "running",
                            "message": "Audio generation is currently running",
                            "audio_urls": []
                        }
                
                # Check if prompt is in pending queue
                for item in queue_pending:
                    if len(item) >= 2 and item[1] == prompt_id:
                        position = queue_pending.index(item) + 1
                        return {
                            "success": True,
                            "status": "pending",
                            "message": f"Audio generation is pending (position {position} in queue)",
                            "audio_urls": []
                        }
            
            return {
                "success": False,
                "status": "unknown",
                "error": "Prompt not found in history or queue",
                "audio_urls": []
            }
        
        # Prompt is in history, so it's completed
        # Get the audio URLs using the audio URL mapper
        audio_info = get_audio_urls(prompt_id)
        
        if audio_info.get('status') == 'success':
            audio_urls = audio_info.get('audio_urls', [])
            total_audio = audio_info.get('total_audio', 0)
            
            return {
                "success": True,
                "status": "completed",
                "message": f"Audio generation completed",
                "audio_urls": audio_urls,
                "total_audio": total_audio
            }
        else:
            return {
                "success": False,
                "status": "completed_error",
                "error": "Audio generation completed but failed to get URLs",
                "details": audio_info.get('error', 'Unknown error'),
                "audio_urls": []
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": "Exception occurred",
            "details": str(e),
            "audio_urls": []
        }

def get_recent_audio_simple(limit: int = 10) -> Dict[str, Any]:
    """
    Get recent audio generations with browser-accessible URLs.
    
    Args:
        limit: Maximum number of recent audio generations to return
    
    Returns:
        Dict with recent audio generations and their URLs
    """
    try:
        # Get full history
        history = get_comfyui_history()
        
        if history.get('status') != 'success':
            return {
                "success": False,
                "error": "Failed to get history",
                "details": history.get('error', 'Unknown error')
            }
        
        history_data = history.get('data', {})
        recent_audio = []
        
        # Sort by most recent (assuming higher prompt IDs are more recent)
        sorted_prompts = sorted(history_data.keys(), reverse=True)
        
        for prompt_id in sorted_prompts[:limit * 2]:  # Get more to filter for audio
            # Get audio URLs for this prompt
            audio_info = get_audio_urls(prompt_id)
            
            if audio_info.get('status') == 'success' and audio_info.get('audio_urls'):
                recent_audio.append({
                    "prompt_id": prompt_id,
                    "audio_urls": audio_info['audio_urls'],
                    "total_audio": audio_info.get('total_audio', 0)
                })
                
                if len(recent_audio) >= limit:
                    break
        
        return {
            "success": True,
            "audio": recent_audio,
            "total": len(recent_audio)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": "Exception occurred",
            "details": str(e)
        }

def wait_for_audio_completion(prompt_id: str, max_wait: int = 300, check_interval: int = 5) -> Dict[str, Any]:
    """
    Wait for audio generation to complete and return URLs.
    
    Args:
        prompt_id: The ComfyUI prompt ID
        max_wait: Maximum time to wait in seconds
        check_interval: How often to check status in seconds
    
    Returns:
        Dict with final status and audio URLs
    """
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        status = get_audio_status_simple(prompt_id)
        
        if not status['success']:
            return status
        
        if status['status'] == 'completed':
            return status
        elif status['status'] in ['running', 'pending']:
            time.sleep(check_interval)
            continue
        else:
            return {
                "success": False,
                "status": "timeout",
                "error": f"Audio generation status unknown: {status['status']}",
                "audio_urls": []
            }
    
    return {
        "success": False,
        "status": "timeout",
        "error": f"Audio generation did not complete within {max_wait} seconds",
        "audio_urls": []
    }

# Example usage for testing
if __name__ == "__main__":
    print("🎵 Simple Audio Client for ElizaOS")
    print("=" * 40)
    
    # Check if ComfyUI is running
    status = check_comfyui_status()
    print(f"ComfyUI Status: {status['status']}")
    print(f"Message: {status['message']}")
    
    if status['status'] == 'success':
        # Test audio generation
        print("\n🎵 Testing audio generation...")
        result = generate_audio_simple(
            prompt="electronic dance music like grimes, upbeat tempo, dreamy synths",
            negative_prompt="distorted, low quality, silence",
            duration=15.0,  # Short duration for testing
            steps=30       # Faster generation for testing
        )
        print(f"Generation Result:")
        print(json.dumps(result, indent=2))
        
        if result['success']:
            prompt_id = result['prompt_id']
            
            # Wait for completion (shorter timeout for testing)
            print(f"\n⏳ Waiting for audio generation to complete...")
            completion_result = wait_for_audio_completion(prompt_id, max_wait=120)
            print(f"Completion Result:")
            print(json.dumps(completion_result, indent=2))
            
            if completion_result['success'] and completion_result['audio_urls']:
                print(f"\n✅ Audio URLs (browser accessible):")
                for url in completion_result['audio_urls']:
                    print(f"   {url}")
        
        # Check recent audio
        print(f"\n📂 Recent audio generations:")
        recent = get_recent_audio_simple(limit=3)
        print(json.dumps(recent, indent=2))
        
    else:
        print("\n❌ ComfyUI is not running. Please start ComfyUI first:")
        print("   ./start_comfyui_api.sh")
        print("   or")
        print("   python main.py --listen 0.0.0.0 --port 8188 --enable-cors-header") 