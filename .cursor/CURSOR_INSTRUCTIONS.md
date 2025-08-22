# Cursor AI Instructions for .cursor Directory

## Overview
This document provides instructions for Cursor AI on how to effectively use the `.cursor` directory structure to understand and work with the ComfyUI WhisperX transcription system.

## Directory Structure

```
.cursor/
├── README.md                           # Project overview and quick start
├── DEPLOYMENT_GUIDE.md                 # Complete setup instructions
├── DEVELOPMENT_HISTORY.md              # Detailed development timeline
├── TROUBLESHOOTING.md                  # Common issues and solutions
├── CUSTOM_NODES_GUIDE.md              # Custom node documentation
├── WEBSOCKET_INTEGRATION.md            # Real-time communication guide
├── ELIZAOS_INTEGRATION.md              # External system integration
├── CURSOR_INSTRUCTIONS.md              # This file
└── custom_nodes/
    └── ComfyUI-WhisperX/
        ├── README.md                   # WhisperX specific documentation
        ├── DEVELOPMENT_LOG.md          # Detailed development history
        ├── INTEGRATION_GUIDE.md        # Integration instructions
        ├── TROUBLESHOOTING.md          # WhisperX specific issues
        └── API_REFERENCE.md            # API documentation
```

## How to Use This Directory

### 1. Start with README.md
Always begin by reading `.cursor/README.md` to understand:
- Project overview and purpose
- Key components and architecture
- Current status and capabilities
- Quick start instructions

### 2. Check Development History
For any development task, consult `.cursor/DEVELOPMENT_HISTORY.md` to understand:
- Previous decisions and their rationale
- Technical challenges and solutions
- Performance optimizations implemented
- Lessons learned from past development

### 3. Use Troubleshooting Guide
When encountering issues, refer to `.cursor/TROUBLESHOOTING.md` for:
- Common problems and solutions
- Debug commands and procedures
- Performance optimization techniques
- Emergency procedures

### 4. Consult Integration Guides
For integration tasks, use:
- `.cursor/WEBSOCKET_INTEGRATION.md` for real-time communication
- `.cursor/ELIZAOS_INTEGRATION.md` for external system integration
- `.cursor/CUSTOM_NODES_GUIDE.md` for ComfyUI node development

### 5. WhisperX-Specific Documentation
For WhisperX custom node work, use `.cursor/custom_nodes/ComfyUI-WhisperX/`:
- `README.md` for node overview and features
- `DEVELOPMENT_LOG.md` for detailed development history
- `INTEGRATION_GUIDE.md` for integration patterns
- `API_REFERENCE.md` for complete API documentation
- `TROUBLESHOOTING.md` for node-specific issues

## Key Development Principles

### 1. Preserve Context
- All technical decisions are documented with rationale
- Performance metrics and optimization details are preserved
- Error handling and recovery mechanisms are documented

### 2. Follow Established Patterns
- Use proven integration patterns from the guides
- Follow the documented error handling strategies
- Apply the performance optimization techniques

### 3. Maintain Compatibility
- Ensure changes don't break existing functionality
- Test with the documented verification procedures
- Follow the established deployment processes

## Common Tasks and Where to Look

### Adding New Features
1. Check `DEVELOPMENT_HISTORY.md` for similar features
2. Review `INTEGRATION_GUIDE.md` for integration patterns
3. Consult `API_REFERENCE.md` for existing APIs
4. Update relevant documentation files

### Debugging Issues
1. Start with `TROUBLESHOOTING.md` for common solutions
2. Check `DEVELOPMENT_HISTORY.md` for similar past issues
3. Review `DEVELOPMENT_LOG.md` for specific node issues
4. Use debug commands from the troubleshooting guides

### Performance Optimization
1. Review performance metrics in `DEVELOPMENT_HISTORY.md`
2. Apply optimization techniques from `TROUBLESHOOTING.md`
3. Check `WEBSOCKET_INTEGRATION.md` for communication optimization
4. Monitor using documented performance tools

### Integration Work
1. Study `WEBSOCKET_INTEGRATION.md` for communication patterns
2. Review `ELIZAOS_INTEGRATION.md` for external system integration
3. Check `CUSTOM_NODES_GUIDE.md` for ComfyUI integration
4. Follow documented testing procedures

## Documentation Standards

### When Adding New Documentation
1. **Update relevant existing files** rather than creating new ones
2. **Include context and rationale** for all decisions
3. **Provide code examples** for implementation
4. **Document performance implications** of changes
5. **Include troubleshooting information** for common issues

### Code Documentation
1. **Follow the established patterns** in existing code
2. **Include comprehensive docstrings** for all functions
3. **Document error handling** and recovery mechanisms
4. **Provide usage examples** for complex functionality

### Testing Documentation
1. **Document test procedures** for new features
2. **Include verification commands** for functionality
3. **Provide performance benchmarks** where applicable
4. **Document integration testing** procedures

## Emergency Procedures

### System Issues
1. Check `TROUBLESHOOTING.md` for emergency procedures
2. Review `DEVELOPMENT_HISTORY.md` for similar past issues
3. Use documented rollback procedures
4. Follow recovery steps from the guides

### Performance Issues
1. Apply optimization techniques from `TROUBLESHOOTING.md`
2. Check performance metrics in `DEVELOPMENT_HISTORY.md`
3. Use monitoring tools from the guides
4. Apply documented memory management techniques

### Integration Issues
1. Review `WEBSOCKET_INTEGRATION.md` for communication issues
2. Check `ELIZAOS_INTEGRATION.md` for external system issues
3. Use documented debugging procedures
4. Follow reconnection and recovery patterns

## Best Practices

### 1. Always Check Documentation First
- Search existing documentation before implementing solutions
- Use documented patterns and approaches
- Follow established best practices

### 2. Preserve Knowledge
- Document all significant decisions and their rationale
- Include performance implications of changes
- Document troubleshooting procedures for new issues

### 3. Test Thoroughly
- Use documented testing procedures
- Verify performance with established benchmarks
- Test integration points thoroughly

### 4. Update Documentation
- Keep documentation current with code changes
- Add new troubleshooting information
- Update performance metrics and benchmarks

## Quick Reference

### Essential Files for Development
- `README.md` - Project overview and quick start
- `DEVELOPMENT_HISTORY.md` - Technical decisions and context
- `TROUBLESHOOTING.md` - Common issues and solutions
- `API_REFERENCE.md` - Complete API documentation

### Essential Files for Integration
- `WEBSOCKET_INTEGRATION.md` - Real-time communication
- `ELIZAOS_INTEGRATION.md` - External system integration
- `CUSTOM_NODES_GUIDE.md` - ComfyUI node development

### Essential Files for Debugging
- `TROUBLESHOOTING.md` - Common issues and solutions
- `DEVELOPMENT_LOG.md` - Detailed development history
- `API_REFERENCE.md` - API documentation and examples

This directory structure provides comprehensive context and knowledge for effective development and maintenance of the ComfyUI WhisperX transcription system.


