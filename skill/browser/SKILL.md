---
name: browser
description: When testing or verifying web UI use this skill to start the browser server, take screenshots to observe state, interact with elements, and verify visually.
---

# Browser Interaction

## Setup

```bash
# Start dev server (if not running)
npm run dev &

# Start browser server
python .opencode/skill/browser/screenshot.py start &

# Check status
python .opencode/skill/browser/screenshot.py status
```

## Commands

```bash
python .opencode/skill/browser/screenshot.py <command> [args]
```

| Command | Description |
|---------|-------------|
| `start` | Start browser server |
| `stop` | Stop browser server |
| `status` | Check if running |
| `screenshot` | Take screenshot |
| `click <selector>` | Click element |
| `type <selector> <text>` | Type into input |
| `press <key>` | Press key (Enter, ArrowDown, etc.) |
| `list <selector>` | List matching elements |
| `text <selector>` | Get element text |

## Workflow

1. Screenshot to see current state
2. List elements to discover selectors
3. Interact with elements
4. Screenshot to verify result

## Screenshots

Saved to `.screenshots/screenshot.png` in the current working directory. Read this file to see the visual state.
