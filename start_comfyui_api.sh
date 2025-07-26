#!/bin/bash

# Start ComfyUI with API configuration for external container access
echo "Starting ComfyUI with API configuration..."
echo "Server will be accessible at: http://0.0.0.0:8188"
echo "CORS enabled for cross-origin requests"

python main.py --listen 0.0.0.0 --port 8188 --enable-cors-header 