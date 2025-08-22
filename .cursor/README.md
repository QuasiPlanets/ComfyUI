# ComfyUI Development Environment - Cursor AI Documentation

## Project Overview
This is a ComfyUI development environment with live WhisperX transcription capabilities, designed for real-time audio processing and AI workflow integration. The project includes multiple custom nodes and has undergone extensive development to resolve dependency conflicts and achieve optimal performance.

## Key Components

### Core ComfyUI
- **Version**: Latest stable with custom modifications
- **Purpose**: AI workflow orchestration and execution
- **Key Features**: Node-based workflow system, GPU acceleration, real-time processing

### Custom Nodes
1. **ComfyUI-WhisperX**: Live audio transcription with GPU acceleration
2. **ComfyUI-XTTS**: Text-to-speech synthesis
3. **ComfyUI-UVR5**: Audio source separation
4. **ComfyUI-Manager**: Node and model management
5. **comfyui_ultimatesdupscale**: Image upscaling

## Development History

### Phase 1: Initial Setup
- Basic ComfyUI installation
- Custom node integration
- Initial dependency conflicts

### Phase 2: Dependency Resolution
- **NumPy Conflict**: Resolved version conflicts between TTS (required 1.22.0) and newer packages (required >=1.24)
- **Solution**: Using NumPy 1.26.4 (compatible with all components)
- **Impact**: All custom nodes now work without conflicts

### Phase 3: GPU Acceleration Issues
- **cuDNN Conflict**: WhisperX needed system cuDNN 8.x, but only PyTorch's bundled cuDNN 9.x was available
- **Solution**: Installed system cuDNN 8.9.3 alongside PyTorch's bundled cuDNN 9.x
- **Impact**: WhisperX now works without crashes, PyTorch unaffected

### Phase 4: WebSocket Integration
- Real-time audio streaming implementation
- Browser-to-server communication
- Audio buffering and processing optimization

### Phase 5: ElizaOS Integration
- External system integration
- Audio quality optimization
- Connection stability improvements

## Current Status
✅ **Fully Functional**: All custom nodes working
✅ **GPU Accelerated**: WhisperX using CUDA 12.1
✅ **Dependency Resolved**: No conflicts
✅ **Real-time Processing**: Live transcription operational
✅ **100% Reproducible**: Complete deployment documentation

## File Structure
```
.cursor/
├── README.md                           # This file
├── DEPLOYMENT_GUIDE.md                 # Complete setup instructions
├── DEVELOPMENT_HISTORY.md              # Detailed development timeline
├── TROUBLESHOOTING.md                  # Common issues and solutions
├── CUSTOM_NODES_GUIDE.md              # Custom node documentation
├── WEBSOCKET_INTEGRATION.md            # Real-time communication guide
├── ELIZAOS_INTEGRATION.md              # External system integration
├── COMMIT_MANAGEMENT_GUIDE.md          # Commit strategy and best practices
├── REPOSITORY_MAPPING.md               # File distribution and commit process
├── SPEECH_SYSTEM_STATE.md              # Current operational state
├── COMMIT_EXECUTION_PLAN.md            # Step-by-step commit instructions
├── CURSOR_DIRECTORY_COMMIT_GUIDE.md    # .cursor directory management
├── GIT_REPOSITORY_VERIFICATION.md      # Repository status and verification
├── LLM_SAFETY_GUIDELINES.md            # Critical safety rules for LLMs
└── custom_nodes/
    └── ComfyUI-WhisperX/
        ├── README.md                   # WhisperX specific documentation
        ├── DEVELOPMENT_LOG.md          # Detailed development history
        ├── INTEGRATION_GUIDE.md        # Integration instructions
        ├── TROUBLESHOOTING.md          # WhisperX specific issues
        └── API_REFERENCE.md            # API documentation
```

## Quick Start
1. **Build Container**: `docker-compose build`
2. **Start Services**: `docker-compose up -d`
3. **Access ComfyUI**: http://localhost:8188
4. **Test WhisperX**: Use SimpleLiveTranscription node

## Key Technologies
- **CUDA**: 12.1.1 for GPU acceleration
- **PyTorch**: 2.7.1 with CUDA support
- **WhisperX**: 3.4.2 for transcription
- **WebSockets**: Real-time communication
- **Docker**: Containerized development environment

## Performance Metrics
- **WhisperX GPU Memory**: ~5.6MB
- **Transcription Speed**: Real-time
- **Audio Buffer**: 1.5 seconds
- **Silence Detection**: RMS threshold 0.03

## Future Development
- ElizaOS integration optimization
- Additional custom nodes
- Performance improvements
- Extended language support


