# Repository Mapping - Speech System

## Current File Distribution

### Main ComfyUI Repository (QuasiPlanets/ComfyUI)
**Location**: Root directory (current workspace)
**Branch**: `develop-speech`

#### Core Files to Commit:
```
ComfyUI/
├── server.py (WebSocket enhancements)
├── start_websocket_server.py (speech processing)
├── execution.py (audio pipeline integration)
├── nodes.py (speech node registration)
├── folder_paths.py (custom node paths)
├── main.py (speech system initialization)
├── requirements.txt (speech dependencies)
├── elizaos_management.sh (speech system management)
├── COMFYUI-COMMANDS.txt (speech commands)
├── .cursor/ (documentation and guides - MUST COMMIT)
├── api_server/ (speech API endpoints)
├── app/ (speech application logic)
├── comfy_api_nodes/ (speech API nodes)
├── comfy_extras/ (speech utilities)
├── utils/ (speech utilities)
└── custom_nodes/ (symlinks/references to custom nodes)
```

### Custom Node Repositories

#### 1. ComfyUI-UVR5 (QuasiPlanets/ComfyUI-UVR5)
**Location**: `custom_nodes/ComfyUI-UVR5/`
**Branch**: `develop-speech`

**Files to Commit**:
- All files in `custom_nodes/ComfyUI-UVR5/`
- Speech integration modifications
- VAD processing enhancements
- Audio processing utilities
- `.cursor/` directory (if exists) - MUST COMMIT

#### 2. ComfyUI-XTTS (QuasiPlanets/ComfyUI-XTTS)
**Location**: `custom_nodes/ComfyUI-XTTS/`
**Branch**: `develop-speech`

**Files to Commit**:
- All files in `custom_nodes/ComfyUI-XTTS/`
- Speech synthesis enhancements
- Real-time processing modifications
- WebSocket integration
- `.cursor/` directory (contains XTTS documentation) - MUST COMMIT

#### 3. ComfyUI-WhisperX (QuasiPlanets/ComfyUI-WhisperX)
**Location**: `custom_nodes/ComfyUI-WhisperX/`
**Branch**: `develop-speech`

**Files to Commit**:
- All files in `custom_nodes/ComfyUI-WhisperX/`
- Transcription pipeline modifications
- VAD integration
- Audio buffer management
- RMS threshold implementations
- `.cursor/` directory (contains WhisperX documentation) - MUST COMMIT

#### 4. ComfyUI-Manager (QuasiPlanets/ComfyUI-Manager)
**Location**: `custom_nodes/ComfyUI-Manager/`
**Branch**: `develop-speech`

**Files to Commit**:
- All files in `custom_nodes/ComfyUI-Manager/`
- Speech node management
- Installation automation
- Dependency management
- `.cursor/` directory (if exists) - MUST COMMIT

## Commit Process Flow

**⚠️ IMPORTANT: These instructions should ONLY be executed with EXPLICIT USER PERMISSION.**
**⚠️ ALWAYS ask the user before executing any git commands.**

### Phase 1: Custom Node Preparation
For each custom node repository:

1. **Navigate to custom node directory**
   ```bash
   cd custom_nodes/[NODE_NAME]
   ```

2. **Check current status**
   ```bash
   git status
   git remote -v
   ```

3. **Create develop-speech branch**
   ```bash
   git checkout -b develop-speech
   ```

4. **Stage all changes**
   ```bash
   git add .
   ```

5. **Commit with descriptive message**
   ```bash
   git commit -m "feat: speech system integration - [NODE_NAME]

   - VAD implementation with RMS thresholds
   - WebSocket integration for real-time processing
   - Audio buffer management (3-second intervals)
   - Transcription pipeline integration
   - Energy-based voice activity detection
   - RMS threshold=0.01, zcr_threshold=0.05, audio_rms_filter=0.03

   State: FULLY OPERATIONAL"
   ```

6. **Push to remote**
   ```bash
   git push origin develop-speech
   ```

### Phase 2: Main Repository Preparation

1. **Return to ComfyUI root**
   ```bash
   cd /path/to/ComfyUI
   ```

2. **Create develop-speech branch**
   ```bash
   git checkout -b develop-speech
   ```

3. **Stage core changes only**
   ```bash
   # Don't include custom_nodes/ directory content
   git add server.py start_websocket_server.py execution.py nodes.py
   git add folder_paths.py main.py requirements.txt elizaos_management.sh
   git add COMFYUI-COMMANDS.txt .cursor/ api_server/ app/
   git add comfy_api_nodes/ comfy_extras/ utils/
   ```

4. **Commit main repository changes**
   ```bash
   git commit -m "feat: speech system core integration

   - WebSocket server enhancements for speech processing
   - Real-time audio transcription pipeline
   - VAD integration with energy-based detection
   - Custom node management for speech components
   - Audio processing utilities and buffer management
   - Speech-to-text workflow integration

   Dependencies:
   - ComfyUI-UVR5/develop-speech
   - ComfyUI-XTTS/develop-speech  
   - ComfyUI-WhisperX/develop-speech
   - ComfyUI-Manager/develop-speech

   State: FULLY OPERATIONAL"
   ```

5. **Push to remote**
   ```bash
   git push origin develop-speech
   ```

## File Exclusion Rules

### Main Repository Exclusions
- `custom_nodes/[NODE_NAME]/` directories (belong to separate repos)
- `venv/` (virtual environment)
- `__pycache__/` (Python cache)
- `output/` (generated content)
- `temp/` (temporary files)
- `models/` (downloaded models)
- `user/` (user-specific content)

### Custom Node Inclusions
- All Python files
- All configuration files
- All documentation files
- All dependency files
- All integration files

## State Verification Commands

### Pre-Commit Verification
```bash
# Check WebSocket connections
curl -I http://localhost:8189

# Check VAD settings
grep -r "rms_threshold" custom_nodes/ComfyUI-WhisperX/

# Check transcription pipeline
grep -r "whisper" custom_nodes/ComfyUI-WhisperX/

# Check audio processing
grep -r "audio_rms_filter" custom_nodes/ComfyUI-WhisperX/
```

### Post-Commit Verification
```bash
# Verify all branches exist
git branch -r | grep develop-speech

# Check remote connections
git remote -v

# Verify commit messages
git log --oneline -10
```

## Integration Testing Commands

### Fresh Installation Test
```bash
# Clone all repositories
git clone https://github.com/QuasiPlanets/ComfyUI.git
git clone https://github.com/QuasiPlanets/ComfyUI-UVR5.git
git clone https://github.com/QuasiPlanets/ComfyUI-XTTS.git
git clone https://github.com/QuasiPlanets/ComfyUI-WhisperX.git
git clone https://github.com/QuasiPlanets/ComfyUI-Manager.git

# Checkout develop-speech branches
cd ComfyUI && git checkout develop-speech
cd ../ComfyUI-UVR5 && git checkout develop-speech
cd ../ComfyUI-XTTS && git checkout develop-speech
cd ../ComfyUI-WhisperX && git checkout develop-speech
cd ../ComfyUI-Manager && git checkout develop-speech

# Install dependencies
cd ../ComfyUI && pip install -r requirements.txt
```

This mapping ensures precise file distribution and commit process for 100% reproducibility.
