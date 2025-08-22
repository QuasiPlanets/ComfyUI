# WhisperX Custom Node Troubleshooting Guide

## Quick Diagnosis

### System Health Check
```bash
# Check CUDA availability
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# Check GPU memory
nvidia-smi

# Check cuDNN libraries
ls -la /usr/lib/x86_64-linux-gnu/libcudnn*

# Check WhisperX installation
python -c "import whisperx; print('WhisperX OK')"

# Check node registration
python -c "import sys; sys.path.append('custom_nodes'); import ComfyUI_WhisperX; print('Node OK')"
```

## Common Issues and Solutions

### 1. Node Not Appearing in ComfyUI

#### Problem
WhisperX node doesn't appear in the ComfyUI node list.

#### Symptoms
- Node not visible in node browser
- No WhisperX category in ComfyUI
- Import errors in console

#### Solutions

**Check Node Registration**:
```python
# Verify __init__.py contains proper registration
from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
```

**Check File Structure**:
```bash
# Verify correct directory structure
ls -la custom_nodes/ComfyUI-WhisperX/
# Should contain: __init__.py, nodes.py, requirements.txt
```

**Restart ComfyUI**:
```bash
# Stop ComfyUI and restart
# The node should appear after restart
```

**Check Python Path**:
```python
# Verify custom_nodes is in Python path
import sys
print('custom_nodes' in sys.path)
```

### 2. cuDNN Library Errors

#### Problem
`Could not load library libcudnn_ops_infer.so.8`

#### Symptoms
- WhisperX crashes during post-processing
- Error: `libcudnn_ops_infer.so.8: cannot open shared object file`
- Transcription works but crashes on completion

#### Root Cause
- PyTorch uses bundled cuDNN 9.x
- WhisperX seeks system cuDNN 8.x
- Missing system cuDNN libraries

#### Solutions

**Install System cuDNN**:
```bash
# Install cuDNN 8.9.3 for CUDA 12.1
sudo apt-get update
sudo apt-get install -y libcudnn8=8.9.*-1+cuda12.1 libcudnn8-dev=8.9.*-1+cuda12.1

# Verify installation
ls -la /usr/lib/x86_64-linux-gnu/libcudnn*
```

**Set Environment Variables**:
```bash
# Add to ~/.bashrc or environment
export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
export CUDNN_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu
```

**Verify Installation**:
```bash
# Check if libraries are accessible
python -c "import whisperx; print('WhisperX with cuDNN OK')"
```

### 3. GPU Memory Issues

#### Problem
CUDA out of memory errors during transcription.

#### Symptoms
- `CUDA out of memory` errors
- High GPU memory usage
- System slowdown during transcription

#### Solutions

**Clear GPU Cache**:
```python
import torch
torch.cuda.empty_cache()
```

**Use Smaller Model**:
```python
# Change model size in node configuration
model_size = "base"  # Instead of "large-v3"
```

**Optimize Memory Usage**:
```python
# Use float16 precision
compute_type = "float16"

# Reduce buffer size
buffer_size = 1.0  # Instead of 1.5
```

**Monitor Memory Usage**:
```python
# Check GPU memory
import torch
print(f"Allocated: {torch.cuda.memory_allocated() / 1024**2:.1f}MB")
print(f"Cached: {torch.cuda.memory_reserved() / 1024**2:.1f}MB")
```

### 4. Audio Processing Issues

#### Problem
Poor transcription quality or no transcription results.

#### Symptoms
- Empty transcription results
- Poor accuracy
- Audio not being processed

#### Solutions

**Check Audio Format**:
```python
# Verify audio specifications
SAMPLE_RATE = 16000      # Hz
CHANNELS = 1             # Mono
FORMAT = "PCM"           # Pulse Code Modulation
BIT_DEPTH = 16           # bits per sample
```

**Optimize Audio Quality**:
```python
# Normalize audio
def normalize_audio(audio_data):
    if np.max(np.abs(audio_data)) > 0:
        return audio_data / np.max(np.abs(audio_data))
    return audio_data

# Resample if needed
import librosa
if sample_rate != 16000:
    audio_data = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=16000)
```

**Adjust Silence Detection**:
```python
# Modify RMS threshold
rms_threshold = 0.01  # More sensitive (default: 0.03)
```

**Check Audio Buffer**:
```python
# Verify buffer size
buffer_size = 1.5  # seconds
min_buffer_samples = int(buffer_size * 16000)
```

### 5. WebSocket Connection Issues

#### Problem
WebSocket connection failures or audio streaming issues.

#### Symptoms
- Browser can't connect to ComfyUI
- Audio not being received
- Connection timeouts

#### Solutions

**Check Server Status**:
```bash
# Verify ComfyUI is running
curl -s http://localhost:8188 | head -n 5

# Check WebSocket port
netstat -tlnp | grep 8188
```

**Verify WebSocket Handler**:
```python
# Check if WebSocket handler is properly integrated
# Look for WhisperX message handling in server.py
```

**Test WebSocket Connection**:
```javascript
// Browser console test
const ws = new WebSocket('ws://localhost:8188');
ws.onopen = () => console.log('Connected');
ws.onerror = (e) => console.error('Error:', e);
```

**Check CORS Settings**:
```python
# Ensure CORS is enabled in ComfyUI
# Add --enable-cors-header flag when starting ComfyUI
```

### 6. Model Loading Issues

#### Problem
WhisperX models fail to load or load slowly.

#### Symptoms
- Long loading times
- Model loading errors
- Memory issues during loading

#### Solutions

**Check Model Cache**:
```bash
# Clear model cache if corrupted
rm -rf ~/.cache/huggingface/hub/models--Systran--faster-whisper-*

# Or clear entire cache
rm -rf ~/.cache/huggingface/
```

**Use Smaller Model**:
```python
# Start with smaller model for testing
model_size = "base"  # Faster loading
```

**Check Internet Connection**:
```bash
# Verify model download
curl -I https://huggingface.co/Systran/faster-whisper-large-v3
```

**Pre-download Models**:
```python
# Pre-download models to avoid runtime delays
import whisperx
model = whisperx.load_model("large-v3", device="cuda")
```

### 7. Performance Issues

#### Problem
Slow transcription or high latency.

#### Symptoms
- High end-to-end latency
- Slow processing
- Poor real-time performance

#### Solutions

**Optimize Model Settings**:
```python
# Use faster settings
model_size = "base"        # Faster model
compute_type = "float16"   # Faster precision
device = "cuda"           # GPU acceleration
```

**Optimize Buffer Settings**:
```python
# Reduce buffer size for lower latency
buffer_size = 1.0  # seconds (default: 1.5)

# Adjust silence detection
rms_threshold = 0.05  # Less sensitive (default: 0.03)
```

**Enable GPU Optimization**:
```python
# Ensure GPU optimization is enabled
torch.backends.cudnn.benchmark = True
torch.backends.cudnn.deterministic = False
```

**Monitor Performance**:
```python
import time

def measure_performance(func):
    start_time = time.time()
    result = func()
    duration = time.time() - start_time
    print(f"Duration: {duration:.2f}s")
    return result
```

### 8. Language Detection Issues

#### Problem
Incorrect language detection or poor transcription for non-English.

#### Symptoms
- Wrong language detected
- Poor transcription quality for non-English
- Language-specific errors

#### Solutions

**Force Language**:
```python
# Set specific language instead of auto-detection
language = "en"  # or "es", "fr", "de", etc.
```

**Use Language-Specific Model**:
```python
# Some models work better for specific languages
# large-v3 is generally good for all languages
model_size = "large-v3"
```

**Check Audio Quality**:
```python
# Ensure good audio quality for language detection
# Clear speech, minimal background noise
# Proper sample rate and format
```

**Test with Known Audio**:
```python
# Test with high-quality audio samples
# Verify language detection accuracy
```

## Advanced Troubleshooting

### Debug Mode

#### Enable Verbose Logging
```python
# Set environment variables for debugging
import os
os.environ['CT2_VERBOSE'] = '1'
os.environ['CT2_FORCE_CPU_ISA'] = 'AVX2'
os.environ['CT2_USE_MKL'] = '1'
```

#### Debug WebSocket Communication
```python
# Add debug logging to WebSocket handler
import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('whisperx_websocket')
logger.debug(f"Received message: {message}")
```

#### Debug Audio Processing
```python
# Add audio processing debug information
def debug_audio_processing(audio_data):
    print(f"Audio shape: {audio_data.shape}")
    print(f"Audio dtype: {audio_data.dtype}")
    print(f"Audio range: {np.min(audio_data)} to {np.max(audio_data)}")
    print(f"Audio RMS: {np.sqrt(np.mean(np.square(audio_data)))}")
```

### Performance Profiling

#### Memory Profiling
```python
import torch
import psutil

def profile_memory():
    gpu_memory = torch.cuda.memory_allocated() / 1024**2
    cpu_memory = psutil.Process().memory_info().rss / 1024**2
    
    print(f"GPU Memory: {gpu_memory:.1f}MB")
    print(f"CPU Memory: {cpu_memory:.1f}MB")
```

#### Timing Profiling
```python
import time
import functools

def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

@timing_decorator
def transcribe_audio(audio_data):
    # Transcription code
    pass
```

### Error Recovery

#### Automatic Retry
```python
import asyncio

async def retry_operation(operation, max_retries=3, delay=1.0):
    for attempt in range(max_retries):
        try:
            return await operation()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay * (2 ** attempt))
```

#### Graceful Degradation
```python
class GracefulWhisperX:
    def __init__(self):
        self.primary_model = "large-v3"
        self.fallback_model = "base"
    
    def transcribe_with_fallback(self, audio_data):
        try:
            return self.transcribe_audio(audio_data, model_size=self.primary_model)
        except Exception as e:
            print(f"Primary model failed: {e}")
            try:
                return self.transcribe_audio(audio_data, model_size=self.fallback_model)
            except Exception as e2:
                print(f"Fallback model also failed: {e2}")
                raise e2
```

## Prevention Strategies

### 1. Regular Maintenance
```bash
# Clear GPU cache regularly
python -c "import torch; torch.cuda.empty_cache()"

# Monitor disk space
df -h

# Check for updates
pip list --outdated
```

### 2. Environment Monitoring
```python
# Monitor system resources
import psutil
import torch

def monitor_system():
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    gpu_memory = torch.cuda.memory_allocated() / 1024**2
    
    print(f"CPU: {cpu_percent}%")
    print(f"Memory: {memory_percent}%")
    print(f"GPU Memory: {gpu_memory:.1f}MB")
```

### 3. Configuration Validation
```python
# Validate configuration on startup
def validate_config():
    # Check CUDA availability
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA not available")
    
    # Check cuDNN libraries
    import ctypes
    try:
        ctypes.CDLL("libcudnn_ops_infer.so.8")
    except OSError:
        raise RuntimeError("cuDNN libraries not found")
    
    # Check WhisperX installation
    try:
        import whisperx
    except ImportError:
        raise RuntimeError("WhisperX not installed")
```

## Emergency Procedures

### Complete Reset
```bash
# Stop all services
pkill -f "python.*main.py"

# Clear all caches
rm -rf __pycache__/
rm -rf ~/.cache/huggingface/
torch.cuda.empty_cache()

# Restart ComfyUI
python main.py --listen 0.0.0.0 --port 8188 --enable-cors-header
```

### Rollback to Previous Version
```bash
# Restore from backup
cp .devcontainer/Dockerfile.backup .devcontainer/Dockerfile

# Rebuild container
docker-compose build --no-cache
docker-compose up -d
```

### Data Recovery
```bash
# Backup important data
tar -czf whisperx_backup_$(date +%Y%m%d_%H%M%S).tar.gz \
    custom_nodes/ComfyUI-WhisperX/ \
    requirements.txt \
    .devcontainer/
```

This troubleshooting guide provides comprehensive solutions for common WhisperX custom node issues, ensuring optimal performance and reliability.


