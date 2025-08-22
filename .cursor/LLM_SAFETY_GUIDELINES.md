# LLM Safety Guidelines - Git Operations

## Critical Safety Rules

### ⚠️ NEVER Execute Git Commands Without Explicit Permission

**RULE #1: NEVER use git commands unless explicitly asked by the user**
- Do not suggest git operations unless the user specifically requests them
- Do not execute git commands automatically
- Do not assume the user wants commits made

**RULE #2: ALWAYS ask for permission before git operations**
- Ask: "Do you want me to commit these changes?"
- Ask: "Should I push these changes to the remote repository?"
- Ask: "Do you want me to create a new branch?"

**RULE #3: ALWAYS explain what will happen**
- Explain what git operations will be performed
- Explain which files will be committed
- Explain which branches will be affected
- Explain what the impact will be

**RULE #4: ALWAYS confirm before proceeding**
- Wait for explicit user confirmation
- Do not proceed if the user is unsure
- Stop immediately if the user says no

## Examples of Proper LLM Behavior

### ✅ CORRECT - Ask First
```
"I can see there are uncommitted changes. Would you like me to commit them to the develop-speech branch? I would need to:
1. Stage the modified files
2. Create a commit with a descriptive message
3. Push to the remote repository

Should I proceed with these git operations?"
```

### ❌ INCORRECT - Don't Do This
```
"I'll commit these changes for you now..."
[executes git commands without asking]
```

## When Git Operations Are Appropriate

### ✅ Safe Scenarios (Still Ask First)
- User explicitly says "commit these changes"
- User explicitly says "push to remote"
- User explicitly says "create a new branch"
- User explicitly says "follow the commit plan"

### ❌ Never Safe Scenarios
- User mentions there are changes but doesn't ask for commits
- User asks about git status but doesn't request actions
- User is exploring or learning about the system
- User is asking questions about the repository structure

## Emergency Procedures

### If You Accidentally Execute Git Commands
1. **STOP immediately**
2. **Tell the user what happened**
3. **Explain the impact**
4. **Ask if they want to undo the changes**
5. **Document the incident**

### If User Asks About Git Status
- Provide information about current state
- Explain what changes exist
- **DO NOT suggest or execute git operations**
- Let the user decide what they want to do

## Documentation Requirements

### Always Document Git Operations
When git operations are performed (with permission):
1. Document what was done
2. Document why it was done
3. Document the user's explicit permission
4. Update relevant .cursor documentation

## Repository-Specific Guidelines

### Main ComfyUI Repository
- **Remote**: origin (ComfyUI) and quasiplanets (ComfyUI)
- **Branch**: develop-speech
- **Ask before**: Any commits, pushes, or branch operations

### Custom Node Repositories
- **UVR5**: origin → ComfyUI-UVR5
- **XTTS**: origin → ComfyUI-XTTS  
- **WhisperX**: origin → ComfyUI-WhisperX
- **Manager**: origin → ComfyUI-Manager
- **Ask before**: Any operations on these repositories

## Communication Templates

### When User Mentions Changes
```
"I can see there are [X] modified files. Would you like me to:
1. Show you what changes exist?
2. Help you understand the current git status?
3. Commit these changes (if you want me to)?

What would you prefer?"
```

### When User Asks About Committing
```
"Before I commit these changes, let me confirm:
- I'll commit to the develop-speech branch
- I'll include [list of files]
- I'll push to the remote repository

Is this what you want me to do?"
```

### When User Asks About Git Status
```
"Current git status:
- Branch: [branch name]
- Modified files: [list]
- Untracked files: [list]
- Remote: [remote info]

What would you like to know more about?"
```

## Summary

**Remember: The user is in control. You are here to help, not to make decisions about their repository.**

- ✅ **Ask first, always**
- ✅ **Explain what you'll do**
- ✅ **Wait for permission**
- ✅ **Document everything**
- ❌ **Never assume**
- ❌ **Never execute without asking**
- ❌ **Never rush or pressure**

This ensures the user's repository remains safe and under their control at all times.
