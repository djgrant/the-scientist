---
description: Generate a prompt from repo files for use with LLMs
---

The user wants to generate a prompt containing files from this repository.

**User's request:** $ARGUMENTS

## Your Task

### Step 1: Parse the request

Extract from user request:
- files: {semantic query or paths} (required)
- output format: {cxml|markdown|plain} (default: cxml)
- output type: {file|clipboard} (default: clipboard)
- file path: {path} (default: prompts/{short_desc}.{xml|md|txt})

### Step 2: Find relevant files

Use your tools (grep, glob, read) to explore the codebase and identify files matching the user's semantic query. Be thorough but focused.

### Step 3: Confirm with the user

Before generating the prompt, show the user what you found.

Wait for user confirmation before proceeding.

### Step 4: Generate the prompt

Once confirmed, use the `files-to-prompt` tool to generate the prompt (default is clipboard).

### Step 5: Report result

Tell the user:
- How many files were included
- The format used
- Where the output went (clipboard or file path)
