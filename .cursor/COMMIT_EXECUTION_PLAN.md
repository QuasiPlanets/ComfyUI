# Commit Execution Plan - Speech System

## Overview
This plan provides step-by-step instructions to commit all current changes to `develop-speech` branches across all repositories, ensuring 100% reproducibility of the current operational state.

## Prerequisites
- All repositories cloned and accessible
- Current working state verified and operational
- Git credentials configured for all repositories
- Network access to push to remote repositories

## .cursor Directory Requirements
- All `.cursor/` directories MUST be committed
- No .gitignore exclusions for .cursor directories
- Documentation in .cursor directories is critical for future LLMs
- Each repository should include its relevant .cursor documentation

## Execution Order (CRITICAL)

### Phase 1: Custom Node Repositories (Dependencies First)

#### Step 1: ComfyUI-UVR5
```bash
# Navigate to UVR5 custom node
cd custom_nodes/ComfyUI-UVR5

# Verify current status
git status
git remote -v

# Create develop-speech branch
git checkout -b develop-speech

# Stage all changes
git add .

# Commit with descriptive message
git commit -m "feat: speech system integration - UVR5

- VAD implementation with RMS thresholds
- WebSocket integration for real-time processing
- Audio buffer management (3-second intervals)
- Transcription pipeline integration
- Energy-based voice activity detection
- RMS threshold=0.01, zcr_threshold=0.05, audio_rms_filter=0.03
- Audio processing utilities for speech enhancement

State: FULLY OPERATIONAL"

# Push to remote
git push origin develop-speech
```

#### Step 2: ComfyUI-XTTS
```bash
# Navigate to XTTS custom node
cd ../ComfyUI-XTTS

# Verify current status
git status
git remote -v

# Create develop-speech branch
git checkout -b develop-speech

# Stage all changes
git add .

# Commit with descriptive message
git commit -m "feat: speech system integration - XTTS

- VAD implementation with RMS thresholds
- WebSocket integration for real-time processing
- Audio buffer management (3-second intervals)
- Transcription pipeline integration
- Energy-based voice activity detection
- RMS threshold=0.01, zcr_threshold=0.05, audio_rms_filter=0.03
- Text-to-speech synthesis enhancements
- Real-time processing modifications

State: FULLY OPERATIONAL"

# Push to remote
git push origin develop-speech
```

#### Step 3: ComfyUI-WhisperX
```bash
# Navigate to WhisperX custom node
cd ../ComfyUI-WhisperX

# Verify current status
git status
git remote -v

# Create develop-speech branch
git checkout -b develop-speech

# Stage all changes
git add .

# Commit with descriptive message
git commit -m "feat: speech system integration - WhisperX

- VAD implementation with RMS thresholds
- WebSocket integration for real-time processing
- Audio buffer management (3-second intervals)
- Transcription pipeline integration
- Energy-based voice activity detection
- RMS threshold=0.01, zcr_threshold=0.05, audio_rms_filter=0.03
- Speech-to-text transcription with WhisperX
- Audio buffer management and processing
- RMS threshold implementations for VAD

State: FULLY OPERATIONAL"

# Push to remote
git push origin develop-speech
```

#### Step 4: ComfyUI-Manager
```bash
# Navigate to Manager custom node
cd ../ComfyUI-Manager

# Verify current status
git status
git remote -v

# Create develop-speech branch
git checkout -b develop-speech

# Stage all changes
git add .

# Commit with descriptive message
git commit -m "feat: speech system integration - Manager

- VAD implementation with RMS thresholds
- WebSocket integration for real-time processing
- Audio buffer management (3-second intervals)
- Transcription pipeline integration
- Energy-based voice activity detection
- RMS threshold=0.01, zcr_threshold=0.05, audio_rms_filter=0.03
- Speech node management and installation
- Dependency resolution for speech components
- Custom node automation for speech system

State: FULLY OPERATIONAL"

# Push to remote
git push origin develop-speech
```

### Phase 2: Main ComfyUI Repository (Depends on Custom Nodes)

#### Step 5: Main ComfyUI Repository
```bash
# Return to ComfyUI root directory
cd /path/to/ComfyUI

# Verify current status
git status
git remote -v

# Create develop-speech branch
git checkout -b develop-speech

# Stage core changes (exclude custom_nodes content)
git add server.py
git add start_websocket_server.py
git add execution.py
git add nodes.py
git add folder_paths.py
git add main.py
git add requirements.txt
git add elizaos_management.sh
git add COMFYUI-COMMANDS.txt
git add .cursor/  # CRITICAL: Must include all documentation
git add api_server/
git add app/
git add comfy_api_nodes/
git add comfy_extras/
git add utils/

# Commit with comprehensive message
git commit -m "feat: speech system core integration

- WebSocket server enhancements for speech processing
- Real-time audio transcription pipeline
- VAD integration with energy-based detection
- Custom node management for speech components
- Audio processing utilities and buffer management
- Speech-to-text workflow integration
- WebSocket URL priority fix for container hostname resolution
- 3-second buffer processing implementation
- RMS threshold-based VAD system
- Infinite loop prevention in audio processing

Dependencies:
- ComfyUI-UVR5/develop-speech
- ComfyUI-XTTS/develop-speech  
- ComfyUI-WhisperX/develop-speech
- ComfyUI-Manager/develop-speech

Critical Settings:
- rms_threshold=0.01, zcr_threshold=0.05, audio_rms_filter=0.03
- 3-second buffer processing intervals
- WebSocket priority: hostname first, localhost second

State: FULLY OPERATIONAL"

# Push to remote
git push origin develop-speech
```

## Verification Steps

### Post-Commit Verification
```bash
# Verify all branches exist
git branch -r | grep develop-speech

# Check remote connections
git remote -v

# Verify commit messages
git log --oneline -5

# Verify .cursor directories are committed
find . -name ".cursor" -type d
git ls-files | grep ".cursor"
```

### State Verification
```bash
# Test WebSocket connections
curl -I http://localhost:8189

# Check VAD settings
grep -r "rms_threshold" custom_nodes/ComfyUI-WhisperX/

# Verify processing logic
grep -r "3.0" custom_nodes/ComfyUI-WhisperX/

# Check audio filtering
grep -r "audio_rms_filter" custom_nodes/ComfyUI-WhisperX/
```

## Rollback Procedures

### If Issues Occur During Commit
```bash
# For each repository, if needed:
git checkout main
git branch -D develop-speech
git checkout -b develop-speech-backup-[DATE]
# Then retry the commit process
```

### If Remote Push Fails
```bash
# Check remote access
git remote -v
git fetch origin

# Verify permissions
git push origin develop-speech --dry-run

# If needed, create backup branch
git checkout -b develop-speech-backup-[DATE]
git push origin develop-speech-backup-[DATE]
```

## Success Criteria

### All Repositories Committed
- [ ] ComfyUI-UVR5/develop-speech
- [ ] ComfyUI-XTTS/develop-speech
- [ ] ComfyUI-WhisperX/develop-speech
- [ ] ComfyUI-Manager/develop-speech
- [ ] ComfyUI/develop-speech

### .cursor Directories Verified
- [ ] All .cursor directories committed
- [ ] No .gitignore exclusions for .cursor
- [ ] Documentation preserved in each repo
- [ ] Future LLM instructions available

### State Preserved
- [ ] VAD thresholds maintained
- [ ] WebSocket configuration preserved
- [ ] 3-second processing logic intact
- [ ] All custom nodes functional
- [ ] Speech pipeline operational

### Documentation Updated
- [ ] Commit messages descriptive and complete
- [ ] Dependencies clearly documented
- [ ] State information preserved
- [ ] Rollback procedures available

## Post-Commit Actions

### 1. Update Documentation
- Verify all .cursor/ documentation reflects current state
- Update any references to branch names
- Document any issues encountered during commit

### 2. Test Fresh Installation
```bash
# Clone fresh repositories
git clone https://github.com/QuasiPlanets/ComfyUI.git test-comfyui
git clone https://github.com/QuasiPlanets/ComfyUI-UVR5.git test-uvr5
git clone https://github.com/QuasiPlanets/ComfyUI-XTTS.git test-xtts
git clone https://github.com/QuasiPlanets/ComfyUI-WhisperX.git test-whisperx
git clone https://github.com/QuasiPlanets/ComfyUI-Manager.git test-manager

# Checkout develop-speech branches
cd test-comfyui && git checkout develop-speech
cd ../test-uvr5 && git checkout develop-speech
cd ../test-xtts && git checkout develop-speech
cd ../test-whisperx && git checkout develop-speech
cd ../test-manager && git checkout develop-speech
```

### 3. Verify System Operation
- Test WebSocket connections
- Verify VAD functionality
- Check transcription pipeline
- Confirm audio processing
- Validate all custom nodes

This execution plan ensures 100% reproducibility of the current operational speech system state.
