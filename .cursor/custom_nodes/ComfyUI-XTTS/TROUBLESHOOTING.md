# XTTS Custom Node Troubleshooting Guide

## Quick Diagnosis

### Check Node Status
```bash
# Verify XTTS nodes are loaded in ComfyUI
python -c "from nodes import NODE_CLASS_MAPPINGS; xtts_nodes = [k for k in NODE_CLASS_MAPPINGS.keys() if 'XTTS' in k or 'AIFSH' in k]; print('XTTS nodes:', xtts_nodes)"
```

### Check PyTorch Version
```bash
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"
```

## Common Issues

### 1. PyTorch 2.6+ Compatibility Issues

**Problem**: XTTS fails to load models with PyTorch 2.6+
```
Weights only load failed. This file can still be loaded, to do so you have two options...
WeightsUnpickler error: Unsupported global: GLOBAL TTS.tts.configs.xtts_config.XttsConfig
```

**Root Cause**: PyTorch 2.6+ changed `torch.load()` default from `weights_only=False` to `weights_only=True`

**Solution**: ✅ **FIXED** - All `torch.load()` calls now use `weights_only=False`

**Files Fixed**:
- `TTS/tts/models/xtts.py` - Main model loading
- `TTS/tts/layers/xtts/xtts_manager.py` - Speaker manager
- `TTS/tts/layers/xtts/hifigan_decoder.py` - HiFiGAN decoder
- `TTS/tts/layers/xtts/dvae.py` - DVAE model
- `TTS/tts/layers/xtts/trainer/gpt_trainer.py` - Trainer checkpoints
- `TTS/tts/utils/fairseq.py` - Fairseq checkpoints
- `TTS/tts/utils/managers.py` - Manager files
- `TTS/utils/io.py` - I/O utilities

### 2. Model Download Failures

**Problem**: XTTS model fails to download
```
Error downloading model from Hugging Face
```

**Solutions**:
1. **Check Internet Connection**
   ```bash
   curl -I https://huggingface.co
   ```

2. **Manual Download**
   ```bash
   # Download from Hugging Face manually
   git lfs install
   git clone https://huggingface.co/coqui/XTTS-v2
   ```

3. **Clear Cache**
   ```bash
   rm -rf ~/.cache/huggingface/hub/models--Systran--faster-whisper-large-v3
   ```

### 3. CUDA Out of Memory

**Problem**: GPU memory errors during processing
```
CUDA out of memory. Tried to allocate...
```

**Solutions**:
1. **Reduce Batch Size**
   - Set `gpt_batch_size` to 1
   - Use smaller audio chunks

2. **Use CPU Processing**
   ```python
   # Force CPU usage
   model = model.cpu()
   ```

3. **Free GPU Memory**
   ```python
   import torch
   torch.cuda.empty_cache()
   ```

4. **Close Other Applications**
   - Close other GPU-intensive applications
   - Restart ComfyUI

### 4. Audio Quality Issues

**Problem**: Poor audio quality or artifacts
- Robotic speech
- Background noise
- Inconsistent voice cloning

**Solutions**:
1. **Improve Reference Audio**
   - Use 16kHz+ sample rate
   - 10+ seconds of clear speech
   - No background noise
   - Single speaker

2. **Adjust Generation Parameters**
   ```python
   temperature = 0.5  # Lower for more stable output
   top_p = 0.85      # Optimal for most cases
   repetition_penalty = 4.0  # Prevent repetition
   ```

3. **Check Audio Format**
   - Input: WAV, MP3, FLAC, OGG
   - Output: WAV (16-bit, 24kHz)
   - Ensure proper sample rate

### 5. Import Errors

**Problem**: Module import failures
```
ModuleNotFoundError: No module named 'TTS'
ImportError: cannot import name 'XTTS_INFER'
```

**Solutions**:
1. **Check Installation**
   ```bash
   cd custom_nodes/ComfyUI-XTTS
   python -c "from nodes import XTTS_INFER; print('Import successful')"
   ```

2. **Fix Python Path**
   ```python
   import sys
   sys.path.append('/workspace/custom_nodes/ComfyUI-XTTS')
   ```

3. **Reinstall Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### 6. Node Not Appearing in ComfyUI

**Problem**: XTTS nodes don't appear in ComfyUI interface

**Solutions**:
1. **Restart ComfyUI**
   ```bash
   # Stop ComfyUI and restart
   python main.py
   ```

2. **Check Node Registration**
   ```python
   from nodes import NODE_CLASS_MAPPINGS
   print([k for k in NODE_CLASS_MAPPINGS.keys() if 'XTTS' in k])
   ```

3. **Check Custom Node Loading**
   ```python
   from nodes import init_external_custom_nodes
   init_external_custom_nodes()
   ```

### 7. Language Support Issues

**Problem**: Unsupported language errors
```
Language 'xx' not supported
```

**Supported Languages**:
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Polish (pl)
- Turkish (tr)
- Russian (ru)
- Dutch (nl)
- Czech (cs)
- Arabic (ar)
- Chinese (zh-cn)
- Japanese (ja)
- Hungarian (hu)
- Korean (ko)
- Hindi (hi)

### 8. SRT File Processing Issues

**Problem**: SRT file parsing errors
```
Error parsing SRT file
```

**Solutions**:
1. **Check SRT Format**
   ```srt
   1
   00:00:01,000 --> 00:00:04,000
   Speaker 1: Hello world
   
   2
   00:00:04,000 --> 00:00:07,000
   Speaker 2: How are you?
   ```

2. **Validate SRT File**
   ```python
   from srt import parse
   with open('file.srt', 'r') as f:
       subtitles = list(parse(f.read()))
   ```

3. **Check Encoding**
   ```python
   # Ensure UTF-8 encoding
   with open('file.srt', 'r', encoding='utf-8') as f:
       content = f.read()
   ```

## Advanced Troubleshooting

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Profiling

Monitor GPU usage:
```bash
nvidia-smi -l 1
```

### Memory Profiling

Check memory usage:
```python
import torch
print(f"GPU Memory: {torch.cuda.memory_allocated() / 1024**3:.2f} GB")
```

### Model Verification

Test model loading:
```python
from TTS.tts.models.xtts import Xtts
from TTS.tts.configs.xtts_config import XttsConfig

config = XttsConfig()
model = Xtts.init_from_config(config)
print("Model loaded successfully")
```

## Emergency Procedures

### Complete Reset

If all else fails:
1. **Backup Workflows**
   ```bash
   cp -r output/* backup/
   ```

2. **Remove XTTS Node**
   ```bash
   rm -rf custom_nodes/ComfyUI-XTTS
   ```

3. **Reinstall**
   ```bash
   git clone https://github.com/your-repo/ComfyUI-XTTS custom_nodes/ComfyUI-XTTS
   ```

4. **Restart ComfyUI**
   ```bash
   python main.py
   ```

### Fallback to CPU

If GPU issues persist:
```python
# Force CPU usage in node
device = torch.device("cpu")
model = model.to(device)
```

## Prevention Strategies

### Regular Maintenance

1. **Update Dependencies**
   ```bash
   pip install --upgrade torch torchaudio
   ```

2. **Clear Cache**
   ```bash
   rm -rf ~/.cache/huggingface
   ```

3. **Monitor Disk Space**
   ```bash
   df -h
   ```

### Best Practices

1. **Use Stable PyTorch Versions**
   - Test with PyTorch 2.0+ but < 2.6
   - Or use the fixed version with PyTorch 2.6+

2. **Quality Reference Audio**
   - 16kHz+ sample rate
   - 10+ seconds duration
   - Clear speech, no noise

3. **Regular Testing**
   - Test workflows regularly
   - Monitor performance metrics
   - Keep backups of working configurations

## Support Resources

### Documentation
- [XTTS GitHub Repository](https://github.com/coqui-ai/TTS)
- [ComfyUI Documentation](https://github.com/comfyanonymous/ComfyUI)
- [PyTorch Documentation](https://pytorch.org/docs/)

### Community Support
- ComfyUI Discord
- XTTS GitHub Issues
- PyTorch Forums

### Log Files
- ComfyUI logs: `server.log`
- XTTS logs: Check console output
- System logs: `dmesg | grep -i cuda`

---

**Note**: This troubleshooting guide covers the most common issues. For specific problems, check the logs and provide detailed error messages when seeking help.


