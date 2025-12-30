# opencode-scientist

An extensible [OpenCode](https://opencode.ai)↗ configuration with custom agents, work packages, commands, and skills.

Designed to help agents self-steer using feedback loops and a hypothesis-driven iteration cycle. 

Excels at operating long-horizon, multi-task projects. 

## Use Cases

I am still experimenting with this setup, but I have found it very valuable for two particular use-cases:
1. Personal applications e.g. holiday planner, home automation etc.
2. Feasibilty explorations e.g. building out large features to generate insights

Whether you decide to ship the code this system produces, or use it as the inspiration for a more-considered build, will depend on entirely on your context and risk tolerance.

The system may also be valuable to developers who gain less enjoyment from spending all day steering agents. The long-running projects create a meaningful interval to divert attention onto more focussed tasks.

## How to Use

The most important agent in this setup is you.

A clear, well-thought-out vision is to an LLM what a good data structure is to code.

I recommend trying the following workflow:

1. Start opencode in *plan* mode and explain your vision to the agent
2. Feel free to leave some questions open-ended at this stage (exploration can be delegated to subagents)
3. Once the vision is well-formed ask the *plan* agent to create a "scoping work package" to capture the vision and areas to explore 
4. Compact the conversation
5. Switch to *delegate* mode (tab key), and ask the agent to read the work package and execute the vision

The *delegate* agent will then use subagents to create more detailed work packages, which, in turn, get delegated to other subagents to implement.

## Operating Cost

It is recommended to run long-running projects with subscription pricing e.g. Claude Code, Github Copilot etc. (via `opencode auth login`). 

In my experience API pricing can end up being a factor of 100x more expensive.

## Recommended Models

I am personally using this with Opus 4.5. No doubt, Gemini 3, GPT 5.2 and similar class models will work similarly well.  

I strongly suspect that the system will break down with a model like Sonnet 4.5, and will be no more cost effective.

Note: You can [set a default model](https://opencode.ai/docs/models/#set-a-default)↗ in your global or project opencode configuration.

## What's Included

### Agents

| Agent | Description |
|-------|-------------|
| `architect` | Plans architecture and major changes |
| `critique` | Adversarial critic for generating insights through disagreement |
| `delegate` | Orchestrates long-horizon projects via work packages and subagents |
| `document` | Technical writer for documentation |
| `ux` | Tests web interfaces and researches UX solutions |

Note: opencode already ships with [built-in agents](https://opencode.ai/docs/agents/#built-in)↗ – plan, general, build, and explore.

### Commands

| Command | Description |
|---------|-------------|
| `/browser-test` | Test web UI in browser with screenshots |
| `/commit` | Create a git commit with AI-generated message |
| `/review-docs` | Check documentation accuracy against code |
| `/test-and-fix` | Run tests and fix any failures |

### Skills

| Skill | Description |
|-------|-------------|
| `browser` | Take screenshots and interact with web UIs via Playwright |
| `read-learnings` | Review previously recorded project learnings |
| `record-learnings` | Record notable discoveries for future reference |
| `scientific-method` | Hypothesis-driven iteration |
| `work-packages` | Structured approach for multi-agent task handoff |
| `write-tests` | Guidelines for writing tests |

### Work Packages

This config includes a work package system for structured multi-agent collaboration:

```
work/
  todo/        # Pending work packages
  in-progress/ # Currently being worked on
  completed/   # Finished work packages
```

Work packages are markdown files that define a problem, scope, approach, and track results across multiple agent sessions.

### Learnings

Agents can record project-specific discoveries in `learnings/`:

```
learnings/
  2025-01-15-(package:api)-(auth flow)-(tags:security,oauth).md
```

These are loaded by the `read-learnings` skill to provide context to agents.


## Setup

### Option 1: Symlink (Full Replacement)

Replace your global OpenCode config with this repo:

```bash
# Clone the repo
git clone https://github.com/djgrant/dotopencode.git

# Symlink
ln -s {repo_path} ~/.config/opencode
```

### Option 2: OPENCODE_CONFIG_DIR (Merge with Personal Config)

Keep your personal config at `~/.config/opencode` and load this repo as an overlay:

```bash
# Clone the repo
git clone https://github.com/djgrant/dotopencode.git

# Add to your shell profile (.zshrc, .bashrc, etc.)
export OPENCODE_CONFIG_DIR={repo_path}
```

The overlay config is loaded **after** your personal config, so it can override settings while preserving your personal preferences.

## Customization

### Per-Project Overrides

You can override any of these settings in a project's `.opencode/` directory. OpenCode merges configs in this order:

1. Global config (`~/.config/opencode/`)
2. `OPENCODE_CONFIG_DIR` (if set)
3. Project config (`.opencode/`)

## Global Dependencies

### Playwright

The browser skill requires Playwright:

```bash
pip install playwright
playwright install chromium
```
