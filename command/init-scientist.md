# /init-scientist

Initialize project with opencode-scientist structure and dependencies.

## Instructions

You are setting up a project to use the opencode-scientist configuration. Follow these steps:

### 1. Check Current State

Check the following and note what exists vs what's missing:

- `.opencode/work/` directory structure (todo/, in-progress/, completed/)
- `.opencode/learnings/` directory
- `AGENTS.md` or `.opencode/agents.md` file
- Python/pip availability: `which python3 && which pip3`
- Playwright package: `pip3 show playwright`
- files-to-prompt package: `pip3 show files-to-prompt`

### 2. Propose a Plan

Present your findings to the user in a clear summary:

```
## Current State

Directories:
- .opencode/work/: [exists | missing]
- .opencode/learnings/: [exists | missing]

AGENTS.md: [exists at ./AGENTS.md | exists at .opencode/agents.md | missing]

Dependencies:
- Python/pip: [available | not found]
- playwright: [installed | not installed]
- files-to-prompt: [installed | not installed]

## Proposed Actions

1. [List what will be created]
2. [List what will be installed]
```

Then ask the user:
- "Would you like me to create an AGENTS.md file? (default location: ./AGENTS.md)"
- "Proceed with setup? (y/n)"

Wait for user confirmation before proceeding.

### 3. Execute the Plan

After user confirms:

**Create directory structure:**
```bash
mkdir -p .opencode/work/todo .opencode/work/in-progress .opencode/work/completed
mkdir -p .opencode/learnings
touch .opencode/work/todo/.gitkeep
touch .opencode/work/in-progress/.gitkeep
touch .opencode/work/completed/.gitkeep
touch .opencode/learnings/.gitkeep
```

**Install missing dependencies (if pip available):**
```bash
pip3 install playwright
playwright install chromium
pip3 install files-to-prompt
```

If pip is not available, inform the user:
> Python/pip not found. Please install Python 3 and pip, then run:
> - `pip3 install playwright && playwright install chromium`
> - `pip3 install files-to-prompt`

**Create AGENTS.md (if requested):**

Create the file at the user's preferred location with this template:

```markdown
# Project Instructions

## Overview

[Brief description of the project]

## Architecture

[Key architectural decisions and patterns]

## Development Guidelines

[Coding standards, conventions, and practices]

## Important Files

[Key files and their purposes]
```

### 4. Report Results

Summarize what was done:

```
## Setup Complete

Created:
- .opencode/work/todo/
- .opencode/work/in-progress/
- .opencode/work/completed/
- .opencode/learnings/
- [AGENTS.md if created]

Installed:
- [List installed packages]

Skipped:
- [List anything that already existed or was skipped]
```
