# Diagnostic Code Guide for XTTS Custom Node

*A comprehensive guide for adding diagnostic logging to the XTTS custom node when debugging is needed*

---

## Table of Contents

1. [Overview](#overview)
2. [When to Add Diagnostic Code](#when-to-add-diagnostic-code)
3. [Diagnostic Code Templates](#diagnostic-code-templates)
4. [Implementation Examples](#implementation-examples)
5. [Best Practices](#best-practices)
6. [Removing Diagnostic Code](#removing-diagnostic-code)

---

## Overview

This guide provides templates and examples for adding diagnostic logging to the XTTS custom node when debugging issues. The diagnostic code should be added temporarily during development and removed before production deployment.

### Key Principles
- **Temporary Use**: Diagnostic code should be removed after debugging
- **Comprehensive Logging**: Log all relevant data types, shapes, and values
- **Clear Labels**: Use consistent `[XTTS * DEBUG]` prefixes
- **Performance Aware**: Minimize impact on generation speed

---

## When to Add Diagnostic Code

### Common Scenarios
1. **Model Loading Issues**: When XTTS fails to load or initialize
2. **Audio Quality Problems**: When generated audio is glitchy or poor quality
3. **Generation Failures**: When inference fails or produces errors
4. **Performance Issues**: When generation is slow or uses excessive memory
5. **Parameter Tuning**: When testing different generation parameters

### Signs You Need Diagnostic Code
- CUDA errors or device-side asserts
- Audio files that are too short or cut off
- Poor voice quality or unnatural speech
- Memory issues or crashes
- Unexpected behavior with different inputs

---

## Diagnostic Code Templates

### 1. Text Tokenization Debugging

**Location**: `custom_nodes/ComfyUI-XTTS/TTS/tts/models/xtts.py` in the `inference` method

**Template**:
```python
# Add after text processing
sent = sent.strip().lower()

# DIAGNOSTIC: Log text tokenization to identify encoding issues
print(f"[XTTS TOKENIZATION DEBUG] Input text: '{sent}'")
print(f"[XTTS TOKENIZATION DEBUG] Language: {language}")

encoded_tokens = self.tokenizer.encode(sent, lang=language)
print(f"[XTTS TOKENIZATION DEBUG] Encoded tokens: {encoded_tokens}")
print(f"[XTTS TOKENIZATION DEBUG] Token count: {len(encoded_tokens)}")

text_tokens = torch.IntTensor(encoded_tokens).unsqueeze(0).to(self.device)
print(f"[XTTS TOKENIZATION DEBUG] Text tokens shape: {text_tokens.shape}")
print(f"[XTTS TOKENIZATION DEBUG] Text tokens: {text_tokens}")
```

### 2. GPT Generation Debugging

**Location**: `custom_nodes/ComfyUI-XTTS/TTS/tts/models/xtts.py` in the `inference` method

**Template**:
```python
# Add before GPT generation
with torch.no_grad():
    # DIAGNOSTIC: Log GPT generation inputs and outputs
    print(f"[XTTS GPT DEBUG] GPT generation parameters:")
    print(f"[XTTS GPT DEBUG]   temperature: {temperature}")
    print(f"[XTTS GPT DEBUG]   top_p: {top_p}")
    print(f"[XTTS GPT DEBUG]   top_k: {top_k}")
    print(f"[XTTS GPT DEBUG]   repetition_penalty: {repetition_penalty}")
    print(f"[XTTS GPT DEBUG] Input text_tokens shape: {text_tokens.shape}")
    print(f"[XTTS GPT DEBUG] Input cond_latents shape: {gpt_cond_latent.shape}")
    
    text_len = len(sent)
    print(f"[XTTS GPT DEBUG] Text length: {text_len} chars, using model defaults")
    print(f"[XTTS GPT DEBUG] Using original XTTS parameters")
    
    gpt_codes = self.gpt.generate(...)
    
    print(f"[XTTS GPT DEBUG] Generated GPT codes shape: {gpt_codes.shape}")
    print(f"[XTTS GPT DEBUG] GPT codes dtype: {gpt_codes.dtype}")
    print(f"[XTTS GPT DEBUG] GPT codes min/max: {gpt_codes.min()}/{gpt_codes.max()}")
    print(f"[XTTS GPT DEBUG] GPT codes sample: {gpt_codes[0, :10]}")  # First 10 codes
```

### 3. Latent Processing Debugging

**Location**: `custom_nodes/ComfyUI-XTTS/TTS/tts/models/xtts.py` in the `inference` method

**Template**:
```python
# Add before GPT latent computation
text_len = torch.tensor([text_tokens.shape[-1]], device=self.device)

# DIAGNOSTIC: Log GPT latent processing
print(f"[XTTS LATENT DEBUG] Computing GPT latents...")
print(f"[XTTS LATENT DEBUG] Expected output length: {expected_output_len}")
print(f"[XTTS LATENT DEBUG] Text length: {text_len}")

gpt_latents = self.gpt(...)

print(f"[XTTS LATENT DEBUG] GPT latents shape: {gpt_latents.shape}")
print(f"[XTTS LATENT DEBUG] GPT latents dtype: {gpt_latents.dtype}")
print(f"[XTTS LATENT DEBUG] GPT latents min/max: {gpt_latents.min():.6f}/{gpt_latents.max():.6f}")
print(f"[XTTS LATENT DEBUG] GPT latents mean: {gpt_latents.mean():.6f}")
```

### 4. Speaker Embedding Debugging

**Location**: `custom_nodes/ComfyUI-XTTS/TTS/tts/models/xtts.py` in the `inference` method

**Template**:
```python
# Add before HiFiGAN decoder
gpt_latents_list.append(gpt_latents.cpu())

# DIAGNOSTIC: Log speaker embedding properties
print(f"[XTTS SPEAKER DEBUG] Speaker embedding shape: {speaker_embedding.shape}")
print(f"[XTTS SPEAKER DEBUG] Speaker embedding dtype: {speaker_embedding.dtype}")
print(f"[XTTS SPEAKER DEBUG] Speaker embedding min/max: {speaker_embedding.min():.6f}/{speaker_embedding.max():.6f}")
print(f"[XTTS SPEAKER DEBUG] Speaker embedding mean: {speaker_embedding.mean():.6f}")
print(f"[XTTS SPEAKER DEBUG] Speaker embedding std: {speaker_embedding.std():.6f}")
```

### 5. Audio Generation Debugging

**Location**: `custom_nodes/ComfyUI-XTTS/TTS/tts/models/xtts.py` in the `inference` method

**Template**:
```python
# Add after HiFiGAN decoder
wav_output = self.hifigan_decoder(gpt_latents, g=speaker_embedding)
wav_cpu = wav_output.cpu().squeeze()

# DIAGNOSTIC: Log audio properties to identify glitchy audio cause
print(f"[XTTS AUDIO DEBUG] wav_output shape: {wav_output.shape}")
print(f"[XTTS AUDIO DEBUG] wav_cpu shape: {wav_cpu.shape}")
print(f"[XTTS AUDIO DEBUG] wav_cpu dtype: {wav_cpu.dtype}")
print(f"[XTTS AUDIO DEBUG] wav_cpu min/max: {wav_cpu.min():.6f}/{wav_cpu.max():.6f}")
print(f"[XTTS AUDIO DEBUG] wav_cpu mean: {wav_cpu.mean():.6f}")
print(f"[XTTS AUDIO DEBUG] Expected sample rate: 24000")
```

### 6. Audio Concatenation Debugging

**Location**: `custom_nodes/ComfyUI-XTTS/TTS/tts/models/xtts.py` in the `inference` method

**Template**:
```python
# Add before final audio processing
# DIAGNOSTIC: Log audio concatenation process
print(f"[XTTS CONCATENATION DEBUG] Number of audio segments: {len(wavs)}")
for i, wav_segment in enumerate(wavs):
    print(f"[XTTS CONCATENATION DEBUG] Segment {i}: shape={wav_segment.shape}, dtype={wav_segment.dtype}, min/max={wav_segment.min():.6f}/{wav_segment.max():.6f}")

concatenated_wav = torch.cat(wavs, dim=0)
print(f"[XTTS CONCATENATION DEBUG] Concatenated shape: {concatenated_wav.shape}")
print(f"[XTTS CONCATENATION DEBUG] Concatenated dtype: {concatenated_wav.dtype}")
print(f"[XTTS CONCATENATION DEBUG] Concatenated min/max: {concatenated_wav.min():.6f}/{concatenated_wav.max():.6f}")

final_wav_numpy = concatenated_wav.numpy()
print(f"[XTTS CONCATENATION DEBUG] Final numpy shape: {final_wav_numpy.shape}")
print(f"[XTTS CONCATENATION DEBUG] Final numpy dtype: {final_wav_numpy.dtype}")
print(f"[XTTS CONCATENATION DEBUG] Final numpy min/max: {final_wav_numpy.min():.6f}/{final_wav_numpy.max():.6f}")
```

### 7. Node-Level Debugging

**Location**: `custom_nodes/ComfyUI-XTTS/nodes.py` in the `get_wav_tts` method

**Template**:
```python
# Add after audio generation
wav_path = os.path.join(output_path, f"{time.time()}_xtts.wav")
# Fix: Handle numpy array properly for better audio quality
wav_data = out["wav"]

# DIAGNOSTIC: Log audio saving process  
print(f"[XTTS NODE DEBUG] Input wav_data type: {type(wav_data)}")
print(f"[XTTS NODE DEBUG] Input wav_data shape: {wav_data.shape if hasattr(wav_data, 'shape') else 'No shape'}")
print(f"[XTTS NODE DEBUG] Input wav_data dtype: {wav_data.dtype if hasattr(wav_data, 'dtype') else type(wav_data)}")
if hasattr(wav_data, 'min'):
    print(f"[XTTS NODE DEBUG] Input wav_data min/max: {wav_data.min():.6f}/{wav_data.max():.6f}")

if isinstance(wav_data, np.ndarray):
    wav_tensor = torch.from_numpy(wav_data).float().unsqueeze(0)
    print(f"[XTTS NODE DEBUG] From numpy conversion")
else:
    wav_tensor = torch.tensor(wav_data).float().unsqueeze(0)
    print(f"[XTTS NODE DEBUG] From tensor conversion")
    
print(f"[XTTS NODE DEBUG] Final tensor shape: {wav_tensor.shape}")
print(f"[XTTS NODE DEBUG] Final tensor dtype: {wav_tensor.dtype}")
print(f"[XTTS NODE DEBUG] Final tensor min/max: {wav_tensor.min():.6f}/{wav_tensor.max():.6f}")
print(f"[XTTS NODE DEBUG] Saving to: {wav_path}")
print(f"[XTTS NODE DEBUG] Sample rate: 24000, bits_per_sample: 16")
```

---

## Implementation Examples

### Example 1: Debugging Audio Quality Issues

**Problem**: Generated audio is glitchy or poor quality

**Diagnostic Code to Add**:
```python
# In xtts.py inference method, after HiFiGAN decoder
wav_output = self.hifigan_decoder(gpt_latents, g=speaker_embedding)
wav_cpu = wav_output.cpu().squeeze()

# DIAGNOSTIC: Log audio properties to identify glitchy audio cause
print(f"[XTTS AUDIO DEBUG] wav_output shape: {wav_output.shape}")
print(f"[XTTS AUDIO DEBUG] wav_cpu shape: {wav_cpu.shape}")
print(f"[XTTS AUDIO DEBUG] wav_cpu dtype: {wav_cpu.dtype}")
print(f"[XTTS AUDIO DEBUG] wav_cpu min/max: {wav_cpu.min():.6f}/{wav_cpu.max():.6f}")
print(f"[XTTS AUDIO DEBUG] wav_cpu mean: {wav_cpu.mean():.6f}")
print(f"[XTTS AUDIO DEBUG] Expected sample rate: 24000")
```

### Example 2: Debugging Generation Parameters

**Problem**: Audio generation stops prematurely

**Diagnostic Code to Add**:
```python
# In xtts.py inference method, before GPT generation
with torch.no_grad():
    # DIAGNOSTIC: Log GPT generation inputs and outputs
    print(f"[XTTS GPT DEBUG] GPT generation parameters:")
    print(f"[XTTS GPT DEBUG]   temperature: {temperature}")
    print(f"[XTTS GPT DEBUG]   top_p: {top_p}")
    print(f"[XTTS GPT DEBUG]   top_k: {top_k}")
    print(f"[XTTS GPT DEBUG]   repetition_penalty: {repetition_penalty}")
    print(f"[XTTS GPT DEBUG] Input text_tokens shape: {text_tokens.shape}")
    print(f"[XTTS GPT DEBUG] Input cond_latents shape: {gpt_cond_latent.shape}")
    
    text_len = len(sent)
    print(f"[XTTS GPT DEBUG] Text length: {text_len} chars, using model defaults")
    print(f"[XTTS GPT DEBUG] Using original XTTS parameters")
```

### Example 3: Debugging Model Loading Issues

**Problem**: Model fails to load or initialize

**Diagnostic Code to Add**:
```python
# In nodes.py get_wav_tts method, after model loading
print("Loading model...")
config = XttsConfig()
config.load_json(os.path.join(pretrained_models_path, "config.json"))
model = Xtts.init_from_config(config)
model.load_checkpoint(config, checkpoint_dir=pretrained_models_path, use_deepspeed=False)
if cuda_malloc.cuda_malloc_supported():
    model.cuda()

# DIAGNOSTIC: Log model loading status
print(f"[XTTS MODEL DEBUG] Model loaded successfully")
print(f"[XTTS MODEL DEBUG] Model device: {next(model.parameters()).device}")
print(f"[XTTS MODEL DEBUG] Config path: {os.path.join(pretrained_models_path, 'config.json')}")
print(f"[XTTS MODEL DEBUG] Checkpoint path: {pretrained_models_path}")
```

---

## Best Practices

### 1. Consistent Labeling
- Use `[XTTS * DEBUG]` prefix for all diagnostic messages
- Use descriptive section names: `TOKENIZATION`, `GPT`, `LATENT`, `SPEAKER`, `AUDIO`, `CONCATENATION`, `NODE`, `MODEL`

### 2. Comprehensive Data Logging
- Log data types, shapes, and value ranges
- Include min/max values for tensors
- Log expected vs actual values
- Include device information for tensors

### 3. Performance Considerations
- Diagnostic code adds overhead
- Remove after debugging is complete
- Consider conditional logging for production

### 4. Error Context
- Log the context around errors
- Include parameter values when issues occur
- Log both successful and failed operations

---

## Removing Diagnostic Code

### When to Remove
- After the issue is resolved
- Before production deployment
- When performance becomes a concern
- When logs become too verbose

### Removal Process
1. **Identify all diagnostic statements** using search for `[XTTS * DEBUG]`
2. **Remove print statements** while preserving core functionality
3. **Test thoroughly** to ensure removal doesn't break functionality
4. **Update documentation** if any insights were gained

### Example Removal
```python
# Before (with diagnostic code)
print(f"[XTTS AUDIO DEBUG] wav_output shape: {wav_output.shape}")
wav_cpu = wav_output.cpu().squeeze()
print(f"[XTTS AUDIO DEBUG] wav_cpu shape: {wav_cpu.shape}")

# After (clean code)
wav_cpu = wav_output.cpu().squeeze()
```

---

## Quick Reference

### Common Debugging Scenarios

| Issue | Diagnostic Code Location | Key Information to Log |
|-------|-------------------------|------------------------|
| **Audio Quality** | `xtts.py` after HiFiGAN | Shape, dtype, min/max values |
| **Generation Stops** | `xtts.py` before GPT | Parameters, input shapes |
| **Model Loading** | `nodes.py` after loading | Device, config paths |
| **Tokenization** | `xtts.py` after encoding | Tokens, counts, shapes |
| **Memory Issues** | Both files | Tensor shapes, device info |

### Diagnostic Code Checklist
- [ ] Add appropriate section headers
- [ ] Log data types and shapes
- [ ] Include min/max values for tensors
- [ ] Log expected vs actual values
- [ ] Include device information
- [ ] Test with problematic inputs
- [ ] Document findings
- [ ] Remove after debugging

---

*Last Updated: July 31, 2025*
*Status: Ready for use when debugging XTTS issues* 