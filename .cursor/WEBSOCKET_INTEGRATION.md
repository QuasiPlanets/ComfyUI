# WebSocket Integration Guide

## Overview
This guide covers the WebSocket integration for real-time audio streaming and transcription in the ComfyUI WhisperX system. The implementation enables browser-to-server communication for live audio processing.

## Architecture

### System Components
```
Browser (Frontend)
    ↓ WebSocket Connection
ComfyUI Server (server.py)
    ↓ Audio Processing
WhisperX Engine
    ↓ Transcription Results
Browser (Frontend)
```

### Message Flow
1. **Browser**: Captures audio and sends via WebSocket
2. **Server**: Receives audio chunks and buffers them
3. **WhisperX**: Processes audio and generates transcription
4. **Server**: Sends results back to browser
5. **Browser**: Displays transcription in real-time

## WebSocket Implementation

### Server-Side (ComfyUI)

#### Modified server.py
```python
# WebSocket handler modifications
import websockets
import json
import asyncio
import whisperx

class WhisperXWebSocketHandler:
    def __init__(self):
        self.audio_buffer = []
        self.buffer_size = 1.5  # seconds
        self.sample_rate = 16000
        self.whisperx_model = None
        
    async def handle_websocket(self, websocket, path):
        """Handle WebSocket connections for audio streaming"""
        try:
            async for message in websocket:
                data = json.loads(message)
                message_type = data.get('type')
                
                if message_type == 'whisperx_audio_chunk':
                    await self.process_audio_chunk(websocket, data)
                elif message_type == 'whisperx_status':
                    await self.send_status(websocket, data)
                    
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")
        except Exception as e:
            print(f"WebSocket error: {e}")
    
    async def process_audio_chunk(self, websocket, data):
        """Process incoming audio chunk"""
        audio_data = data.get('audio')
        timestamp = data.get('timestamp')
        
        # Add to buffer
        self.audio_buffer.append({
            'data': audio_data,
            'timestamp': timestamp
        })
        
        # Check if buffer is full
        if len(self.audio_buffer) >= self.buffer_size * self.sample_rate:
            await self.process_buffer(websocket)
    
    async def process_buffer(self, websocket):
        """Process full audio buffer"""
        if not self.whisperx_model:
            self.whisperx_model = whisperx.load_model("large-v3", device="cuda")
        
        # Combine audio chunks
        combined_audio = self.combine_audio_chunks()
        
        # Process with WhisperX
        result = self.whisperx_model.transcribe(combined_audio)
        
        # Send result back
        await websocket.send(json.dumps({
            'type': 'whisperx_transcription_result',
            'transcription': result['text'],
            'segments': result['segments'],
            'language': result['language']
        }))
        
        # Clear buffer
        self.audio_buffer = []
```

#### Message Types
```python
# Audio streaming message
{
    "type": "whisperx_audio_chunk",
    "audio": "base64_encoded_audio_data",
    "timestamp": 1234567890.123,
    "sample_rate": 16000,
    "channels": 1
}

# Transcription result message
{
    "type": "whisperx_transcription_result",
    "transcription": "Hello, this is a test.",
    "segments": [
        {
            "start": 0.0,
            "end": 2.5,
            "text": "Hello, this is a test."
        }
    ],
    "language": "en",
    "confidence": 0.95
}

# Status message
{
    "type": "whisperx_status",
    "status": "connected|processing|error",
    "message": "Status description",
    "timestamp": 1234567890.123
}
```

### Client-Side (Browser)

#### JavaScript Implementation
```javascript
class WhisperXClient {
    constructor(serverUrl = 'ws://localhost:8188') {
        this.serverUrl = serverUrl;
        this.websocket = null;
        this.mediaRecorder = null;
        this.audioContext = null;
        this.isRecording = false;
        this.onTranscription = null;
        this.onStatus = null;
    }
    
    async connect() {
        try {
            this.websocket = new WebSocket(this.serverUrl);
            
            this.websocket.onopen = () => {
                console.log('WebSocket connected');
                this.sendStatus('connected');
            };
            
            this.websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleMessage(data);
            };
            
            this.websocket.onclose = () => {
                console.log('WebSocket disconnected');
                this.sendStatus('disconnected');
            };
            
            this.websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.sendStatus('error', error.message);
            };
            
        } catch (error) {
            console.error('Connection failed:', error);
            throw error;
        }
    }
    
    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    sampleRate: 16000,
                    channelCount: 1,
                    echoCancellation: true,
                    noiseSuppression: true
                }
            });
            
            this.audioContext = new AudioContext({ sampleRate: 16000 });
            const source = this.audioContext.createMediaStreamSource(stream);
            const processor = this.audioContext.createScriptProcessor(4096, 1, 1);
            
            processor.onaudioprocess = (event) => {
                if (this.isRecording && this.websocket.readyState === WebSocket.OPEN) {
                    const audioData = event.inputBuffer.getChannelData(0);
                    this.sendAudioChunk(audioData);
                }
            };
            
            source.connect(processor);
            processor.connect(this.audioContext.destination);
            
            this.isRecording = true;
            this.sendStatus('recording_started');
            
        } catch (error) {
            console.error('Failed to start recording:', error);
            this.sendStatus('error', error.message);
        }
    }
    
    stopRecording() {
        this.isRecording = false;
        if (this.audioContext) {
            this.audioContext.close();
            this.audioContext = null;
        }
        this.sendStatus('recording_stopped');
    }
    
    sendAudioChunk(audioData) {
        const message = {
            type: 'whisperx_audio_chunk',
            audio: this.audioToBase64(audioData),
            timestamp: Date.now() / 1000,
            sample_rate: 16000,
            channels: 1
        };
        
        this.websocket.send(JSON.stringify(message));
    }
    
    audioToBase64(audioData) {
        const buffer = new ArrayBuffer(audioData.length * 2);
        const view = new DataView(buffer);
        
        for (let i = 0; i < audioData.length; i++) {
            view.setInt16(i * 2, audioData[i] * 32767, true);
        }
        
        return btoa(String.fromCharCode(...new Uint8Array(buffer)));
    }
    
    handleMessage(data) {
        switch (data.type) {
            case 'whisperx_transcription_result':
                if (this.onTranscription) {
                    this.onTranscription(data);
                }
                break;
                
            case 'whisperx_status':
                if (this.onStatus) {
                    this.onStatus(data);
                }
                break;
                
            default:
                console.log('Unknown message type:', data.type);
        }
    }
    
    sendStatus(status, message = '') {
        const statusMessage = {
            type: 'whisperx_status',
            status: status,
            message: message,
            timestamp: Date.now() / 1000
        };
        
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            this.websocket.send(JSON.stringify(statusMessage));
        }
    }
    
    disconnect() {
        if (this.websocket) {
            this.websocket.close();
            this.websocket = null;
        }
    }
}
```

#### HTML Integration
```html
<!DOCTYPE html>
<html>
<head>
    <title>WhisperX Live Transcription</title>
</head>
<body>
    <div id="controls">
        <button id="connectBtn">Connect</button>
        <button id="recordBtn" disabled>Start Recording</button>
        <button id="stopBtn" disabled>Stop Recording</button>
        <button id="disconnectBtn" disabled>Disconnect</button>
    </div>
    
    <div id="status">Status: Disconnected</div>
    
    <div id="transcription">
        <h3>Live Transcription:</h3>
        <div id="transcriptionText"></div>
    </div>
    
    <script>
        const client = new WhisperXClient();
        
        // Event handlers
        document.getElementById('connectBtn').onclick = async () => {
            try {
                await client.connect();
                document.getElementById('recordBtn').disabled = false;
                document.getElementById('disconnectBtn').disabled = false;
                document.getElementById('connectBtn').disabled = true;
            } catch (error) {
                console.error('Connection failed:', error);
            }
        };
        
        document.getElementById('recordBtn').onclick = async () => {
            await client.startRecording();
            document.getElementById('recordBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;
        };
        
        document.getElementById('stopBtn').onclick = () => {
            client.stopRecording();
            document.getElementById('recordBtn').disabled = false;
            document.getElementById('stopBtn').disabled = true;
        };
        
        document.getElementById('disconnectBtn').onclick = () => {
            client.disconnect();
            document.getElementById('recordBtn').disabled = true;
            document.getElementById('stopBtn').disabled = true;
            document.getElementById('disconnectBtn').disabled = true;
            document.getElementById('connectBtn').disabled = false;
        };
        
        // Callbacks
        client.onTranscription = (data) => {
            const textDiv = document.getElementById('transcriptionText');
            textDiv.innerHTML += `<p><strong>${new Date().toLocaleTimeString()}:</strong> ${data.transcription}</p>`;
            textDiv.scrollTop = textDiv.scrollHeight;
        };
        
        client.onStatus = (data) => {
            document.getElementById('status').textContent = `Status: ${data.status} - ${data.message}`;
        };
    </script>
</body>
</html>
```

## Audio Processing

### Audio Format Requirements
```python
# Audio specifications
SAMPLE_RATE = 16000      # Hz
CHANNELS = 1             # Mono
FORMAT = "PCM"           # Pulse Code Modulation
BIT_DEPTH = 16           # bits per sample
BUFFER_SIZE = 1.5        # seconds
```

### Audio Buffer Management
```python
class AudioBuffer:
    def __init__(self, buffer_size=1.5, sample_rate=16000):
        self.buffer_size = buffer_size
        self.sample_rate = sample_rate
        self.max_samples = int(buffer_size * sample_rate)
        self.buffer = []
        self.timestamps = []
    
    def add_chunk(self, audio_data, timestamp):
        """Add audio chunk to buffer"""
        self.buffer.extend(audio_data)
        self.timestamps.append(timestamp)
        
        # Remove old data if buffer is full
        if len(self.buffer) > self.max_samples:
            excess = len(self.buffer) - self.max_samples
            self.buffer = self.buffer[excess:]
            self.timestamps = self.timestamps[1:]
    
    def is_full(self):
        """Check if buffer is ready for processing"""
        return len(self.buffer) >= self.max_samples
    
    def get_buffer(self):
        """Get current buffer data"""
        return np.array(self.buffer, dtype=np.float32)
    
    def clear(self):
        """Clear buffer"""
        self.buffer = []
        self.timestamps = []
```

### Silence Detection
```python
def detect_silence(audio_data, threshold=0.03):
    """Detect if audio chunk is silence"""
    rms = np.sqrt(np.mean(np.square(audio_data)))
    return rms < threshold

def process_audio_with_silence_detection(audio_chunk):
    """Process audio with silence detection"""
    if detect_silence(audio_chunk):
        return None  # Skip silent chunks
    
    return audio_chunk
```

## Error Handling

### Connection Management
```python
class WebSocketManager:
    def __init__(self):
        self.connections = set()
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        
    async def handle_connection(self, websocket, path):
        """Handle new WebSocket connection"""
        self.connections.add(websocket)
        try:
            await self.send_status(websocket, "connected")
            await self.message_loop(websocket)
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed normally")
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            self.connections.discard(websocket)
    
    async def message_loop(self, websocket):
        """Main message processing loop"""
        async for message in websocket:
            try:
                await self.process_message(websocket, message)
            except Exception as e:
                await self.send_error(websocket, str(e))
    
    async def send_error(self, websocket, error_message):
        """Send error message to client"""
        error_data = {
            "type": "whisperx_error",
            "error": error_message,
            "timestamp": time.time()
        }
        await websocket.send(json.dumps(error_data))
```

### Retry Logic
```python
class RetryManager:
    def __init__(self, max_retries=3, delay=1.0):
        self.max_retries = max_retries
        self.delay = delay
    
    async def retry_operation(self, operation, *args, **kwargs):
        """Retry operation with exponential backoff"""
        for attempt in range(self.max_retries):
            try:
                return await operation(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                
                wait_time = self.delay * (2 ** attempt)
                await asyncio.sleep(wait_time)
```

## Performance Optimization

### Memory Management
```python
class MemoryManager:
    def __init__(self):
        self.audio_buffers = {}
        self.max_buffers = 10
    
    def cleanup_old_buffers(self):
        """Clean up old audio buffers"""
        if len(self.audio_buffers) > self.max_buffers:
            oldest_key = min(self.audio_buffers.keys())
            del self.audio_buffers[oldest_key]
    
    def clear_all_buffers(self):
        """Clear all audio buffers"""
        self.audio_buffers.clear()
        torch.cuda.empty_cache()
```

### Batch Processing
```python
class BatchProcessor:
    def __init__(self, batch_size=4):
        self.batch_size = batch_size
        self.pending_chunks = []
    
    async def add_chunk(self, audio_chunk):
        """Add audio chunk to batch"""
        self.pending_chunks.append(audio_chunk)
        
        if len(self.pending_chunks) >= self.batch_size:
            await self.process_batch()
    
    async def process_batch(self):
        """Process batch of audio chunks"""
        if not self.pending_chunks:
            return
        
        # Combine chunks
        combined_audio = np.concatenate(self.pending_chunks)
        
        # Process with WhisperX
        result = await self.transcribe_audio(combined_audio)
        
        # Send results
        await self.send_results(result)
        
        # Clear batch
        self.pending_chunks = []
```

## Security Considerations

### Input Validation
```python
def validate_audio_message(data):
    """Validate incoming audio message"""
    required_fields = ['type', 'audio', 'timestamp']
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    if data['type'] != 'whisperx_audio_chunk':
        raise ValueError(f"Invalid message type: {data['type']}")
    
    # Validate audio data
    try:
        audio_data = base64.b64decode(data['audio'])
        if len(audio_data) > MAX_AUDIO_SIZE:
            raise ValueError("Audio data too large")
    except Exception as e:
        raise ValueError(f"Invalid audio data: {e}")
    
    return True
```

### Rate Limiting
```python
class RateLimiter:
    def __init__(self, max_requests=100, window=60):
        self.max_requests = max_requests
        self.window = window
        self.requests = {}
    
    def is_allowed(self, client_id):
        """Check if client is within rate limits"""
        now = time.time()
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests.get(client_id, [])
            if now - req_time < self.window
        ]
        
        # Check limit
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[client_id].append(now)
        return True
```

## Testing

### Unit Tests
```python
import unittest
import asyncio
from unittest.mock import Mock, patch

class TestWebSocketHandler(unittest.TestCase):
    def setUp(self):
        self.handler = WhisperXWebSocketHandler()
    
    async def test_audio_chunk_processing(self):
        """Test audio chunk processing"""
        websocket = Mock()
        data = {
            'type': 'whisperx_audio_chunk',
            'audio': 'base64_audio_data',
            'timestamp': 1234567890.123
        }
        
        await self.handler.process_audio_chunk(websocket, data)
        
        # Verify audio was added to buffer
        self.assertEqual(len(self.handler.audio_buffer), 1)
    
    async def test_transcription_result(self):
        """Test transcription result handling"""
        websocket = Mock()
        result = {
            'transcription': 'Test transcription',
            'segments': [],
            'language': 'en'
        }
        
        await self.handler.send_transcription_result(websocket, result)
        
        # Verify message was sent
        websocket.send.assert_called_once()
```

### Integration Tests
```python
class TestWebSocketIntegration(unittest.TestCase):
    async def test_full_workflow(self):
        """Test complete WebSocket workflow"""
        # Start server
        server = await websockets.serve(
            self.handler.handle_websocket,
            "localhost",
            8188
        )
        
        # Connect client
        async with websockets.connect('ws://localhost:8188') as websocket:
            # Send audio chunk
            await websocket.send(json.dumps({
                'type': 'whisperx_audio_chunk',
                'audio': 'test_audio_data',
                'timestamp': time.time()
            }))
            
            # Receive response
            response = await websocket.recv()
            data = json.loads(response)
            
            # Verify response
            self.assertEqual(data['type'], 'whisperx_transcription_result')
        
        server.close()
        await server.wait_closed()
```

## Monitoring and Logging

### Logging Configuration
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('websocket.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('whisperx_websocket')

# Usage
logger.info("WebSocket connection established")
logger.error("Transcription failed", exc_info=True)
```

### Performance Monitoring
```python
import time
import psutil

class PerformanceMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
    
    def record_request(self):
        """Record a successful request"""
        self.request_count += 1
    
    def record_error(self):
        """Record an error"""
        self.error_count += 1
    
    def get_stats(self):
        """Get performance statistics"""
        uptime = time.time() - self.start_time
        return {
            'uptime': uptime,
            'requests_per_second': self.request_count / uptime,
            'error_rate': self.error_count / max(self.request_count, 1),
            'memory_usage': psutil.Process().memory_info().rss / 1024 / 1024
        }
```

This WebSocket integration guide provides comprehensive information for implementing real-time audio streaming and transcription in the ComfyUI WhisperX system.


