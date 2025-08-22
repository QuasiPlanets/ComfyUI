# ElizaOS Integration Guide

## Overview
This guide covers the integration of ElizaOS with the ComfyUI WhisperX system for enhanced audio processing and response generation. ElizaOS provides additional audio capture capabilities and response generation that complements the WhisperX transcription system.

## Architecture

### System Integration
```
ElizaOS (Audio Capture)
    ↓ Audio Stream
ComfyUI WhisperX (Transcription)
    ↓ Transcribed Text
ElizaOS (Response Generation)
    ↓ Response Audio
User Interface
```

### Data Flow
1. **ElizaOS**: Captures high-quality audio input
2. **ComfyUI**: Receives audio and processes with WhisperX
3. **WhisperX**: Generates accurate transcription
4. **ElizaOS**: Processes transcription and generates response
5. **System**: Delivers response to user

## Integration Components

### 1. Audio Capture Integration

#### ElizaOS Audio Capture
```python
class ElizaOSAudioCapture:
    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.audio_buffer = []
        self.is_capturing = False
        
    def start_capture(self):
        """Start audio capture from ElizaOS"""
        self.is_capturing = True
        # Initialize ElizaOS audio capture
        # Configure audio parameters for optimal quality
        
    def stop_capture(self):
        """Stop audio capture"""
        self.is_capturing = False
        
    def get_audio_chunk(self):
        """Get audio chunk from ElizaOS"""
        if not self.is_capturing:
            return None
            
        # Retrieve audio data from ElizaOS
        audio_data = self.retrieve_from_elizaos()
        return audio_data
        
    def retrieve_from_elizaos(self):
        """Retrieve audio data from ElizaOS system"""
        # Implementation depends on ElizaOS API
        # This is a placeholder for the actual integration
        pass
```

#### Audio Quality Optimization
```python
class AudioQualityOptimizer:
    def __init__(self):
        self.noise_reduction = True
        self.echo_cancellation = True
        self.gain_control = True
        
    def optimize_audio(self, audio_data):
        """Optimize audio quality for transcription"""
        # Apply noise reduction
        if self.noise_reduction:
            audio_data = self.apply_noise_reduction(audio_data)
            
        # Apply echo cancellation
        if self.echo_cancellation:
            audio_data = self.apply_echo_cancellation(audio_data)
            
        # Apply gain control
        if self.gain_control:
            audio_data = self.apply_gain_control(audio_data)
            
        return audio_data
        
    def apply_noise_reduction(self, audio_data):
        """Apply noise reduction algorithm"""
        # Implementation for noise reduction
        return audio_data
        
    def apply_echo_cancellation(self, audio_data):
        """Apply echo cancellation"""
        # Implementation for echo cancellation
        return audio_data
        
    def apply_gain_control(self, audio_data):
        """Apply automatic gain control"""
        # Implementation for gain control
        return audio_data
```

### 2. Response Generation Integration

#### ElizaOS Response System
```python
class ElizaOSResponseGenerator:
    def __init__(self):
        self.response_models = {}
        self.context_history = []
        self.max_history = 10
        
    def generate_response(self, transcription, context=None):
        """Generate response based on transcription"""
        # Add to context history
        self.add_to_history(transcription, context)
        
        # Generate response using ElizaOS
        response = self.process_with_elizaos(transcription)
        
        return response
        
    def add_to_history(self, transcription, context):
        """Add transcription to context history"""
        entry = {
            'transcription': transcription,
            'context': context,
            'timestamp': time.time()
        }
        
        self.context_history.append(entry)
        
        # Maintain history size
        if len(self.context_history) > self.max_history:
            self.context_history.pop(0)
            
    def process_with_elizaos(self, transcription):
        """Process transcription with ElizaOS"""
        # Send transcription to ElizaOS for processing
        # This is a placeholder for the actual ElizaOS integration
        response = self.send_to_elizaos(transcription)
        return response
        
    def send_to_elizaos(self, transcription):
        """Send transcription to ElizaOS system"""
        # Implementation depends on ElizaOS API
        # This is a placeholder for the actual integration
        pass
```

### 3. Connection Management

#### ElizaOS Connection Manager
```python
class ElizaOSConnectionManager:
    def __init__(self, elizaos_url, timeout=30):
        self.elizaos_url = elizaos_url
        self.timeout = timeout
        self.connection = None
        self.is_connected = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        
    async def connect(self):
        """Establish connection to ElizaOS"""
        try:
            # Establish connection to ElizaOS
            self.connection = await self.create_connection()
            self.is_connected = True
            self.reconnect_attempts = 0
            print("Connected to ElizaOS")
            
        except Exception as e:
            print(f"Failed to connect to ElizaOS: {e}")
            await self.handle_connection_error()
            
    async def create_connection(self):
        """Create connection to ElizaOS"""
        # Implementation depends on ElizaOS connection method
        # This could be WebSocket, HTTP, or other protocol
        pass
        
    async def disconnect(self):
        """Disconnect from ElizaOS"""
        if self.connection:
            await self.connection.close()
            self.connection = None
            self.is_connected = False
            print("Disconnected from ElizaOS")
            
    async def handle_connection_error(self):
        """Handle connection errors with retry logic"""
        if self.reconnect_attempts < self.max_reconnect_attempts:
            self.reconnect_attempts += 1
            wait_time = 2 ** self.reconnect_attempts  # Exponential backoff
            print(f"Reconnecting to ElizaOS in {wait_time} seconds...")
            await asyncio.sleep(wait_time)
            await self.connect()
        else:
            print("Max reconnection attempts reached")
            
    async def send_message(self, message):
        """Send message to ElizaOS"""
        if not self.is_connected:
            await self.connect()
            
        try:
            response = await self.connection.send(message)
            return response
        except Exception as e:
            print(f"Error sending message to ElizaOS: {e}")
            await self.handle_connection_error()
            return None
```

## Integration Workflow

### Complete Integration Pipeline
```python
class ElizaOSWhisperXIntegration:
    def __init__(self):
        self.audio_capture = ElizaOSAudioCapture()
        self.quality_optimizer = AudioQualityOptimizer()
        self.response_generator = ElizaOSResponseGenerator()
        self.connection_manager = ElizaOSConnectionManager("ws://elizaos:8080")
        self.whisperx_model = None
        
    async def initialize(self):
        """Initialize the integration"""
        # Connect to ElizaOS
        await self.connection_manager.connect()
        
        # Initialize WhisperX
        self.whisperx_model = whisperx.load_model("large-v3", device="cuda")
        
        print("ElizaOS WhisperX integration initialized")
        
    async def process_audio_stream(self):
        """Process audio stream from ElizaOS"""
        self.audio_capture.start_capture()
        
        while True:
            # Get audio chunk from ElizaOS
            audio_chunk = self.audio_capture.get_audio_chunk()
            
            if audio_chunk is None:
                continue
                
            # Optimize audio quality
            optimized_audio = self.quality_optimizer.optimize_audio(audio_chunk)
            
            # Process with WhisperX
            transcription = await self.transcribe_audio(optimized_audio)
            
            if transcription:
                # Generate response with ElizaOS
                response = self.response_generator.generate_response(transcription)
                
                # Send response back
                await self.send_response(response)
                
    async def transcribe_audio(self, audio_data):
        """Transcribe audio using WhisperX"""
        try:
            result = self.whisperx_model.transcribe(audio_data)
            return result['text']
        except Exception as e:
            print(f"Transcription error: {e}")
            return None
            
    async def send_response(self, response):
        """Send response back to user"""
        # Implementation depends on how response should be delivered
        # This could be audio playback, text display, etc.
        pass
        
    async def cleanup(self):
        """Cleanup resources"""
        self.audio_capture.stop_capture()
        await self.connection_manager.disconnect()
```

## Configuration

### ElizaOS Configuration
```python
# elizaos_config.py
class ElizaOSConfig:
    # Connection settings
    ELIZAOS_URL = "ws://elizaos:8080"
    CONNECTION_TIMEOUT = 30
    MAX_RECONNECT_ATTEMPTS = 5
    
    # Audio settings
    SAMPLE_RATE = 16000
    CHANNELS = 1
    BUFFER_SIZE = 1.5
    
    # Quality settings
    NOISE_REDUCTION = True
    ECHO_CANCELLATION = True
    GAIN_CONTROL = True
    
    # Response settings
    MAX_CONTEXT_HISTORY = 10
    RESPONSE_TIMEOUT = 10
    
    # WhisperX settings
    WHISPERX_MODEL = "large-v3"
    WHISPERX_DEVICE = "cuda"
    WHISPERX_COMPUTE_TYPE = "float16"
```

### Environment Variables
```bash
# .env file
ELIZAOS_URL=ws://elizaos:8080
ELIZAOS_API_KEY=your_api_key_here
ELIZAOS_TIMEOUT=30
WHISPERX_MODEL=large-v3
AUDIO_SAMPLE_RATE=16000
```

## Error Handling

### Connection Error Handling
```python
class ElizaOSErrorHandler:
    def __init__(self):
        self.error_count = 0
        self.max_errors = 10
        self.error_window = 300  # 5 minutes
        
    def handle_connection_error(self, error):
        """Handle connection errors"""
        self.error_count += 1
        
        if self.error_count > self.max_errors:
            print("Too many errors, stopping integration")
            return False
            
        print(f"Connection error: {error}")
        return True
        
    def handle_audio_error(self, error):
        """Handle audio processing errors"""
        print(f"Audio processing error: {error}")
        # Implement audio error recovery
        
    def handle_transcription_error(self, error):
        """Handle transcription errors"""
        print(f"Transcription error: {error}")
        # Implement transcription error recovery
        
    def reset_error_count(self):
        """Reset error count after successful operation"""
        self.error_count = 0
```

### Retry Logic
```python
class ElizaOSRetryManager:
    def __init__(self, max_retries=3, base_delay=1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        
    async def retry_operation(self, operation, *args, **kwargs):
        """Retry operation with exponential backoff"""
        for attempt in range(self.max_retries):
            try:
                return await operation(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                    
                delay = self.base_delay * (2 ** attempt)
                print(f"Retry {attempt + 1}/{self.max_retries} in {delay}s")
                await asyncio.sleep(delay)
```

## Performance Optimization

### Audio Processing Optimization
```python
class AudioProcessingOptimizer:
    def __init__(self):
        self.buffer_size = 1.5
        self.sample_rate = 16000
        self.audio_buffer = []
        
    def optimize_buffer_size(self, audio_data):
        """Optimize buffer size for processing"""
        # Ensure buffer size is optimal for WhisperX
        target_samples = int(self.buffer_size * self.sample_rate)
        
        if len(audio_data) < target_samples:
            # Pad with silence
            padding = np.zeros(target_samples - len(audio_data))
            audio_data = np.concatenate([audio_data, padding])
        elif len(audio_data) > target_samples:
            # Truncate to target size
            audio_data = audio_data[:target_samples]
            
        return audio_data
        
    def optimize_audio_format(self, audio_data):
        """Optimize audio format for processing"""
        # Convert to float32 if needed
        if audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32)
            
        # Normalize audio
        if np.max(np.abs(audio_data)) > 0:
            audio_data = audio_data / np.max(np.abs(audio_data))
            
        return audio_data
```

### Memory Management
```python
class ElizaOSMemoryManager:
    def __init__(self):
        self.audio_buffers = {}
        self.response_cache = {}
        self.max_buffers = 20
        self.max_cache_size = 100
        
    def cleanup_old_buffers(self):
        """Clean up old audio buffers"""
        if len(self.audio_buffers) > self.max_buffers:
            # Remove oldest buffers
            oldest_keys = sorted(self.audio_buffers.keys())[:len(self.audio_buffers) - self.max_buffers]
            for key in oldest_keys:
                del self.audio_buffers[key]
                
    def cleanup_response_cache(self):
        """Clean up response cache"""
        if len(self.response_cache) > self.max_cache_size:
            # Remove oldest responses
            oldest_keys = sorted(self.response_cache.keys())[:len(self.response_cache) - self.max_cache_size]
            for key in oldest_keys:
                del self.response_cache[key]
                
    def clear_all(self):
        """Clear all cached data"""
        self.audio_buffers.clear()
        self.response_cache.clear()
        torch.cuda.empty_cache()
```

## Testing

### Integration Testing
```python
class TestElizaOSIntegration:
    def setUp(self):
        self.integration = ElizaOSWhisperXIntegration()
        
    async def test_audio_capture(self):
        """Test audio capture from ElizaOS"""
        # Mock ElizaOS audio capture
        audio_data = np.random.randn(16000)  # 1 second of audio
        
        # Test audio optimization
        optimized_audio = self.integration.quality_optimizer.optimize_audio(audio_data)
        
        # Verify audio format
        self.assertEqual(optimized_audio.dtype, np.float32)
        self.assertTrue(np.max(np.abs(optimized_audio)) <= 1.0)
        
    async def test_transcription_workflow(self):
        """Test complete transcription workflow"""
        # Mock transcription
        transcription = "Hello, this is a test."
        
        # Test response generation
        response = self.integration.response_generator.generate_response(transcription)
        
        # Verify response
        self.assertIsNotNone(response)
        
    async def test_connection_management(self):
        """Test connection management"""
        # Test connection
        await self.integration.connection_manager.connect()
        self.assertTrue(self.integration.connection_manager.is_connected)
        
        # Test disconnection
        await self.integration.connection_manager.disconnect()
        self.assertFalse(self.integration.connection_manager.is_connected)
```

### Performance Testing
```python
class PerformanceTest:
    def __init__(self):
        self.start_time = time.time()
        self.operation_times = []
        
    def measure_operation(self, operation_name):
        """Measure operation execution time"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                start = time.time()
                result = await func(*args, **kwargs)
                end = time.time()
                
                execution_time = end - start
                self.operation_times.append({
                    'operation': operation_name,
                    'time': execution_time
                })
                
                return result
            return wrapper
        return decorator
        
    def get_performance_stats(self):
        """Get performance statistics"""
        total_time = time.time() - self.start_time
        
        stats = {
            'total_time': total_time,
            'operations': len(self.operation_times),
            'average_time': np.mean([op['time'] for op in self.operation_times]),
            'max_time': np.max([op['time'] for op in self.operation_times]),
            'min_time': np.min([op['time'] for op in self.operation_times])
        }
        
        return stats
```

## Monitoring and Logging

### Integration Monitoring
```python
class ElizaOSMonitor:
    def __init__(self):
        self.metrics = {
            'audio_chunks_processed': 0,
            'transcriptions_generated': 0,
            'responses_generated': 0,
            'connection_errors': 0,
            'processing_errors': 0
        }
        
    def record_metric(self, metric_name, value=1):
        """Record a metric"""
        if metric_name in self.metrics:
            self.metrics[metric_name] += value
            
    def get_metrics(self):
        """Get current metrics"""
        return self.metrics.copy()
        
    def reset_metrics(self):
        """Reset all metrics"""
        for key in self.metrics:
            self.metrics[key] = 0
```

### Logging Configuration
```python
import logging

# Configure logging for ElizaOS integration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('elizaos_integration.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('elizaos_integration')

# Usage examples
logger.info("ElizaOS integration started")
logger.debug("Processing audio chunk")
logger.error("Connection failed", exc_info=True)
```

## Deployment

### Docker Integration
```dockerfile
# Dockerfile for ElizaOS integration
FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy application
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose ports
EXPOSE 8188 8189

# Start application
CMD ["python", "main.py", "--listen", "0.0.0.0", "--port", "8188"]
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  comfyui-whisperx:
    build: .
    ports:
      - "8188:8188"
      - "8189:8189"
    environment:
      - ELIZAOS_URL=ws://elizaos:8080
      - CUDA_VISIBLE_DEVICES=0
    volumes:
      - ./models:/app/models
      - ./output:/app/output
    depends_on:
      - elizaos
      
  elizaos:
    image: elizaos:latest
    ports:
      - "8080:8080"
    environment:
      - ELIZAOS_CONFIG=/config/elizaos.conf
    volumes:
      - ./elizaos_config:/config
```

## Troubleshooting

### Common Issues

#### Connection Issues
**Problem**: Cannot connect to ElizaOS
**Solution**: 
- Check ElizaOS service status
- Verify network connectivity
- Check firewall settings
- Validate connection URL

#### Audio Quality Issues
**Problem**: Poor transcription quality
**Solution**:
- Optimize audio capture settings
- Enable noise reduction
- Adjust gain control
- Check microphone quality

#### Performance Issues
**Problem**: Slow response times
**Solution**:
- Optimize buffer sizes
- Enable GPU acceleration
- Reduce model complexity
- Implement caching

### Debug Commands
```bash
# Check ElizaOS connection
curl -I http://elizaos:8080/health

# Check audio devices
python -c "import sounddevice; print(sounddevice.query_devices())"

# Monitor GPU usage
nvidia-smi

# Check logs
tail -f elizaos_integration.log
```

This ElizaOS integration guide provides comprehensive information for integrating ElizaOS with the ComfyUI WhisperX system, ensuring optimal performance and reliability.


