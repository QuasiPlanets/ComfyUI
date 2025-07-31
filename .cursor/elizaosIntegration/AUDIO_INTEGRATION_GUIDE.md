# 🎵 ElizaOS + ComfyUI Audio Generation Integration Guide

## ✅ Status: Ready to Use!

Your ComfyUI instance is now configured for both image AND audio generation using local models. **No API tokens required!**

## 🎯 What You Have

- ✅ ComfyUI running with local models
- ✅ Stable Audio Open model (`stable-audio-open-1.0.safetensors`) workflow configured
- ✅ T5 CLIP model (`t5-base.safetensors`) for text encoding
- ✅ Audio workflow template integrated
- ✅ Browser-accessible audio URLs (localhost:8188)
- ✅ API endpoint accessible at `http://localhost:8188`

## 🚀 How to Use Audio Generation with ElizaOS

### Step 1: Import the Simple Audio Client

In your ElizaOS plugin or agent code:

```python
from simple_audio_client import (
    generate_audio_simple,
    get_audio_status_simple,
    get_recent_audio_simple,
    wait_for_audio_completion
)
```

### Step 2: Generate Audio

```python
# Simple audio generation
result = generate_audio_simple(
    prompt="electronic dance music like grimes, upbeat tempo, dreamy synths"
)

# Advanced audio generation with parameters
result = generate_audio_simple(
    prompt="ambient forest sounds with gentle rain and birds",
    negative_prompt="distorted, low quality, silence, harsh noise",
    duration=60.0,  # 60 seconds
    steps=50,       # Higher quality
    cfg=4.98,       # Creativity vs adherence 
    seed=12345      # Reproducible results
)
```

### Step 3: Check Status and Get URLs

```python
# Check if audio generation is complete
status = get_audio_status_simple(prompt_id)

if status['success'] and status['status'] == 'completed':
    audio_urls = status['audio_urls']  # Browser-accessible URLs!
    print(f"Audio ready: {audio_urls[0]}")

# Or wait for completion automatically
result = wait_for_audio_completion(prompt_id, max_wait=300)
```

## 🎨 Example ElizaOS Agent Function

Here's how you can create an audio generation function for your ElizaOS agent:

```python
def generate_audio_agent(prompt: str, **kwargs):
    """
    ElizaOS agent function to generate audio using ComfyUI Stable Audio Open.
    
    Args:
        prompt: The audio description
        **kwargs: Optional parameters (negative_prompt, duration, steps, etc.)
    
    Returns:
        Dict with status and audio URLs
    """
    try:
        # Check if ComfyUI is running
        from simple_audio_client import check_comfyui_status
        status = check_comfyui_status()
        if status['status'] != 'success':
            return {
                "error": "ComfyUI is not running",
                "details": status['message']
            }
        
        # Generate the audio
        result = generate_audio_simple(prompt, **kwargs)
        
        if result['success']:
            # Wait for completion (optional)
            completion = wait_for_audio_completion(
                result['prompt_id'], 
                max_wait=kwargs.get('max_wait', 300)
            )
            
            if completion['success'] and completion['status'] == 'completed':
                return {
                    "success": True,
                    "message": f"Audio generated: {prompt}",
                    "audio_urls": completion['audio_urls'],
                    "duration": kwargs.get('duration', 30.0),
                    "prompt_id": result['prompt_id']
                }
            else:
                return {
                    "success": True,
                    "message": f"Audio generation started: {prompt}",
                    "prompt_id": result['prompt_id'],
                    "status": "generating",
                    "note": "Check status later for URLs"
                }
        else:
            return {
                "error": "Failed to generate audio",
                "details": result.get('error', 'Unknown error')
            }
            
    except Exception as e:
        return {
            "error": "Exception occurred",
            "details": str(e)
        }
```

## 📋 Available Parameters

When calling `generate_audio_simple()`, you can use these parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `prompt` | Required | The audio description |
| `negative_prompt` | `"distorted, low quality, silence"` | Things to avoid in the audio |
| `duration` | `30.0` | Audio duration in seconds |
| `steps` | `50` | Sampling steps (higher = better quality, slower) |
| `cfg` | `4.98` | CFG scale (higher = more prompt adherence) |
| `seed` | `-1` | Random seed (-1 for random) |

## 🎼 Audio Workflow Details

Your audio workflow uses:
- **Model**: `stable-audio-open-1.0.safetensors` (local Stable Audio Open)
- **Text Encoder**: `t5-base.safetensors` with stable_audio type
- **Sampler**: dpmpp_3m_sde_gpu with exponential scheduler
- **Steps**: 50 (configurable)
- **Duration**: 30-60 seconds (configurable)
- **Output Format**: WAV files
- **Output Directory**: `audio/` subdirectory

## 📁 Output Location

Generated audio files are saved to:
- **Directory**: `output/audio/`
- **Filename format**: `ElizaOS_[prompt]_[timestamp].wav`
- **Example**: `ElizaOS_electronic dance music like_00001_.wav`
- **URL Format**: `http://localhost:8188/view?filename=ElizaOS_electronic dance music like_00001_.wav&subfolder=audio&type=output`

## 🎯 Example Usage Scenarios

### Scenario 1: Background Music
```python
result = generate_audio_simple(
    prompt="calm ambient background music, soft piano and strings",
    duration=120.0,  # 2 minutes
    steps=60         # High quality
)
```

### Scenario 2: Sound Effects
```python
result = generate_audio_simple(
    prompt="epic battle sound effects, swords clashing, magical spells",
    negative_prompt="music, melody, singing",
    duration=15.0,   # Short sound effect
    steps=40
)
```

### Scenario 3: Musical Composition
```python
result = generate_audio_simple(
    prompt="electronic dance music like grimes, upbeat tempo, dreamy synths, 4/4 beat",
    negative_prompt="distorted, low quality, silence",
    duration=90.0,   # Full track length
    cfg=5.5,         # Higher adherence to prompt
    seed=42          # Reproducible result
)
```

### Scenario 4: Nature Sounds
```python
result = generate_audio_simple(
    prompt="peaceful forest ambience, gentle rain, distant thunder, birds chirping",
    duration=300.0,  # 5 minutes of ambience
    steps=45
)
```

## 🔄 Workflow Integration

You can integrate audio generation with your existing image workflows:

```python
# Generate image and matching audio
image_result = generate_image_with_flux("A cyberpunk cityscape at night")
audio_result = generate_audio_simple("cyberpunk electronic music, dark atmospheric synths")

# Both will have browser-accessible URLs
print(f"Image: {image_result['image_urls']}")
print(f"Audio: {audio_result['audio_urls']}")
```

## 🐛 Troubleshooting

### ComfyUI Not Running
```bash
# Start ComfyUI
./start_comfyui_api.sh
```

### Missing Models
Ensure you have these files in your ComfyUI models directory:
- `models/checkpoints/stable-audio-open-1.0.safetensors`
- `models/clip/t5-base.safetensors`

### Check Status
```python
from simple_audio_client import check_comfyui_status
status = check_comfyui_status()
print(status)
```

### Check Audio Queue
```python
from simple_audio_client import get_comfyui_queue
queue = get_comfyui_queue()
print(queue)
```

## ✅ Success Indicators

You'll know everything is working when:
1. `check_comfyui_status()` returns `{"status": "success"}`
2. `generate_audio_simple()` returns a `prompt_id`
3. Audio files appear in the `output/audio/` directory
4. `audio_urls` in responses start with `http://localhost:8188`
5. You can play audio files directly from the browser URLs
6. No error messages in the response

## 🎵 Testing Your Setup

```bash
# Test the audio generation
python simple_audio_client.py

# Test a quick generation
python -c "
from simple_audio_client import generate_audio_simple, wait_for_audio_completion
result = generate_audio_simple('electronic music', duration=10.0, steps=25)
if result['success']:
    completion = wait_for_audio_completion(result['prompt_id'], max_wait=120)
    print(f'Audio URLs: {completion.get(\"audio_urls\", [])}')
"
```

## 🌟 Key Benefits

1. **✅ Browser Accessible**: All audio URLs work from your `localhost:3001` interface
2. **✅ No API Tokens**: Uses local Stable Audio Open model, no external services
3. **✅ High Quality**: Professional audio generation with configurable parameters
4. **✅ Flexible Duration**: Generate anything from short sound effects to long compositions
5. **✅ Status Tracking**: Real-time generation status with queue position
6. **✅ Recent Audio**: Easy access to previously generated audio files
7. **✅ Multiple Formats**: Supports various audio generation scenarios

## 🎯 Audio Generation States

| Status | Description | Audio URLs Available |
|--------|-------------|---------------------|
| `pending` | In queue waiting | ❌ No |
| `running` | Currently generating | ❌ No |
| `completed` | Generation finished | ✅ Yes |
| `timeout` | Took too long | ❌ Check manually |
| `unknown` | Error or cancelled | ❌ No |

---

**🎉 You're all set!** Your ElizaOS system can now generate high-quality audio using local ComfyUI workflows with Stable Audio Open, providing browser-accessible URLs that work from your `localhost:3001` interface alongside your existing image generation capabilities!

## 📚 Quick Reference

```python
# Generate audio
from simple_audio_client import generate_audio_simple
result = generate_audio_simple("your prompt here")

# Check status
from simple_audio_client import get_audio_status_simple
status = get_audio_status_simple(prompt_id)

# Get recent audio
from simple_audio_client import get_recent_audio_simple
recent = get_recent_audio_simple(limit=5)

# Wait for completion
from simple_audio_client import wait_for_audio_completion
final = wait_for_audio_completion(prompt_id)
``` 