from .nodes import ParlerTTSNode, PreViewAudio

NODE_CLASS_MAPPINGS = {
    "ParlerTTSNode": ParlerTTSNode,
    "PreViewAudio": PreViewAudio,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ParlerTTSNode": "Parler-TTS Generator",
    "PreViewAudio": "Preview Audio",
}

# Add to Python path if needed
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir) 