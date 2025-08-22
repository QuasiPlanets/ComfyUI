# .cursor Directory Commit Guide

## Overview
This guide ensures that all `.cursor/` directories are properly committed to their respective repositories. These directories contain critical documentation for future LLMs and must never be ignored.

**⚠️ CRITICAL: This guide should ONLY be executed with EXPLICIT USER PERMISSION.**
**⚠️ NEVER execute git operations without asking the user first.**

## Critical Requirements

### 1. .cursor Directories Must Be Committed
- **NEVER** exclude `.cursor/` from commits
- **NEVER** add `.cursor/` to .gitignore files
- **ALWAYS** include `.cursor/` directories in repository commits
- **ALWAYS** preserve documentation for future LLMs

### 2. Current .cursor Locations
```
ComfyUI/
├── .cursor/ (MAIN SYSTEM DOCUMENTATION)
│   ├── COMMIT_MANAGEMENT_GUIDE.md
│   ├── REPOSITORY_MAPPING.md
│   ├── SPEECH_SYSTEM_STATE.md
│   ├── COMMIT_EXECUTION_PLAN.md
│   └── CURSOR_DIRECTORY_COMMIT_GUIDE.md
├── custom_nodes/
│   ├── ComfyUI-UVR5/
│   │   └── .cursor (if exists)
│   ├── ComfyUI-XTTS/
│   │   └── .cursor/ (CONTAINS XTTS DOCUMENTATION)
│   │       ├── QUICK_REFERENCE.md
│   │       ├── README.md
│   │       ├── SYSTEM_TRACKER.md
│   │       ├── XTTS_DIAGNOSTIC_CODE_TRACKER.md
│   │       └── XTTS_DEVELOPMENT_GUIDE.md
│   ├── ComfyUI-WhisperX/
│   │   └── .cursor/ (CONTAINS WHISPERX DOCUMENTATION)
│   │       ├── QuasiWhisperX/
│   │       └── QuasiRealtimNode/
│   └── ComfyUI-Manager/
│       └── .cursor (if exists)
```

## Commit Process for .cursor Directories

### For Each Repository

#### 1. Verify .cursor Directory Exists
```bash
# Check if .cursor directory exists
ls -la .cursor/

# If it exists, ensure it's not ignored
grep -r ".cursor" .gitignore || echo ".cursor not in .gitignore - GOOD"
```

#### 2. Stage .cursor Directory
```bash
# Stage all changes including .cursor
git add .

# Explicitly ensure .cursor is included
git add .cursor/ 2>/dev/null || echo ".cursor directory not found in this repo"
```

#### 3. Verify .cursor is Staged
```bash
# Check what's staged
git status

# Verify .cursor files are included
git diff --cached --name-only | grep ".cursor"
```

#### 4. Commit with .cursor Documentation
```bash
git commit -m "feat: speech system integration - [REPO_NAME]

- VAD implementation with RMS thresholds
- WebSocket integration for real-time processing
- Audio buffer management (3-second intervals)
- Transcription pipeline integration
- Energy-based voice activity detection
- RMS threshold=0.01, zcr_threshold=0.05, audio_rms_filter=0.03
- .cursor/ directory included for future LLM documentation

State: FULLY OPERATIONAL"
```

## Verification Commands

### Pre-Commit Verification
```bash
# Check .cursor directories exist
find . -name ".cursor" -type d

# Verify .cursor is not ignored
grep -r ".cursor" .gitignore || echo "GOOD: .cursor not ignored"

# Check .cursor contents
ls -la .cursor/ 2>/dev/null || echo "No .cursor directory found"
```

### Post-Commit Verification
```bash
# Verify .cursor files are committed
git ls-files | grep ".cursor"

# Check .cursor directory in commit
git show --name-only HEAD | grep ".cursor"
```

## .gitignore Exclusions to Avoid

### NEVER Add These to .gitignore
```gitignore
# ❌ WRONG - Never exclude .cursor directories
.cursor/
.cursor/*
*.cursor

# ❌ WRONG - Never exclude documentation
*.md
docs/
documentation/
```

### Safe .gitignore Exclusions
```gitignore
# ✅ CORRECT - Safe exclusions
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
.env
*.log
.DS_Store
.vscode/
.idea/
```

## Repository-Specific .cursor Requirements

### Main ComfyUI Repository
- **Must Include**: All `.cursor/` documentation
- **Purpose**: System-wide documentation and guides
- **Critical Files**: Commit management, repository mapping, state documentation

### ComfyUI-XTTS Repository
- **Must Include**: `.cursor/` directory with XTTS documentation
- **Purpose**: XTTS-specific development and troubleshooting guides
- **Critical Files**: XTTS diagnostic tracker, development guide

### ComfyUI-WhisperX Repository
- **Must Include**: `.cursor/` directory with WhisperX documentation
- **Purpose**: WhisperX-specific implementation guides
- **Critical Files**: Real-time node documentation, WhisperX integration guides

### Other Custom Node Repositories
- **Must Include**: `.cursor/` directories if they exist
- **Purpose**: Node-specific documentation and guides
- **Critical Files**: Any documentation relevant to the specific node

## Future LLM Instructions

When working with this system:

1. **NEVER use git commands unless explicitly asked by the user**
2. **ALWAYS ask for user permission before making any commits**
3. **ALWAYS confirm the user wants to proceed with git operations**
4. **Always check for .cursor directories** before making changes
5. **Never exclude .cursor from commits** - these contain critical documentation
6. **Update .cursor documentation** when making significant changes
7. **Preserve state information** in .cursor directories
8. **Follow commit guides** stored in .cursor directories
9. **Maintain documentation** for future development cycles

### Critical Safety Rules:
- **NEVER execute git commands without explicit user request**
- **ALWAYS ask "Do you want me to commit these changes?" before proceeding**
- **NEVER assume the user wants commits made automatically**
- **ALWAYS explain what git operations will be performed before executing them**

## Emergency Procedures

### If .cursor Directory is Accidentally Ignored
```bash
# Remove .cursor from .gitignore
sed -i '/\.cursor/d' .gitignore

# Add .cursor back to git
git add .cursor/
git commit -m "fix: restore .cursor directory documentation"
```

### If .cursor Directory is Missing
```bash
# Check if it was accidentally deleted
git log --name-status | grep ".cursor"

# Restore from previous commit if needed
git checkout HEAD~1 -- .cursor/
git add .cursor/
git commit -m "fix: restore missing .cursor directory"
```

This guide ensures that all critical documentation is preserved for future LLMs and development cycles.
