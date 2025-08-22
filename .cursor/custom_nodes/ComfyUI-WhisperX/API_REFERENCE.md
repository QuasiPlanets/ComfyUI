# WhisperX Custom Node API Reference

## Overview
This document provides a comprehensive API reference for the ComfyUI-WhisperX custom node, including all classes, methods, parameters, and usage examples.

## Core Classes

### SimpleLiveTranscription

#### Class Definition
```python
class SimpleLiveTranscription:
    """Main transcription node for live audio processing"""
    
    @classmethod
    def INPUT_TYPES(cls):
        """Define input types for ComfyUI"""
        return {
            "required": {
                "model_size": (["tiny", "base", "small", "medium", "large", "large-v3"], {"default": "large-v3"}),
                "language": (["auto", "en", "es", "fr", "de", "it", "pt", "nl", "pl", "ru"], {"default": "auto"}),
                "device": (["cuda", "cpu"], {"default": "cuda"}),
                "compute_type": (["float16", "float32", "int8"], {"default": "float16"})
            }
        }
    
    RETURN_TYPES = ("STRING", "LIST", "STRING")
    FUNCTION = "transcribe"
    CATEGORY = "WhisperX"
```

#### Methods

##### transcribe()
```python
def transcribe(self, model_size, language, device, compute_type):
    """
    Transcribe audio using WhisperX model.
    
    Args:
        model_size (str): WhisperX model size
        language (str): Language code for transcription
        device (str): Processing device (cuda/cpu)
        compute_type (str): Compute precision
    
    Returns:
        tuple: (transcription, segments, detected_language)
    """
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model_size` | str | `"large-v3"` | WhisperX model size |
| `language` | str | `"auto"` | Language code or auto-detection |
| `device` | str | `"cuda"` | Processing device |
| `compute_type` | str | `"float16"` | Compute precision |

#### Model Size Options
- `"tiny"`: Fastest, lowest accuracy
- `"base"`: Fast, good accuracy
- `"small"`: Balanced speed/accuracy
- `"medium"`: Good accuracy, moderate speed
- `"large"`: High accuracy, slower
- `"large-v3"`: Highest accuracy, slowest

#### Language Options
- `"auto"`: Automatic language detection
- `"en"`: English
- `"es"`: Spanish
- `"fr"`: French
- `"de"`: German
- `"it"`: Italian
- `"pt"`: Portuguese
- `"nl"`: Dutch
- `"pl"`: Polish
- `"ru"`: Russian

#### Compute Type Options
- `"float16"`: Fast, moderate memory usage
- `"float32"`: Accurate, high memory usage
- `"int8"`: Fastest, lowest memory usage

### WhisperXGlobal

#### Class Definition
```python
class WhisperXGlobal:
    """Global WhisperX model management and caching"""
    
    def __init__(self):
        self.models = {}
        self.config = {}
        self.memory_manager = MemoryManager()
```

#### Methods

##### get_model()
```python
def get_model(self, model_size, device="cuda", compute_type="float16"):
    """
    Get or load WhisperX model.
    
    Args:
        model_size (str): Model size
        device (str): Processing device
        compute_type (str): Compute precision
    
    Returns:
        WhisperX model instance
    """
```

##### cleanup()
```python
def cleanup(self):
    """
    Clean up resources and free memory.
    """
```

##### get_loaded_models()
```python
def get_loaded_models(self):
    """
    Get list of currently loaded models.
    
    Returns:
        list: List of loaded model keys
    """
```

## Integration Classes

### WhisperXIntegration

#### Class Definition
```python
class WhisperXIntegration:
    """Main integration class for WhisperX functionality"""
    
    def __init__(self):
        self.model_manager = WhisperXModelManager()
        self.audio_processor = AudioProcessor()
        self.memory_manager = MemoryManager()
```

#### Methods

##### transcribe_audio()
```python
def transcribe_audio(self, audio_data, model_size="large-v3", language="auto", device="cuda", compute_type="float16"):
    """
    Transcribe audio data using WhisperX.
    
    Args:
        audio_data (np.ndarray): Audio data array
        model_size (str): WhisperX model size
        language (str): Language code
        device (str): Processing device
        compute_type (str): Compute precision
    
    Returns:
        dict: Transcription result with text, segments, and language
    """
```

##### is_gpu_available()
```python
def is_gpu_available(self):
    """
    Check if GPU is available for processing.
    
    Returns:
        bool: True if GPU is available
    """
```

##### get_loaded_models()
```python
def get_loaded_models(self):
    """
    Get list of currently loaded models.
    
    Returns:
        list: List of loaded model information
    """
```

### WhisperXModelManager

#### Class Definition
```python
class WhisperXModelManager:
    """Manages WhisperX model loading and caching"""
    
    def __init__(self):
        self.models = {}
        self.device = "cuda"
```

#### Methods

##### load_model()
```python
def load_model(self, model_size, device="cuda", compute_type="float16"):
    """
    Load WhisperX model with caching.
    
    Args:
        model_size (str): Model size
        device (str): Processing device
        compute_type (str): Compute precision
    
    Returns:
        WhisperX model instance
    """
```

##### unload_model()
```python
def unload_model(self, model_size, device="cuda", compute_type="float16"):
    """
    Unload specific model and free memory.
    
    Args:
        model_size (str): Model size
        device (str): Processing device
        compute_type (str): Compute precision
    """
```

##### clear_all_models()
```python
def clear_all_models(self):
    """
    Unload all models and free memory.
    """
```

### AudioProcessor

#### Class Definition
```python
class AudioProcessor:
    """Handles audio processing and optimization"""
    
    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
```

#### Methods

##### process_audio()
```python
def process_audio(self, audio_data, target_sample_rate=16000):
    """
    Process and optimize audio data.
    
    Args:
        audio_data (np.ndarray): Input audio data
        target_sample_rate (int): Target sample rate
    
    Returns:
        np.ndarray: Processed audio data
    """
```

##### detect_silence()
```python
def detect_silence(self, audio_data, threshold=0.03):
    """
    Detect if audio segment is silence.
    
    Args:
        audio_data (np.ndarray): Audio data
        threshold (float): RMS threshold
    
    Returns:
        bool: True if audio is silence
    """
```

##### normalize_audio()
```python
def normalize_audio(self, audio_data):
    """
    Normalize audio data.
    
    Args:
        audio_data (np.ndarray): Audio data
    
    Returns:
        np.ndarray: Normalized audio data
    """
```

### MemoryManager

#### Class Definition
```python
class MemoryManager:
    """Manages GPU memory and cleanup"""
    
    def __init__(self):
        self.allocated_memory = 0
```

#### Methods

##### cleanup()
```python
def cleanup(self):
    """
    Clean up GPU memory.
    """
```

##### emergency_cleanup()
```python
def emergency_cleanup(self):
    """
    Emergency GPU memory cleanup.
    """
```

##### get_memory_usage()
```python
def get_memory_usage(self):
    """
    Get current GPU memory usage.
    
    Returns:
        dict: Memory usage information
    """
```

## WebSocket API

### Message Types

#### Audio Chunk Message
```json
{
    "type": "whisperx_audio_chunk",
    "audio": "base64_encoded_audio_data",
    "timestamp": 1234567890.123,
    "sample_rate": 16000,
    "channels": 1
}
```

#### Transcription Result Message
```json
{
    "type": "whisperx_transcription_result",
    "transcription": "Hello, world!",
    "segments": [
        {
            "start": 0.0,
            "end": 1.5,
            "text": "Hello, world!",
            "confidence": 0.95
        }
    ],
    "language": "en",
    "confidence": 0.95
}
```

#### Status Message
```json
{
    "type": "whisperx_status",
    "status": "connected|processing|error",
    "message": "Status description",
    "timestamp": 1234567890.123
}
```

#### Error Message
```json
{
    "type": "whisperx_error",
    "error": "Error description",
    "timestamp": 1234567890.123
}
```

### WebSocket Handler

#### Class Definition
```python
class WhisperXWebSocketHandler:
    """Handles WebSocket connections for real-time audio streaming"""
    
    def __init__(self):
        self.audio_buffer = []
        self.buffer_size = 1.5
        self.sample_rate = 16000
        self.whisperx_model = None
```

#### Methods

##### handle_websocket()
```python
async def handle_websocket(self, websocket, path):
    """
    Handle WebSocket connection and messages.
    
    Args:
        websocket: WebSocket connection
        path: Connection path
    """
```

##### process_audio_chunk()
```python
async def process_audio_chunk(self, websocket, data):
    """
    Process incoming audio chunk.
    
    Args:
        websocket: WebSocket connection
        data: Audio chunk data
    """
```

##### send_transcription_result()
```python
async def send_transcription_result(self, websocket, result):
    """
    Send transcription result to client.
    
    Args:
        websocket: WebSocket connection
        result: Transcription result
    """
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WHISPERX_MODEL_SIZE` | `"large-v3"` | Default model size |
| `WHISPERX_DEVICE` | `"cuda"` | Default processing device |
| `WHISPERX_COMPUTE_TYPE` | `"float16"` | Default compute precision |
| `WHISPERX_BUFFER_SIZE` | `1.5` | Audio buffer size in seconds |
| `WHISPERX_SAMPLE_RATE` | `16000` | Audio sample rate |
| `WHISPERX_RMS_THRESHOLD` | `0.03` | Silence detection threshold |

### Configuration Class

#### Class Definition
```python
class WhisperXConfig:
    """Configuration management for WhisperX"""
    
    def __init__(self):
        self.config = {
            "model_size": os.getenv("WHISPERX_MODEL_SIZE", "large-v3"),
            "device": os.getenv("WHISPERX_DEVICE", "cuda"),
            "compute_type": os.getenv("WHISPERX_COMPUTE_TYPE", "float16"),
            "buffer_size": float(os.getenv("WHISPERX_BUFFER_SIZE", "1.5")),
            "sample_rate": int(os.getenv("WHISPERX_SAMPLE_RATE", "16000")),
            "rms_threshold": float(os.getenv("WHISPERX_RMS_THRESHOLD", "0.03"))
        }
```

#### Methods

##### get_config()
```python
def get_config(self):
    """
    Get current configuration.
    
    Returns:
        dict: Configuration dictionary
    """
```

##### update_config()
```python
def update_config(self, key, value):
    """
    Update configuration value.
    
    Args:
        key (str): Configuration key
        value: Configuration value
    """
```

## Error Handling

### Exception Classes

#### WhisperXError
```python
class WhisperXError(Exception):
    """Base exception for WhisperX errors"""
    pass
```

#### ModelLoadError
```python
class ModelLoadError(WhisperXError):
    """Exception raised when model loading fails"""
    pass
```

#### TranscriptionError
```python
class TranscriptionError(WhisperXError):
    """Exception raised when transcription fails"""
    pass
```

#### AudioProcessingError
```python
class AudioProcessingError(WhisperXError):
    """Exception raised when audio processing fails"""
    pass
```

### Error Handling Methods

#### handle_error()
```python
def handle_error(self, error, context=None):
    """
    Handle and log errors.
    
    Args:
        error: Exception object
        context: Error context information
    """
```

#### retry_operation()
```python
async def retry_operation(self, operation, max_retries=3, delay=1.0):
    """
    Retry operation with exponential backoff.
    
    Args:
        operation: Function to retry
        max_retries (int): Maximum retry attempts
        delay (float): Initial delay in seconds
    
    Returns:
        Result of operation
    """
```

## Performance Monitoring

### Metrics Class

#### Class Definition
```python
class WhisperXMetrics:
    """Performance metrics collection"""
    
    def __init__(self):
        self.metrics = {
            'transcriptions': 0,
            'errors': 0,
            'total_time': 0,
            'avg_latency': 0,
            'memory_usage': 0
        }
```

#### Methods

##### record_transcription()
```python
def record_transcription(self, duration, memory_usage=None):
    """
    Record transcription metrics.
    
    Args:
        duration (float): Transcription duration
        memory_usage (float): Memory usage in MB
    """
```

##### record_error()
```python
def record_error(self):
    """
    Record error occurrence.
    """
```

##### get_metrics()
```python
def get_metrics(self):
    """
    Get current metrics.
    
    Returns:
        dict: Metrics dictionary
    """
```

##### reset_metrics()
```python
def reset_metrics(self):
    """
    Reset all metrics.
    """
```

## Usage Examples

### Basic Usage
```python
# Create WhisperX integration
whisperx = WhisperXIntegration()

# Transcribe audio
audio_data = load_audio_file("audio.wav")
result = whisperx.transcribe_audio(audio_data)

print(f"Transcription: {result['text']}")
print(f"Language: {result['language']}")
```

### Advanced Usage
```python
# Configure custom settings
config = WhisperXConfig()
config.update_config("model_size", "large-v3")
config.update_config("compute_type", "float16")

# Create integration with custom config
whisperx = WhisperXIntegration(config)

# Process multiple audio files
for audio_file in audio_files:
    audio_data = load_audio_file(audio_file)
    result = whisperx.transcribe_audio(audio_data)
    print(f"File: {audio_file}, Transcription: {result['text']}")
```

### WebSocket Usage
```python
# Server-side
async def handle_websocket(websocket, path):
    handler = WhisperXWebSocketHandler()
    await handler.handle_websocket(websocket, path)

# Start server
start_server = websockets.serve(handle_websocket, "localhost", 8189)
asyncio.get_event_loop().run_until_complete(start_server)
```

### Memory Management
```python
# Create memory manager
memory_manager = MemoryManager()

# Monitor memory usage
usage = memory_manager.get_memory_usage()
print(f"GPU Memory: {usage['allocated']}MB")

# Clean up after processing
memory_manager.cleanup()
```

This API reference provides comprehensive documentation for all classes, methods, and parameters in the WhisperX custom node, enabling developers to effectively integrate and extend the functionality.


