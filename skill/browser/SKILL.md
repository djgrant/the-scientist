---
name: browser
description: When testing web UI, load this skill to take screenshots and interact with elements.
---

## ::workflow::

DO
  1. screenshot to see current state
  2. list elements to find selectors
  3. interact with elements
  4. screenshot to verify result
END


## Setup

```bash
npm run dev
python .opencode/skill/browser/screenshot.py start &
```

## Commands

```bash
python .opencode/skill/browser/screenshot.py <command>
```

Commands: `screenshot` to capture current state, `click <selector>` to click an element, `type <selector> <text>` to type into input, `list <selector>` to list matching elements.


## Teardown

```bash
python .opencode/skill/browser/screenshot.py stop
```
