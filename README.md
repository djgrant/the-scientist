[Features](#features)<sup>↓</sup> • [Installation](#installation)<sup>↓</sup> • [User Guide](#user-guide)<sup>↓</sup>

<h1>
THE
<br \>
SCIENTIST
</h1>

An [OpenCode](https://opencode.ai)<sup>↗</sup> settings pack with custom agents, work packages, commands, and skills.

Designed to help agents self-steer using feedback loops and a hypothesis-driven iteration cycle. 

Excels at operating long-horizon, multi-task projects. 

## Quick Start

```
$ opencode

█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒
█░                                                                      ░▒  
█░  Help me set up https://github.com/djgrant/the-scientist             ░▒
█░                                                                      ░▒  
█░  Build   Claude Opus 4.5 (latest) Anthropic                          ░▒
█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒
```

<br />

# Features

### Agents

Specialized agents for different task types.

| Agent | Description |
|-------|-------------|
| [`architect`](agent/architect.md) | Plans architecture and major changes |
| [`critique`](agent/critique.md) | Adversarial critic for generating insights through disagreement |
| [`delegate`](agent/delegate.md) | Orchestrates long-horizon projects via work packages and subagents |
| [`diverge`](agent/diverge.md) | Thinks outside the box to find new directions or alternative solutions |
| [`document`](agent/document.md) | Technical writer for documentation |
| [`qa`](agent/qa.md) | End-to-end testing using a browser |
| [`ux`](agent/ux.md) | Researches UX solutions |

Note: OpenCode already ships with [built-in agents](https://opencode.ai/docs/agents/#built-in)<sup>↗</sup> – plan, general, build, and explore.

### Commands

Slash commands for common workflows.

| Command | Description |
|---------|-------------|
| [`/browser-test`](command/browser-test.md) | Test web UI in browser with screenshots |
| [`/commit`](command/commit.md) | Create a git commit with AI-generated message |
| [`/files-to-prompt`](command/files-to-prompt.md) | Generate a prompt from repo files for use with LLMs |
| [`/init-scientist`](command/init-scientist.md) | Initialise project with the-scientist structure and dependencies |
| [`/update-scientist`](command/update-scientist.md) | Update the-scientist to the latest version |
| [`/review-docs`](command/review-docs.md) | Check documentation accuracy against code |
| [`/test-and-fix`](command/test-and-fix.md) | Run tests and fix any failures |

### Skills

Lazily loaded instructions that guide agent behavior.

| Skill | Description |
|-------|-------------|
| [`browser`](skill/browser/SKILL.md) | Take screenshots and interact with web UIs via Playwright |
| [`divergent-thinking`](skill/divergent-thinking/SKILL.md) | Expand thinking to the edges of the distribution |
| [`read-learnings`](skill/read-learnings/SKILL.md) | Review previously recorded project learnings |
| [`record-learnings`](skill/record-learnings/SKILL.md) | Record notable discoveries for future reference |
| [`scientific-method`](skill/scientific-method/SKILL.md) | Hypothesis-driven iteration |
| [`work-packages`](skill/work-packages/SKILL.md) | Structured approach for multi-agent task handoff |
| [`write-tests`](skill/write-tests/SKILL.md) | Guidelines for writing tests |

### Storage

Persistent state stored in a project's `.opencode/` directory.

| Concept | Purpose |
|---------|---------|
| Work packages | Documents defining a goal, hypothesis and results; tracked across sessions |
| Learnings | Notable discoveries that provide context to future agent sessions |

### Tools

Custom tools available to agents.

| Tool | Description |
|------|-------------|
| [`files-to-prompt`](tool/files-to-prompt.ts) | Generate prompts from repo files using [files-to-prompt](https://github.com/simonw/files-to-prompt) |

<br />

# Installation

First, install the settings pack globally, then initialise the-scientist per project.

### Global Setup

There are two ways to install:

**1/ As an overlay config**

```bash
git clone https://github.com/djgrant/the-scientist.git

# Add to your shell profile (.zshrc, .bashrc, etc.)
export OPENCODE_CONFIG_DIR={path_to_cloned_repo}
```

Loads _after_ your global and project settings. See [custom directory docs](https://opencode.ai/docs/config/#custom-directory)<sup>↗</sup>.

**2/ As your global config**

```bash
git clone https://github.com/djgrant/the-scientist.git ~/.config/opencode
```

Loads _before_ your project settings. You can alternatively symlink to this location.

### Project Setup

Run `/init-scientist` within your repo. This will set up:

- `.opencode/work/` for work packages
- `.opencode/learnings/` for project learnings
- Playwright and files-to-prompt CLI tools
- Optionally, an AGENTS.md template

## Updating

To update the-scientist to the latest version, you have two options:

**1/ Run update command**

```
/update-scientist
```

The command will instruct the agent to merge any local changes and check for new prerequisites.

**2/ Pull Manually**

```bash
cd {path-to-the-scientist}
git pull
```

<br />

# User Guide

The most important agent in this setup is _you_.

A clear, well-thought-out vision is to an LLM what a good data structure is to code.

## Approach

Here are a couple of suggestions you can try as a starting point.


### Existing Projects 

Prompt the delegate agent to:

```
Commission thorough research looking for gaps and opportunities in this project. Explore a wide range of areas and ideas. 
```

### New Projects/Features

Try this workflow:

1. Start opencode in *plan* mode and explain your vision to the agent
2. Leave some questions open (exploration can be delegated to subagents)
3. Once the vision is well-formed ask the *plan* agent to create a *"scoping work package"* to capture the vision and areas to explore 
4. Compact the conversation (/compact)
5. Switch to *delegate* mode (tab key), then ask the agent to "read the work package and execute the vision"*

The *delegate* agent will then use subagents to create more detailed work packages, which, in turn, get delegated to other subagents to implement.

## Use Cases

I have so far found this setup valuable for:
1. Deep-dives e.g find performance/security/ux gaps and opportunities
2. Feasibilty experiments e.g. build out a features to generate insights
3. Personal applications e.g. holiday planner, home automation etc.

This system may also be valuable to developers who gain less enjoyment from manually hand-holding agents. Once a long-running project gets started, you get a reasonably long interval to divert your attention toward more focussed tasks.

Whether you decide to ship the code this system produces, or use it as the inspiration for a more-considered build, will depend on entirely on your context and risk tolerance.

## Operating Costs

When you use the delegate agent, orchestrated tasks can run for anything up to an hour (even with agents working in parallel). 

It is therefore recommended to be on subscription pricing e.g. Claude Code, Github Copilot etc. (set up via `opencode auth login`). In my experience, API pricing can end up being a factor of 100x more expensive.

## Recommended Models

I am personally using this with Opus 4.5. No doubt, Gemini 3, GPT 5.2 and other SOTA-class models will work similarly well. Mixing models, will probably boost peformance. 

I strongly suspect that the system will break down with a model like Sonnet 4.5, and will be no more cost effective.

Note: You can [set a default model](https://opencode.ai/docs/models/#set-a-default)<sup>↗</sup> in your global or project opencode configuration.

<br />

# License

MIT License - Copyright (c) 2025 Daniel Grant
