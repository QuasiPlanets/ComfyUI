# ComfyUI Developer Guide

*A comprehensive guide for developing, debugging, and maintaining ComfyUI custom nodes*

---

## Table of Contents

1. [Overview](#overview)
2. [ComfyUI Architecture](#comfyui-architecture)
3. [Custom Node Development](#custom-node-development)
4. [Common Issues & Solutions](#common-issues--solutions)
5. [Best Practices](#best-practices)
6. [Debugging Techniques](#debugging-techniques)
7. [Security Considerations](#security-considerations)
8. [Testing Strategies](#testing-strategies)
9. [Troubleshooting Checklist](#troubleshooting-checklist)

---

## Overview

ComfyUI is a powerful, node-based interface for AI workflows. This guide provides practical knowledge for developing custom nodes, solving common issues, and maintaining ComfyUI installations based on real-world development experience.

### Key Principles
- **Minimal Changes**: Make the smallest change necessary to solve the problem
- **Security First**: Always consider security implications, especially with model loading
- **Documentation**: Document why changes were made, not just what changed
- **Testing**: Verify changes work in both isolated and integrated environments

---

## ComfyUI Architecture

### Directory Structure
```
ComfyUI/
├── main.py                 # Entry point
├── nodes.py               # Core nodes
├── execution.py           # Workflow execution engine
├── server.py             # Web server
├── custom_nodes/         # Custom node directory
│   └── YourCustomNode/
│       ├── __init__.py   # Node registration
│       ├── nodes.py      # Node implementations
│       └── requirements.txt
├── models/               # Model storage
├── input/               # Input files
├── output/              # Generated outputs
└── user/                # User data and configs
```

### Custom Node Structure
```python
# __init__.py - Node registration
NODE_CLASS_MAPPINGS = {
    "YourNodeName": YourNodeClass
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YourNodeName": "Human Readable Name"
}

# nodes.py - Node implementation
class YourNodeClass:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"input_name": ("INPUT_TYPE",)}}
    
    RETURN_TYPES = ("OUTPUT_TYPE",)
    FUNCTION = "your_function"
    CATEGORY = "category/subcategory"
    
    def your_function(self, input_name):
        # Node logic here
        return (result,)
```

### Import Path Management
Custom nodes often need to add directories to Python's import path:

```python
# In __init__.py
import sys
import os

now_dir = os.path.dirname(os.path.abspath(__file__))
if now_dir not in sys.path:
    sys.path.append(now_dir)
    sys.path.append(os.path.join(now_dir, "subdirectory"))
```

---

## Custom Node Development

### Essential Components

#### 1. Node Class Structure
```python
class ExampleNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "Hello World"}),
                "number": ("INT", {"default": 1, "min": 0, "max": 100}),
                "choice": (["option1", "option2"], {"default": "option1"})
            },
            "optional": {
                "optional_input": ("FLOAT", {"default": 1.0})
            }
        }
    
    RETURN_TYPES = ("STRING", "INT")
    OUTPUT_NODE = False  # Set to True if this is an output node
    FUNCTION = "process"
    CATEGORY = "custom/example"
    
    def process(self, text, number, choice, optional_input=1.0):
        # Your processing logic here
        result_text = f"{text} - {choice}"
        result_number = number * int(optional_input)
        return (result_text, result_number)
```

#### 2. Error Handling
```python
def process(self, inputs):
    try:
        # Your logic here
        return (result,)
    except Exception as e:
        print(f"Error in {self.__class__.__name__}: {e}")
        raise e  # Re-raise to show in ComfyUI interface
```

#### 3. Resource Management
```python
def process(self, inputs):
    try:
        # Load resources
        model = load_model()
        result = model.process(inputs)
        return (result,)
    finally:
        # Clean up resources
        if 'model' in locals():
            del model
        import gc
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
```

### File Organization Best Practices

1. **Separate concerns**: Keep node definitions, utility functions, and model handling in separate files
2. **Use meaningful names**: Node names should clearly indicate their purpose
3. **Group related nodes**: Use consistent category naming for related functionality
4. **Handle dependencies**: Include comprehensive `requirements.txt` files

---

## Common Issues & Solutions

### 1. PyTorch 2.6+ Weights Loading Error

**Problem**: `WeightsUnpickler error: Unsupported global` when loading models

**Root Cause**: PyTorch 2.6+ changed default `weights_only=True` for security

**Solutions**:

#### Option 1: Set weights_only=False (Recommended for trusted models)
```python
# For trusted models from known sources (e.g., Hugging Face)
checkpoint = torch.load(model_path, map_location="cpu", weights_only=False)
```

#### Option 2: Allowlist specific classes (More complex but more secure)
```python
from your.model.config import YourConfigClass
import torch.serialization

# Allowlist specific classes
with torch.serialization.safe_globals([YourConfigClass]):
    checkpoint = torch.load(model_path, map_location="cpu", weights_only=True)
```

**Best Practice**: Use Option 1 for models from trusted sources (Hugging Face, official repositories) with clear documentation explaining why it's safe.

### 2. Permission Errors

**Problem**: `PermissionError` when trying to write to system directories

**Solution**: 
```python
# Instead of writing to system site-packages
import sys
sys.path.append(your_custom_path)  # Runtime path addition
```

### 3. Import Failures

**Problem**: Custom modules not found

**Solutions**:
```python
# Method 1: Add to sys.path in __init__.py
now_dir = os.path.dirname(os.path.abspath(__file__))
if now_dir not in sys.path:
    sys.path.append(now_dir)

# Method 2: Relative imports
from .your_module import YourClass

# Method 3: Explicit path handling
import importlib.util
spec = importlib.util.spec_from_file_location("module_name", "/path/to/module.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
```

### 4. Node Registration Issues

**Problem**: Nodes not appearing in ComfyUI interface

**Checklist**:
1. Verify `NODE_CLASS_MAPPINGS` is correctly defined
2. Check that `__init__.py` is present and imports correctly
3. Ensure no syntax errors in node classes
4. Confirm `INPUT_TYPES` method is properly implemented
5. Restart ComfyUI after changes

---

## Best Practices

### Code Modification Guidelines

1. **Understand before changing**: Read the existing code to understand its purpose
2. **Minimal intervention**: Make the smallest change that solves the problem
3. **Document changes**: Add comments explaining why changes were made
4. **Test thoroughly**: Verify changes work in isolation and integration
5. **Consider side effects**: Think about how changes might affect other parts

### Security Best Practices

1. **Model Source Verification**: Only use `weights_only=False` for trusted model sources
2. **Path Validation**: Validate file paths before operations
3. **Input Sanitization**: Sanitize user inputs, especially file paths and text
4. **Error Information**: Don't expose sensitive paths or information in error messages

### Performance Optimization

1. **Lazy Loading**: Load models and resources only when needed
2. **Memory Management**: Clean up resources after use
3. **Caching**: Cache expensive operations when appropriate
4. **GPU Memory**: Use `torch.cuda.empty_cache()` after GPU operations

### Error Handling

```python
def robust_node_function(self, inputs):
    try:
        # Validate inputs
        if not inputs:
            raise ValueError("No inputs provided")
        
        # Main logic
        result = process_inputs(inputs)
        
        # Validate outputs
        if result is None:
            raise RuntimeError("Processing failed to produce result")
            
        return (result,)
        
    except Exception as e:
        # Log error with context
        import traceback
        error_msg = f"Error in {self.__class__.__name__}: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        
        # Re-raise for ComfyUI to handle
        raise RuntimeError(error_msg) from e
```

---

## Debugging Techniques

### 1. ComfyUI Console Output

Monitor the console where ComfyUI is running for:
- Import errors during startup
- Runtime exceptions
- Custom print statements

### 2. Node Registration Verification

```python
# Check if nodes are registered
curl -s http://localhost:8188/object_info | python -c "
import sys, json
data = json.load(sys.stdin)
if 'YourNodeName' in data:
    print('✅ Node registered successfully')
else:
    print('❌ Node not found')
"
```

### 3. Import Testing

Create standalone test scripts:
```python
#!/usr/bin/env python3
import sys
sys.path.append('/path/to/custom_nodes/YourNode')

try:
    from your_module import YourClass
    print("✅ Import successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
```

### 4. Model Loading Testing

```python
def test_model_loading():
    try:
        model = load_your_model()
        print("✅ Model loaded successfully")
        
        # Test basic functionality
        result = model.simple_test()
        print(f"✅ Model test result: {result}")
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        if 'model' in locals():
            del model
        import gc
        gc.collect()
```

### 5. Log File Analysis

Check ComfyUI logs:
```bash
# Monitor real-time logs
tail -f /workspace/user/comfyui.log

# Search for specific errors
grep -i "error\|exception\|failed" /workspace/user/comfyui.log
```

---

## Security Considerations

### Model Loading Security

When dealing with PyTorch model loading:

```python
def safe_model_loading(model_path, trusted_source=False):
    """
    Load PyTorch model with appropriate security settings
    
    Args:
        model_path: Path to model file
        trusted_source: True if model is from trusted source (e.g., Hugging Face)
    """
    if trusted_source:
        # For trusted sources, document why it's safe
        # Safe because: Model from Hugging Face coqui/XTTS-v2 repository
        return torch.load(model_path, map_location="cpu", weights_only=False)
    else:
        # For untrusted sources, use allowlisting
        from your.trusted.config import YourConfigClass
        with torch.serialization.safe_globals([YourConfigClass]):
            return torch.load(model_path, map_location="cpu", weights_only=True)
```

### File Path Security

```python
import os
import os.path

def validate_file_path(file_path, allowed_dirs):
    """Validate file path is within allowed directories"""
    real_path = os.path.realpath(file_path)
    for allowed_dir in allowed_dirs:
        if real_path.startswith(os.path.realpath(allowed_dir)):
            return True
    return False

# Usage
if not validate_file_path(user_input_path, [input_dir, models_dir]):
    raise ValueError("File path not allowed")
```

---

## Testing Strategies

### 1. Unit Testing Custom Nodes

```python
import unittest
import sys
import os

# Add your custom node to path
sys.path.append('/path/to/custom_nodes/YourNode')
from your_node import YourNodeClass

class TestYourNode(unittest.TestCase):
    def setUp(self):
        self.node = YourNodeClass()
    
    def test_input_types(self):
        input_types = self.node.INPUT_TYPES()
        self.assertIn("required", input_types)
        self.assertIn("your_input", input_types["required"])
    
    def test_basic_functionality(self):
        result = self.node.your_function("test_input")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)

if __name__ == "__main__":
    unittest.main()
```

### 2. Integration Testing

```python
def test_comfyui_integration():
    """Test that node works within ComfyUI environment"""
    import requests
    import json
    
    # Test node registration
    response = requests.get("http://localhost:8188/object_info")
    nodes = response.json()
    
    assert "YourNodeName" in nodes, "Node not registered"
    
    # Test workflow execution (if you have a test workflow)
    workflow = {
        # Your test workflow JSON
    }
    
    response = requests.post("http://localhost:8188/prompt", 
                           json={"prompt": workflow})
    assert response.status_code == 200
```

### 3. Performance Testing

```python
import time
import psutil
import torch

def performance_test():
    """Test node performance and memory usage"""
    node = YourNodeClass()
    
    # Memory usage before
    memory_before = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    gpu_memory_before = torch.cuda.memory_allocated() / 1024 / 1024 if torch.cuda.is_available() else 0
    
    # Time the operation
    start_time = time.time()
    result = node.your_function("test_input")
    end_time = time.time()
    
    # Memory usage after
    memory_after = psutil.Process().memory_info().rss / 1024 / 1024
    gpu_memory_after = torch.cuda.memory_allocated() / 1024 / 1024 if torch.cuda.is_available() else 0
    
    print(f"Execution time: {end_time - start_time:.2f}s")
    print(f"Memory usage: {memory_after - memory_before:.2f}MB")
    print(f"GPU memory: {gpu_memory_after - gpu_memory_before:.2f}MB")
    
    return result
```

---

## Troubleshooting Checklist

### Node Not Appearing in ComfyUI

- [ ] `__init__.py` exists and contains `NODE_CLASS_MAPPINGS`
- [ ] Node class has required methods (`INPUT_TYPES`, `FUNCTION`)
- [ ] No syntax errors in Python files
- [ ] ComfyUI restarted after adding/modifying nodes
- [ ] Check console for import errors

### Import Errors

- [ ] Required dependencies installed (`pip install -r requirements.txt`)
- [ ] Python path correctly set in `__init__.py`
- [ ] All required files present
- [ ] File permissions correct
- [ ] No circular imports

### Model Loading Issues

- [ ] Model files exist in expected locations
- [ ] Correct PyTorch version compatibility
- [ ] Sufficient disk space and memory
- [ ] Proper `weights_only` parameter handling
- [ ] Network connectivity for downloading models

### Runtime Errors

- [ ] Input validation implemented
- [ ] Error handling in place
- [ ] Resource cleanup (memory, GPU)
- [ ] Dependencies compatible
- [ ] File paths exist and accessible

### Performance Issues

- [ ] Memory leaks (check with `torch.cuda.memory_summary()`)
- [ ] Inefficient operations in hot paths
- [ ] Large models loaded multiple times
- [ ] GPU memory not being freed

---

## Example: Complete Custom Node

Here's a complete example incorporating all best practices:

```python
# nodes.py
import os
import torch
import folder_paths
from typing import Tuple, Any

class ExampleTTSNode:
    """
    Example TTS node demonstrating best practices
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "Hello, world!"}),
                "model_name": (["model1", "model2"], {"default": "model1"}),
                "speed": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 3.0, "step": 0.1}),
            },
            "optional": {
                "voice_file": ("AUDIOPATH",),
            }
        }
    
    RETURN_TYPES = ("AUDIOPATH",)
    RETURN_NAMES = ("audio",)
    FUNCTION = "generate_speech"
    CATEGORY = "audio/tts"
    DESCRIPTION = "Generate speech from text using TTS models"
    
    def __init__(self):
        self.models = {}  # Cache loaded models
    
    def generate_speech(self, text: str, model_name: str, speed: float, 
                       voice_file: str = None) -> Tuple[str]:
        """
        Generate speech from text
        
        Args:
            text: Input text to synthesize
            model_name: Name of TTS model to use
            speed: Speech speed multiplier
            voice_file: Optional voice reference file
            
        Returns:
            Tuple containing path to generated audio file
        """
        try:
            # Validate inputs
            if not text.strip():
                raise ValueError("Text input cannot be empty")
            
            if speed <= 0:
                raise ValueError("Speed must be positive")
            
            # Load model (with caching)
            model = self._load_model(model_name)
            
            # Generate speech
            audio_path = self._synthesize_speech(model, text, speed, voice_file)
            
            return (audio_path,)
            
        except Exception as e:
            error_msg = f"Error in {self.__class__.__name__}: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            raise RuntimeError(error_msg) from e
    
    def _load_model(self, model_name: str):
        """Load and cache TTS model"""
        if model_name not in self.models:
            model_path = os.path.join("models", "tts", f"{model_name}.pth")
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model not found: {model_path}")
            
            try:
                # Use weights_only=False for trusted models with documentation
                # Safe because: Model from trusted source (Hugging Face repository)
                checkpoint = torch.load(model_path, map_location="cpu", weights_only=False)
                
                model = self._create_model_from_checkpoint(checkpoint)
                self.models[model_name] = model
                
                print(f"Loaded model: {model_name}")
                
            except Exception as e:
                raise RuntimeError(f"Failed to load model {model_name}: {e}")
        
        return self.models[model_name]
    
    def _create_model_from_checkpoint(self, checkpoint):
        """Create model instance from checkpoint"""
        # Model creation logic here
        pass
    
    def _synthesize_speech(self, model, text: str, speed: float, 
                          voice_file: str = None) -> str:
        """Synthesize speech and return output path"""
        try:
            # Speech synthesis logic here
            output_dir = folder_paths.get_output_directory()
            output_path = os.path.join(output_dir, f"tts_{hash(text)}.wav")
            
            # Generate and save audio
            # ... synthesis code ...
            
            return output_path
            
        finally:
            # Cleanup GPU memory
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
    
    def __del__(self):
        """Cleanup when node is destroyed"""
        for model in self.models.values():
            del model
        
        import gc
        gc.collect()
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


# __init__.py
from .nodes import ExampleTTSNode

NODE_CLASS_MAPPINGS = {
    "ExampleTTSNode": ExampleTTSNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ExampleTTSNode": "Example TTS Generator",
}

# Add to Python path if needed
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
```

---

## Conclusion

This guide represents practical knowledge gained from real ComfyUI development work. The key to successful ComfyUI development is:

1. **Understanding the architecture** and working with it, not against it
2. **Making minimal, targeted changes** that solve specific problems
3. **Prioritizing security** while maintaining functionality
4. **Testing thoroughly** in both isolated and integrated environments
5. **Documenting decisions** especially around security trade-offs

Remember: ComfyUI is a powerful platform, but with power comes responsibility. Always consider the security implications of your changes, especially when dealing with model loading and file operations.

For the most up-to-date information, always refer to the official ComfyUI documentation and community resources. 