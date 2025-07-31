# ComfyUI API Authentication Setup Guide

This guide will help you configure ComfyUI API authentication so that your ElizaOS system can use the API-based nodes (Kling, Luma, Flux, etc.) for image and video generation.

## 🔍 Current Status

Your ComfyUI instance is configured with API-based nodes that require authentication tokens. The nodes are available but need API keys to function.

## 🚀 Quick Setup

### Step 1: Get Your API Key

1. Go to [https://platform.comfy.org/login](https://platform.comfy.org/login)
2. Sign up or log in to your account
3. Navigate to your API keys section
4. Generate a new API key
5. Copy the API key (it will look like: `comfyui-87d01e28d*******************************************************`)

### Step 2: Configure the API Key

You have two options to configure your API key:

#### Option A: Environment Variable (Recommended)
```bash
export COMFY_ORG_API_KEY="your_actual_api_key_here"
```

#### Option B: Edit Configuration File
Edit `api_config.py` and replace the placeholder:
```python
COMFY_ORG_API_KEY = "your_actual_api_key_here"  # Replace with your actual API key
```

### Step 3: Restart ComfyUI

After setting the API key, restart ComfyUI:
```bash
# If using the startup script
./start_comfyui_api.sh

# Or manually
python main.py --listen 0.0.0.0 --port 8188 --enable-cors-header
```

### Step 4: Test the Configuration

Run the test script to verify everything is working:
```bash
python elizaos_comfyui_integration.py
```

## 🎯 Available Services

Once configured, you'll have access to these AI services:

### Video Generation
- **Kling**: Text-to-video, image-to-video, video effects, lip-sync
- **Luma**: Text-to-video, image-to-video
- **Pika**: Text-to-video, image-to-video
- **Pixverse**: Text-to-video, image-to-video
- **Runway**: Video generation

### Image Generation
- **Flux**: High-quality image generation
- **Stability AI**: Stable Diffusion models
- **Ideogram**: Text-to-image
- **Recraft**: Image generation

### Other Services
- **OpenAI**: Chat, image generation
- **Gemini**: Text generation
- **Minimax**: Video generation
- **Moonvalley**: Video generation

## 🔧 Integration with ElizaOS

The `elizaos_comfyui_integration.py` file provides helper functions that your ElizaOS LLM can use:

### Available Functions

```python
# Check if API is configured
status = check_comfyui_api_status()

# Generate videos
result = generate_video("A beautiful sunset", service="kling")
result = generate_video("A cat playing", service="luma")

# Generate images
result = generate_image("A majestic dragon", service="flux")

# Check queue status
queue = get_comfyui_queue()

# Get execution history
history = get_comfyui_history()
```

### Example ElizaOS Plugin Integration

In your ElizaOS plugin, you can import and use these functions:

```python
from elizaos_comfyui_integration import (
    check_comfyui_api_status,
    generate_video,
    generate_image,
    get_comfyui_queue
)

# Check if API is ready
status = check_comfyui_api_status()
if not status['configured']:
    # Handle unconfigured state
    pass

# Generate content
video_result = generate_video(
    prompt="A beautiful sunset over mountains",
    service="kling",
    negative_prompt="blurry, low quality"
)
```

## 🐛 Troubleshooting

### "Unauthorized: Please login first to use this node"

This error means the API key is not configured or invalid.

**Solutions:**
1. Verify your API key is correct
2. Check that the environment variable is set: `echo $COMFY_ORG_API_KEY`
3. Restart ComfyUI after setting the API key
4. Test with the configuration script: `python api_config.py`

### "Connection refused" or "Cannot connect to ComfyUI"

This means ComfyUI is not running or not accessible.

**Solutions:**
1. Start ComfyUI: `./start_comfyui_api.sh`
2. Check if it's running: `curl http://localhost:8188/queue`
3. Verify the port and network configuration

### API Key Not Working

**Solutions:**
1. Get a fresh API key from [https://platform.comfy.org/login](https://platform.comfy.org/login)
2. Check your account has sufficient credits/quota
3. Verify the API key format (should start with `comfyui-`)

## 📋 Testing Your Setup

Run these commands to test your configuration:

```bash
# 1. Check API configuration
python api_config.py

# 2. Test the integration
python elizaos_comfyui_integration.py

# 3. Test a simple workflow
python example_api_client.py
```

## 🔒 Security Notes

- Never commit API keys to version control
- Use environment variables for production deployments
- Rotate API keys regularly
- Monitor your API usage and costs

## 📞 Support

If you encounter issues:

1. Check the [ComfyUI documentation](https://docs.comfy.org/)
2. Visit the [ComfyUI community](https://github.com/comfyanonymous/ComfyUI)
3. Check your API key status at [https://platform.comfy.org/login](https://platform.comfy.org/login)

## ✅ Success Indicators

You'll know everything is working when:

1. `python api_config.py` shows "API configured successfully"
2. `python elizaos_comfyui_integration.py` runs without errors
3. You can generate content through the ElizaOS interface
4. No "Unauthorized" errors appear in ComfyUI

---

**Next Steps:** Once configured, your ElizaOS system will be able to generate images and videos using the latest AI models through ComfyUI's API nodes! 