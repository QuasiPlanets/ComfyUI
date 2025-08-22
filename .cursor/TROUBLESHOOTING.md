# ComfyUI WhisperX Troubleshooting Guide

## Quick Diagnosis Commands

### System Health Check
```bash
# Check CUDA availability
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# Check GPU memory
nvidia-smi

# Check cuDNN libraries
ls -la /usr/lib/x86_64-linux-gnu/libcudnn*

# Check Python packages
pip list | grep -E "(torch|whisperx|numpy|pandas)"
```

### Component Verification
```bash
# Test WhisperX
python -c "import whisperx; print('WhisperX OK')"

# Test TTS
python -c "import TTS; print('TTS OK')"

# Test all custom nodes
python -c "import sys; sys.path.append('custom_nodes'); import ComfyUI_WhisperX; print('WhisperX node OK')"
```

## Common Issues and Solutions

### 1. cuDNN Library Errors

#### Problem: `Could not load library libcudnn_ops_infer.so.8`
**Symptoms**:
- WhisperX crashes during post-processing
- Error: `libcudnn_ops_infer.so.8: cannot open shared object file`
- Transcription works but crashes on completion

**Root Cause**:
- PyTorch uses bundled cuDNN 9.x
- WhisperX seeks system cuDNN 8.x
- Missing system cuDNN libraries

**Solution**:
```bash
# Install system cuDNN 8.9.3
sudo apt-get update
sudo apt-get install -y libcudnn8=8.9.*-1+cuda12.1 libcudnn8-dev=8.9.*-1+cuda12.1

# Verify installation
ls -la /usr/lib/x86_64-linux-gnu/libcudnn*
```

**Prevention**:
- Include cuDNN installation in Dockerfile
- Set proper LD_LIBRARY_PATH environment variables

#### Problem: cuDNN version mismatch
**Symptoms**:
- Different cuDNN versions causing conflicts
- Inconsistent behavior across components

**Solution**:
```bash
# Check current cuDNN versions
find /usr -name "libcudnn*" 2>/dev/null
find /usr/local -name "libcudnn*" 2>/dev/null

# Set environment variables
export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
```

### 2. NumPy Version Conflicts

#### Problem: `ModuleNotFoundError: No module named 'numpy.dtypes'`
**Symptoms**:
- ComfyUI fails to start
- NumPy import errors
- Custom nodes fail to load

**Root Cause**:
- NumPy version too old for ComfyUI
- Incompatible with newer packages

**Solution**:
```bash
# Upgrade to compatible NumPy version
pip install numpy==1.26.4

# Verify compatibility
python -c "import numpy; print(numpy.__version__)"
```

#### Problem: TTS NumPy compatibility
**Symptoms**:
- TTS framework fails to import
- Error: `TTS requires numpy==1.22.0`

**Solution**:
```bash
# Use compatible NumPy version
pip install numpy==1.26.4  # Works with TTS 0.22.0
```

### 3. Dependency Conflicts

#### Problem: Pandas version conflicts
**Symptoms**:
- TTS compatibility issues
- Error: `pandas<2.0,>=1.4 required`

**Solution**:
```bash
# Install compatible Pandas version
pip install pandas==1.5.3
```

#### Problem: SciPy version conflicts
**Symptoms**:
- NumPy compatibility issues
- Error: `scipy requires numpy<2.5,>=1.23.5`

**Solution**:
```bash
# Install compatible SciPy version
pip install scipy==1.11.4
```

### 4. GPU Memory Issues

#### Problem: Out of GPU memory
**Symptoms**:
- CUDA out of memory errors
- High GPU memory usage
- System slowdown

**Solutions**:
```python
# Clear GPU cache
import torch
torch.cuda.empty_cache()

# Monitor GPU memory
import torch
print(f"GPU Memory: {torch.cuda.memory_allocated() / 1024**2:.1f}MB")
```

**Optimization Techniques**:
- Use smaller WhisperX models
- Implement lazy loading
- Optimize audio buffer sizes

### 5. WebSocket Connection Issues

#### Problem: WebSocket connection fails
**Symptoms**:
- Browser can't connect to ComfyUI
- Audio streaming not working
- Connection timeouts

**Diagnosis**:
```bash
# Check if server is running
curl -s http://localhost:8188 | head -n 5

# Check WebSocket port
netstat -tlnp | grep 8188
```

**Solutions**:
```python
# Verify WebSocket handler in server.py
# Ensure proper message handling
# Check CORS settings
```

#### Problem: Audio streaming issues
**Symptoms**:
- No audio received
- Audio quality problems
- Buffer overflow

**Solutions**:
- Check audio format (PCM, 16kHz, 16-bit)
- Verify buffer sizes
- Monitor audio levels

### 6. Custom Node Loading Issues

#### Problem: Custom nodes not loading
**Symptoms**:
- Nodes not appearing in ComfyUI
- Import errors in logs
- Missing functionality

**Diagnosis**:
```bash
# Check custom node directories
ls -la custom_nodes/

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

**Solutions**:
```bash
# Verify node registration
# Check __init__.py files
# Ensure proper imports
```

### 7. Performance Issues

#### Problem: Slow transcription
**Symptoms**:
- High latency
- CPU/GPU bottlenecks
- Poor real-time performance

**Optimizations**:
```python
# Use GPU acceleration
model = whisperx.load_model("large-v3", device="cuda")

# Optimize buffer size
BUFFER_SIZE = 1.5  # seconds

# Implement silence detection
RMS_THRESHOLD = 0.03
```

#### Problem: High resource usage
**Symptoms**:
- System slowdown
- Memory leaks
- CPU overload

**Solutions**:
- Monitor resource usage
- Implement proper cleanup
- Use efficient data structures

### 8. ElizaOS Integration Issues

#### Problem: Connection instability
**Symptoms**:
- Intermittent disconnections
- Audio quality degradation
- Response delays

**Solutions**:
- Implement connection pooling
- Add retry logic
- Monitor connection health

#### Problem: Audio quality issues
**Symptoms**:
- Poor audio fidelity
- Noise in transcription
- Inconsistent results

**Solutions**:
- Optimize audio processing
- Implement noise reduction
- Use higher quality audio formats

## Advanced Troubleshooting

### Debug Mode
```bash
# Enable verbose logging
export CT2_VERBOSE=1
export CT2_FORCE_CPU_ISA=AVX2
export CT2_USE_MKL=1

# Start with debug output
python main.py --listen 0.0.0.0 --port 8188 --enable-cors-header --debug
```

### Memory Profiling
```python
# Monitor GPU memory
import torch
print(f"Allocated: {torch.cuda.memory_allocated() / 1024**2:.1f}MB")
print(f"Cached: {torch.cuda.memory_reserved() / 1024**2:.1f}MB")
```

### Performance Profiling
```python
# Profile transcription performance
import time
start_time = time.time()
# ... transcription code ...
print(f"Time: {time.time() - start_time:.2f}s")
```

## Prevention Strategies

### 1. Dependency Management
- Pin all versions in requirements.txt
- Use virtual environments
- Regular dependency audits

### 2. Environment Consistency
- Use Docker containers
- Standardize CUDA/cuDNN versions
- Consistent Python versions

### 3. Monitoring
- Implement health checks
- Monitor resource usage
- Log error conditions

### 4. Testing
- Automated testing
- Load testing
- Compatibility testing

## Emergency Procedures

### Complete Reset
```bash
# Stop all services
docker-compose down

# Clear all caches
rm -rf __pycache__/
rm -rf .venv/
rm -rf models/

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

### Rollback to Previous Version
```bash
# Restore from backup
cp .devcontainer/Dockerfile.backup .devcontainer/Dockerfile

# Rebuild container
docker-compose build
docker-compose up -d
```

### Data Recovery
```bash
# Backup important data
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz \
    custom_nodes/ \
    requirements.txt \
    .devcontainer/
```

## Support Resources

### Documentation
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- [DEVELOPMENT_HISTORY.md](DEVELOPMENT_HISTORY.md)
- [CUSTOM_NODES_GUIDE.md](CUSTOM_NODES_GUIDE.md)

### Log Files
- `server.log`: ComfyUI server logs
- `whisperx.log`: WhisperX specific logs
- Docker logs: `docker-compose logs`

### Community Resources
- ComfyUI GitHub issues
- WhisperX documentation
- CUDA/cuDNN compatibility matrix

This troubleshooting guide should cover most common issues and provide effective solutions for maintaining a stable ComfyUI WhisperX environment.


