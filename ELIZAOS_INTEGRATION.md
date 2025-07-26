# ElizaOS + ComfyUI Local Workflow Integration

## ✅ Status: Ready to Use!

Your ComfyUI instance is configured and working with local models. **No API tokens required!**

## 🎯 What You Have

- ✅ ComfyUI running with local models
- ✅ Flux model (`flux1-dev-fp8.safetensors`) available
- ✅ Your workflow template configured
- ✅ API endpoint accessible at `http://localhost:8188`

## 🚀 How to Use with ElizaOS

### Step 1: Import the Client

In your ElizaOS plugin or agent code:

```python
from local_workflow_client import (
    generate_image_with_flux,
    get_comfyui_queue,
    get_comfyui_history,
    check_comfyui_status
)
```

### Step 2: Generate Images

```python
# Simple image generation
result = generate_image_with_flux(
    prompt="A beautiful sunset over mountains, cinematic lighting"
)

# Advanced image generation with parameters
result = generate_image_with_flux(
    prompt="A majestic dragon flying over a medieval castle",
    negative_prompt="blurry, low quality, cartoon",
    width=1024,
    height=1024,
    steps=35,
    seed=12345,  # -1 for random
    guidance=3.5
)
```

### Step 3: Check Status

```python
# Check if ComfyUI is running
status = check_comfyui_status()

# Check queue status
queue = get_comfyui_queue()

# Get execution history
history = get_comfyui_history()
```

## 🎨 Example ElizaOS Agent Function

Here's how you can create a function for your ElizaOS agent:

```python
def generate_image_agent(prompt: str, **kwargs):
    """
    ElizaOS agent function to generate images using ComfyUI.
    
    Args:
        prompt: The image description
        **kwargs: Optional parameters (negative_prompt, width, height, etc.)
    
    Returns:
        Dict with status and prompt_id
    """
    try:
        # Check if ComfyUI is running
        status = check_comfyui_status()
        if status['status'] != 'success':
            return {
                "error": "ComfyUI is not running",
                "details": status['message']
            }
        
        # Generate the image
        result = generate_image_with_flux(prompt, **kwargs)
        
        if result['status'] == 'success':
            return {
                "success": True,
                "message": f"Image generation started: {prompt}",
                "prompt_id": result['prompt_id'],
                "queue_position": "Check queue status for details"
            }
        else:
            return {
                "error": "Failed to generate image",
                "details": result.get('error', 'Unknown error')
            }
            
    except Exception as e:
        return {
            "error": "Exception occurred",
            "details": str(e)
        }
```

## 📋 Available Parameters

When calling `generate_image_with_flux()`, you can use these parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `prompt` | Required | The image description |
| `negative_prompt` | `""` | Things to avoid in the image |
| `width` | `1024` | Image width |
| `height` | `1024` | Image height |
| `steps` | `35` | Sampling steps (higher = better quality, slower) |
| `seed` | `-1` | Random seed (-1 for random) |
| `guidance` | `3.5` | Guidance scale (higher = more prompt adherence) |

## 🔄 Workflow Details

Your workflow uses:
- **Model**: `flux1-dev-fp8.safetensors` (local)
- **Sampler**: Euler with 35 steps
- **Resolution**: 1024x1024
- **Guidance**: 3.5 (with FluxGuidance node)
- **Output**: Saved to `output/` directory

## 📁 Output Location

Generated images are saved to:
- **Directory**: `output/`
- **Filename format**: `ElizaOS_[prompt]_[timestamp].png`
- **Example**: `ElizaOS_A beautiful sunset over mounta_00001_.png`

## 🐛 Troubleshooting

### ComfyUI Not Running
```bash
# Start ComfyUI
./start_comfyui_api.sh
```

### Check Status
```python
status = check_comfyui_status()
print(status)
```

### Check Queue
```python
queue = get_comfyui_queue()
print(queue)
```

## 🎯 Example Usage Scenarios

### Scenario 1: Simple Image Generation
```python
result = generate_image_with_flux("A cute cat playing with yarn")
```

### Scenario 2: High-Quality Portrait
```python
result = generate_image_with_flux(
    prompt="A professional portrait of a woman with flowing red hair",
    negative_prompt="blurry, low quality, distorted",
    steps=50,
    guidance=4.0
)
```

### Scenario 3: Landscape with Specific Dimensions
```python
result = generate_image_with_flux(
    prompt="A serene mountain lake at sunset",
    width=1024,
    height=768,
    seed=42  # Reproducible result
)
```

## ✅ Success Indicators

You'll know everything is working when:
1. `check_comfyui_status()` returns `{"status": "success"}`
2. `generate_image_with_flux()` returns a `prompt_id`
3. Images appear in the `output/` directory
4. No error messages in the response

---

**🎉 You're all set!** Your ElizaOS system can now generate high-quality images using local ComfyUI workflows without any external dependencies or API tokens. 