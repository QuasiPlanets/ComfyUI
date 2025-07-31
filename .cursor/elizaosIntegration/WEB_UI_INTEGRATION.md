# 🎯 ElizaOS Web UI Integration - Image Links Fixed!

## ✅ Problem Solved

Your web UI was not getting image links because the URLs were in internal Docker network format (`172.19.0.4:8188`) instead of browser-accessible format (`localhost:8188`).

## 🚀 Use This Simple Client

**File**: `simple_image_client.py` - This is what your ElizaOS web UI should use.

### Main Functions

```python
from simple_image_client import (
    generate_image_simple,
    get_image_status_simple,
    get_recent_images_simple,
    wait_for_image_completion
)
```

## 📋 Function Reference

### 1. Generate Image
```python
result = generate_image_simple(
    prompt="A beautiful sunset over mountains",
    negative_prompt="blurry, low quality",
    width=1024,
    height=1024
)

# Returns:
{
    "success": True,
    "prompt_id": "abc123...",
    "message": "Image generation started: A beautiful sunset over mountains",
    "status": "queued",
    "image_urls": [],  # Empty until completed
    "note": "Check status with get_image_status()"
}
```

### 2. Check Status
```python
status = get_image_status_simple("abc123...")

# Returns when completed:
{
    "success": True,
    "status": "completed",
    "message": "Image generation completed",
    "image_urls": [
        "http://localhost:8188/view?filename=ElizaOS_00024_.png&subfolder=&type=output"
    ],
    "total_images": 1
}
```

### 3. Get Recent Images
```python
recent = get_recent_images_simple(limit=5)

# Returns:
{
    "success": True,
    "images": [
        {
            "prompt_id": "abc123...",
            "image_urls": [
                "http://localhost:8188/view?filename=ElizaOS_00024_.png&subfolder=&type=output"
            ]
        }
    ],
    "total": 1
}
```

### 4. Wait for Completion
```python
result = wait_for_image_completion("abc123...", max_wait=300)

# Returns when completed:
{
    "success": True,
    "status": "completed",
    "message": "Image generation completed",
    "image_urls": [
        "http://localhost:8188/view?filename=ElizaOS_00024_.png&subfolder=&type=output"
    ],
    "total_images": 1
}
```

## 🎨 Example ElizaOS Web UI Integration

```python
# In your ElizaOS web UI handler
from simple_image_client import generate_image_simple, get_image_status_simple

class ImageGenerationHandler:
    def handle_generate_image(self, prompt: str, user_id: str):
        """Handle image generation request from web UI"""
        
        # Start generation
        result = generate_image_simple(
            prompt=prompt,
            negative_prompt="blurry, low quality, distorted",
            width=1024,
            height=1024
        )
        
        if result['success']:
            return {
                'status': 'success',
                'message': result['message'],
                'prompt_id': result['prompt_id'],
                'next_action': 'check_status'
            }
        else:
            return {
                'status': 'error',
                'message': result.get('error', 'Unknown error')
            }
    
    def handle_check_status(self, prompt_id: str):
        """Check if image generation is complete"""
        
        status = get_image_status_simple(prompt_id)
        
        if status['success'] and status['status'] == 'completed':
            return {
                'status': 'completed',
                'message': status['message'],
                'image_urls': status['image_urls'],  # These work in browser!
                'total_images': status['total_images']
            }
        elif status['success']:
            return {
                'status': status['status'],  # 'running' or 'pending'
                'message': status['message'],
                'image_urls': []
            }
        else:
            return {
                'status': 'error',
                'message': status.get('error', 'Unknown error')
            }
```

## 🌐 URL Format

**Before (Broken)**:
```
http://172.19.0.4:8188/view?filename=ElizaOS_00024_.png&subfolder=&type=output
```

**After (Working)**:
```
http://localhost:8188/view?filename=ElizaOS_00024_.png&subfolder=&type=output
```

## ✅ Verification

The URLs are now:
- ✅ Browser accessible from `localhost:3001`
- ✅ Properly mapped from internal Docker network
- ✅ Return HTTP 200 status codes
- ✅ Display images correctly

## 🔧 Testing

```bash
# Test the simple client
python simple_image_client.py

# Test URL accessibility
python -c "
from simple_image_client import get_recent_images_simple
import requests

recent = get_recent_images_simple(limit=1)
if recent['success'] and recent['images']:
    url = recent['images'][0]['image_urls'][0]
    print(f'Testing: {url}')
    response = requests.head(url, timeout=5)
    print(f'Accessible: {response.status_code == 200}')
"
```

## 🎯 Key Points

1. **Use `simple_image_client.py`** - It handles URL mapping automatically
2. **Check `image_urls` field** - Contains browser-accessible URLs
3. **Wait for completion** - URLs are empty until generation finishes
4. **All URLs work** - No more `172.19.0.4` internal addresses

## 🎉 Result

Your ElizaOS web UI will now receive proper image URLs that work from the browser at `localhost:3001`! 