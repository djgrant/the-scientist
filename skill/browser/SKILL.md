---
name: browser
description: When testing web UI, load this skill to take screenshots and interact with elements.
---

## ::workflow::

DO
  1. open <url> to start session
  2. snapshot to see current state and get @refs
  3. interact with elements (click, type, etc.) using @refs or selectors
  4. screenshot to verify result
END


## Commands

```bash
agent-browser <command>
```

Common commands: `open <url>`, `snapshot`, `click <selector|@ref>`, `type <selector|@ref> <text>`, `screenshot`.
Use `agent-browser --help` for full command list.
