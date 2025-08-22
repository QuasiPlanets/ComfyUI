# WhisperX Custom Node Integration Guide

## Overview
This guide provides comprehensive information for integrating the WhisperX custom node into ComfyUI workflows and external systems. It covers installation, configuration, usage patterns, and advanced integration techniques.

## Quick Start Integration

### 1. Basic Installation
```bash
# Clone the custom node
cd custom_nodes
git clone https://github.com/your-repo/ComfyUI-WhisperX.git

# Install dependencies
cd ComfyUI-WhisperX
pip install -r requirements.txt

# Install system dependencies
sudo apt-get install libcudnn8=8.9.*-1+cuda12.1 libcudnn8-dev=8.9.*-1+cuda12.1

# Restart ComfyUI
```

### 2. Basic Usage
```python
# Simple workflow example
workflow = {
    "nodes": {
        "whisperx_node": {
            "class_type": "SimpleLiveTranscription",
            "inputs": {
                "model_size": "large-v3",
                "language": "auto",
                "device": "cuda",
                "compute_type": "float16"
            }
        }
    }
}
```

## Integration Patterns

### 1. WebSocket Integration

#### Server-Side Setup
```python
# ComfyUI server integration
import asyncio
import websockets
import json
from whisperx_comfyui_integration import WhisperXIntegration

class WhisperXServer:
    def __init__(self):
        self.whisperx = WhisperXIntegration()
        
    async def handle_websocket(self, websocket, path):
        async for message in websocket:
            data = json.loads(message)
            
            if data['type'] == 'whisperx_audio_chunk':
                result = await self.whisperx.process_audio(data['audio'])
                await websocket.send(json.dumps({
                    'type': 'whisperx_result',
                    'transcription': result['text'],
                    'language': result['language']
                }))

# Start server
start_server = websockets.serve(WhisperXServer().handle_websocket, "localhost", 8189)
asyncio.get_event_loop().run_until_complete(start_server)
```

#### Client-Side Integration
```javascript
// Browser client integration
class WhisperXClient {
    constructor(url = 'ws://localhost:8189') {
        this.url = url;
        this.websocket = null;
        this.onTranscription = null;
    }
    
    async connect() {
        this.websocket = new WebSocket(this.url);
        
        this.websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'whisperx_result' && this.onTranscription) {
                this.onTranscription(data);
            }
        };
    }
    
    sendAudio(audioData) {
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            this.websocket.send(JSON.stringify({
                type: 'whisperx_audio_chunk',
                audio: audioData
            }));
        }
    }
}

// Usage
const client = new WhisperXClient();
client.onTranscription = (result) => {
    console.log('Transcription:', result.transcription);
    console.log('Language:', result.language);
};

await client.connect();
```

### 2. REST API Integration

#### API Endpoints
```python
# Flask API integration
from flask import Flask, request, jsonify
from whisperx_comfyui_integration import WhisperXIntegration

app = Flask(__name__)
whisperx = WhisperXIntegration()

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        audio_file = request.files['audio']
        audio_data = audio_file.read()
        
        result = whisperx.transcribe_audio(audio_data)
        
        return jsonify({
            'success': True,
            'transcription': result['text'],
            'language': result['language'],
            'segments': result['segments']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'gpu_available': whisperx.is_gpu_available(),
        'models_loaded': whisperx.get_loaded_models()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

#### Client Usage
```python
# Python client
import requests

def transcribe_audio_file(file_path):
    with open(file_path, 'rb') as f:
        files = {'audio': f}
        response = requests.post('http://localhost:5000/transcribe', files=files)
        
    if response.status_code == 200:
        result = response.json()
        return result['transcription']
    else:
        raise Exception(f"Transcription failed: {response.text}")

# Usage
transcription = transcribe_audio_file('audio.wav')
print(f"Transcription: {transcription}")
```

### 3. ComfyUI Workflow Integration

#### Node Configuration
```python
# Advanced node configuration
class WhisperXNodeConfig:
    def __init__(self):
        self.config = {
            "model_size": "large-v3",
            "language": "auto",
            "device": "cuda",
            "compute_type": "float16",
            "buffer_size": 1.5,
            "rms_threshold": 0.03,
            "enable_silence_detection": True,
            "enable_gpu_optimization": True
        }
    
    def get_node_inputs(self):
        return {
            "model_size": (["tiny", "base", "small", "medium", "large", "large-v3"], 
                          {"default": self.config["model_size"]}),
            "language": (["auto", "en", "es", "fr", "de", "it", "pt", "nl", "pl", "ru"], 
                        {"default": self.config["language"]}),
            "device": (["cuda", "cpu"], {"default": self.config["device"]}),
            "compute_type": (["float16", "float32", "int8"], 
                           {"default": self.config["compute_type"]})
        }
```

#### Workflow Examples
```python
# Real-time transcription workflow
real_time_workflow = {
    "nodes": {
        "audio_input": {
            "class_type": "AudioInputNode",
            "inputs": {
                "sample_rate": 16000,
                "channels": 1
            }
        },
        "whisperx_transcription": {
            "class_type": "SimpleLiveTranscription",
            "inputs": {
                "model_size": "large-v3",
                "language": "auto",
                "device": "cuda",
                "compute_type": "float16"
            }
        },
        "text_output": {
            "class_type": "TextOutputNode",
            "inputs": {}
        }
    },
    "connections": {
        "audio_input": {"audio": "whisperx_transcription"},
        "whisperx_transcription": {"transcription": "text_output"}
    }
}
```

## Advanced Integration Techniques

### 1. Multi-Model Integration

#### Model Management
```python
class MultiModelWhisperX:
    def __init__(self):
        self.models = {}
        self.active_model = None
        
    def load_model(self, model_size, device="cuda", compute_type="float16"):
        model_key = f"{model_size}_{device}_{compute_type}"
        
        if model_key not in self.models:
            self.models[model_key] = whisperx.load_model(
                model_size, device=device, compute_type=compute_type
            )
        
        return self.models[model_key]
    
    def switch_model(self, model_size, device="cuda", compute_type="float16"):
        self.active_model = self.load_model(model_size, device, compute_type)
        
    def transcribe(self, audio_data, language="auto"):
        if not self.active_model:
            raise ValueError("No active model selected")
            
        return self.active_model.transcribe(audio_data, language=language)
```

#### Usage Example
```python
# Multi-model usage
whisperx_multi = MultiModelWhisperX()

# Load different models
whisperx_multi.load_model("base", device="cuda", compute_type="float16")  # Fast
whisperx_multi.load_model("large-v3", device="cuda", compute_type="float16")  # Accurate

# Switch between models based on requirements
whisperx_multi.switch_model("base")  # For speed
result_fast = whisperx_multi.transcribe(audio_data)

whisperx_multi.switch_model("large-v3")  # For accuracy
result_accurate = whisperx_multi.transcribe(audio_data)
```

### 2. Batch Processing Integration

#### Batch Processor
```python
class WhisperXBatchProcessor:
    def __init__(self, batch_size=4):
        self.batch_size = batch_size
        self.audio_queue = []
        self.whisperx = WhisperXIntegration()
        
    def add_audio(self, audio_data):
        self.audio_queue.append(audio_data)
        
        if len(self.audio_queue) >= self.batch_size:
            return self.process_batch()
        
        return None
    
    def process_batch(self):
        if not self.audio_queue:
            return []
        
        # Process batch
        results = []
        for audio_data in self.audio_queue:
            result = self.whisperx.transcribe_audio(audio_data)
            results.append(result)
        
        # Clear queue
        self.audio_queue = []
        
        return results
    
    def flush(self):
        """Process remaining audio in queue"""
        if self.audio_queue:
            return self.process_batch()
        return []
```

#### Usage Example
```python
# Batch processing
batch_processor = WhisperXBatchProcessor(batch_size=4)

# Add audio chunks
for audio_chunk in audio_chunks:
    results = batch_processor.add_audio(audio_chunk)
    if results:
        for result in results:
            print(f"Transcription: {result['text']}")

# Process remaining audio
final_results = batch_processor.flush()
```

### 3. Streaming Integration

#### Stream Processor
```python
class WhisperXStreamProcessor:
    def __init__(self, buffer_size=1.5, sample_rate=16000):
        self.buffer_size = buffer_size
        self.sample_rate = sample_rate
        self.audio_buffer = []
        self.whisperx = WhisperXIntegration()
        self.on_transcription = None
        
    def add_audio_chunk(self, audio_chunk):
        self.audio_buffer.extend(audio_chunk)
        
        # Check if buffer is full
        buffer_duration = len(self.audio_buffer) / self.sample_rate
        
        if buffer_duration >= self.buffer_size:
            # Process buffer
            audio_data = np.array(self.audio_buffer)
            result = self.whisperx.transcribe_audio(audio_data)
            
            # Clear buffer
            self.audio_buffer = []
            
            # Call callback
            if self.on_transcription:
                self.on_transcription(result)
            
            return result
        
        return None
    
    def set_transcription_callback(self, callback):
        self.on_transcription = callback
```

#### Usage Example
```python
# Streaming usage
stream_processor = WhisperXStreamProcessor()

def on_transcription(result):
    print(f"Live transcription: {result['text']}")

stream_processor.set_transcription_callback(on_transcription)

# Process audio stream
for audio_chunk in audio_stream:
    stream_processor.add_audio_chunk(audio_chunk)
```

## Performance Optimization

### 1. GPU Memory Management
```python
class GPUOptimizedWhisperX:
    def __init__(self):
        self.whisperx = WhisperXIntegration()
        self.memory_manager = MemoryManager()
        
    def transcribe_with_optimization(self, audio_data):
        try:
            # Clear GPU cache before processing
            torch.cuda.empty_cache()
            
            # Process audio
            result = self.whisperx.transcribe_audio(audio_data)
            
            # Clean up after processing
            self.memory_manager.cleanup()
            
            return result
            
        except Exception as e:
            # Emergency cleanup on error
            self.memory_manager.emergency_cleanup()
            raise e

class MemoryManager:
    def __init__(self):
        self.allocated_memory = 0
        
    def cleanup(self):
        torch.cuda.empty_cache()
        
    def emergency_cleanup(self):
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
```

### 2. Caching Integration
```python
class WhisperXCache:
    def __init__(self, max_size=1000):
        self.cache = {}
        self.max_size = max_size
        
    def get_cached_result(self, audio_hash):
        return self.cache.get(audio_hash)
        
    def cache_result(self, audio_hash, result):
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[audio_hash] = result
        
    def clear_cache(self):
        self.cache.clear()

class CachedWhisperX:
    def __init__(self):
        self.whisperx = WhisperXIntegration()
        self.cache = WhisperXCache()
        
    def transcribe_with_cache(self, audio_data):
        # Generate hash for audio data
        audio_hash = hashlib.md5(audio_data.tobytes()).hexdigest()
        
        # Check cache first
        cached_result = self.cache.get_cached_result(audio_hash)
        if cached_result:
            return cached_result
        
        # Process with WhisperX
        result = self.whisperx.transcribe_audio(audio_data)
        
        # Cache result
        self.cache.cache_result(audio_hash, result)
        
        return result
```

## Error Handling and Recovery

### 1. Robust Error Handling
```python
class RobustWhisperX:
    def __init__(self, max_retries=3):
        self.whisperx = WhisperXIntegration()
        self.max_retries = max_retries
        self.error_handler = ErrorHandler()
        
    def transcribe_with_retry(self, audio_data):
        for attempt in range(self.max_retries):
            try:
                return self.whisperx.transcribe_audio(audio_data)
                
            except Exception as e:
                self.error_handler.handle_error(e, attempt)
                
                if attempt == self.max_retries - 1:
                    raise e
                
                # Wait before retry
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return None

class ErrorHandler:
    def __init__(self):
        self.error_count = 0
        self.max_errors = 10
        
    def handle_error(self, error, attempt):
        self.error_count += 1
        
        if self.error_count > self.max_errors:
            raise Exception("Too many errors, stopping")
        
        print(f"Attempt {attempt + 1} failed: {error}")
```

### 2. Graceful Degradation
```python
class GracefulWhisperX:
    def __init__(self):
        self.primary_model = "large-v3"
        self.fallback_model = "base"
        self.whisperx = WhisperXIntegration()
        
    def transcribe_with_fallback(self, audio_data):
        try:
            # Try primary model
            return self.whisperx.transcribe_audio(
                audio_data, 
                model_size=self.primary_model
            )
            
        except Exception as e:
            print(f"Primary model failed: {e}")
            
            try:
                # Try fallback model
                return self.whisperx.transcribe_audio(
                    audio_data, 
                    model_size=self.fallback_model
                )
                
            except Exception as e2:
                print(f"Fallback model also failed: {e2}")
                raise e2
```

## Monitoring and Logging

### 1. Performance Monitoring
```python
class WhisperXMonitor:
    def __init__(self):
        self.metrics = {
            'transcriptions': 0,
            'errors': 0,
            'total_time': 0,
            'avg_latency': 0
        }
        
    def record_transcription(self, duration):
        self.metrics['transcriptions'] += 1
        self.metrics['total_time'] += duration
        
        # Update average latency
        self.metrics['avg_latency'] = (
            self.metrics['total_time'] / self.metrics['transcriptions']
        )
        
    def record_error(self):
        self.metrics['errors'] += 1
        
    def get_metrics(self):
        return self.metrics.copy()
        
    def get_success_rate(self):
        total = self.metrics['transcriptions'] + self.metrics['errors']
        if total == 0:
            return 0
        return self.metrics['transcriptions'] / total

class MonitoredWhisperX:
    def __init__(self):
        self.whisperx = WhisperXIntegration()
        self.monitor = WhisperXMonitor()
        
    def transcribe_with_monitoring(self, audio_data):
        start_time = time.time()
        
        try:
            result = self.whisperx.transcribe_audio(audio_data)
            
            duration = time.time() - start_time
            self.monitor.record_transcription(duration)
            
            return result
            
        except Exception as e:
            self.monitor.record_error()
            raise e
```

### 2. Logging Integration
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('whisperx_integration.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('whisperx_integration')

class LoggedWhisperX:
    def __init__(self):
        self.whisperx = WhisperXIntegration()
        
    def transcribe_with_logging(self, audio_data):
        logger.info("Starting transcription")
        
        try:
            result = self.whisperx.transcribe_audio(audio_data)
            
            logger.info(f"Transcription completed: {result['text'][:50]}...")
            return result
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}", exc_info=True)
            raise e
```

## Testing Integration

### 1. Unit Testing
```python
import unittest
from unittest.mock import Mock, patch

class TestWhisperXIntegration(unittest.TestCase):
    def setUp(self):
        self.whisperx = WhisperXIntegration()
        
    def test_basic_transcription(self):
        # Mock audio data
        audio_data = np.random.randn(16000)  # 1 second of audio
        
        # Mock WhisperX response
        mock_result = {
            'text': 'Hello, world!',
            'language': 'en',
            'segments': []
        }
        
        with patch.object(self.whisperx, 'transcribe_audio', return_value=mock_result):
            result = self.whisperx.transcribe_audio(audio_data)
            
            self.assertEqual(result['text'], 'Hello, world!')
            self.assertEqual(result['language'], 'en')
    
    def test_error_handling(self):
        audio_data = np.random.randn(16000)
        
        with patch.object(self.whisperx, 'transcribe_audio', side_effect=Exception("Test error")):
            with self.assertRaises(Exception):
                self.whisperx.transcribe_audio(audio_data)

if __name__ == '__main__':
    unittest.main()
```

### 2. Integration Testing
```python
class TestWhisperXIntegration:
    def test_websocket_integration(self):
        # Test WebSocket communication
        pass
        
    def test_rest_api_integration(self):
        # Test REST API endpoints
        pass
        
    def test_comfyui_integration(self):
        # Test ComfyUI node integration
        pass
```

This integration guide provides comprehensive information for integrating the WhisperX custom node into various systems and workflows, ensuring optimal performance and reliability.


