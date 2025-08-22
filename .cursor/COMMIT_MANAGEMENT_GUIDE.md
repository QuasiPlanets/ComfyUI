# Commit Management Guide - Speech System

## Overview
This guide ensures 100% repeatability of the current operational speech system state across all repositories. All changes are committed to `develop-speech` branches to preserve the exact working state without disturbing main branches.

## Repository Structure
```
QuasiPlanets/ComfyUI (main repo)
├── QuasiPlanets/ComfyUI-UVR5 (custom node)
├── QuasiPlanets/ComfyUI-XTTS (custom node)
├── QuasiPlanets/ComfyUI-WhisperX (custom node)
└── QuasiPlanets/ComfyUI-Manager (custom node)
```

## Current Operational State
- **WebSocket connections**: Working with correct hostname resolution
- **VAD (Voice Activity Detection)**: Energy-based RMS thresholds implemented
- **Transcription**: WhisperX operational with 3-second buffer processing
- **Audio processing**: RMS threshold=0.01, zcr_threshold=0.05, audio_rms_filter=0.03
- **Processing logic**: Every 3 seconds or when buffer gets large (FULLY WORKING)

## Commit Strategy

### 1. Branch Creation
All commits go to `develop-speech` branches:
- `ComfyUI/develop-speech`
- `ComfyUI-UVR5/develop-speech`
- `ComfyUI-XTTS/develop-speech`
- `ComfyUI-WhisperX/develop-speech`
- `ComfyUI-Manager/develop-speech`

### 2. Commit Order (Critical)
1. **Custom Nodes First** (dependencies)
2. **Main ComfyUI Last** (depends on custom nodes)

### 3. Commit Process

#### Step 1: Custom Node Repositories
For each custom node in `custom_nodes/`:
```bash
cd custom_nodes/[NODE_NAME]
git checkout -b develop-speech
git add .
git commit -m "feat: speech system integration - [NODE_NAME]

- VAD implementation with RMS thresholds
- WebSocket integration for real-time processing
- Audio buffer management (3-second intervals)
- Transcription pipeline integration
- Energy-based voice activity detection
- RMS threshold=0.01, zcr_threshold=0.05, audio_rms_filter=0.03

State: FULLY OPERATIONAL"
git push origin develop-speech
```

#### Step 2: Main ComfyUI Repository
```bash
# From ComfyUI root
git checkout -b develop-speech
git add .
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
git push origin develop-speech
```

## File Change Tracking

### Custom Node Changes
Each custom node should track:
- Node implementation files
- Dependencies and requirements
- Configuration files
- Integration points with main ComfyUI
- `.cursor/` directories (CRITICAL: Must be committed)

### Main ComfyUI Changes
- WebSocket server modifications
- Audio processing utilities
- Custom node loading enhancements
- Speech pipeline integration
- `.cursor/` directory (CRITICAL: Contains all documentation)

## .cursor Directory Management

### Critical Importance
- `.cursor/` directories contain essential documentation for future LLMs
- Must be committed to each repository
- Not ignored by any .gitignore files
- Contains state documentation, commit guides, and system information

### Current .cursor Locations
- `ComfyUI/.cursor/` - Main system documentation
- `ComfyUI-XTTS/.cursor/` - XTTS-specific documentation
- `ComfyUI-WhisperX/.cursor/` - WhisperX-specific documentation
- Other custom nodes may have .cursor directories

### Commit Requirements
- All `.cursor/` directories must be included in commits
- No .gitignore exclusions for .cursor directories
- Documentation must be kept up-to-date
- State information must be preserved

## State Verification

### Pre-Commit Checklist
- [ ] All WebSocket connections working
- [ ] VAD thresholds properly configured
- [ ] Transcription operational
- [ ] 3-second buffer processing working
- [ ] No infinite loops in processing logic
- [ ] Audio RMS filtering functional

### Post-Commit Verification
- [ ] All branches created successfully
- [ ] All commits pushed to remote
- [ ] Branch protection rules in place
- [ ] Documentation updated
- [ ] State reproducible from branches

## Rollback Strategy
If issues arise:
1. Keep `develop-speech` branches as backup
2. Create `develop-speech-backup-[DATE]` branches
3. Document any issues in commit messages
4. Maintain working state in separate branches

## Future Development
- All speech-related development continues on `develop-speech` branches
- Main branches remain untouched
- Regular state snapshots via commits
- Comprehensive testing before any main branch integration

## Cursor LLM Instructions
When working with this system:
1. **NEVER use git commands unless explicitly asked by the user**
2. **ALWAYS ask for user permission before making any commits**
3. **ALWAYS confirm the user wants to proceed with git operations**
4. Always check current branch before making changes
5. Follow the commit order (custom nodes first, main repo last)
6. Use descriptive commit messages with state information
7. Verify operational state before committing
8. Document any deviations from this guide
9. Maintain the exact working state at all times

### Critical Safety Rules:
- **NEVER execute git commands without explicit user request**
- **ALWAYS ask "Do you want me to commit these changes?" before proceeding**
- **NEVER assume the user wants commits made automatically**
- **ALWAYS explain what git operations will be performed before executing them**

## Emergency Procedures
If the system breaks:
1. Check out `develop-speech` branches
2. Verify all custom nodes are properly loaded
3. Check WebSocket connections and VAD settings
4. Restore from last known working commit
5. Document the issue and resolution

## Repository Verification Process

### Post-Commit Verification
After all commits are complete, verify each repository:

```bash
# For each repository, check:
git branch          # Should show develop-speech as current
git remote -v       # Should point to correct remote
git status          # Should be clean
```

### Verification Checklist
- [ ] All repositories on `develop-speech` branches
- [ ] All remotes correctly configured
- [ ] All changes committed and pushed
- [ ] No uncommitted changes remaining
- [ ] Documentation updated

## Integration Testing
After commits:
1. Clone fresh repositories
2. Checkout `develop-speech` branches
3. Install dependencies
4. Test speech functionality
5. Verify all components work together
6. Document any integration issues

## Repository Status Documentation
See `.cursor/GIT_REPOSITORY_VERIFICATION.md` for detailed verification status and repository configurations.

This guide ensures the speech system remains 100% reproducible and operational across all development cycles.
