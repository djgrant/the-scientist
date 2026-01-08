---
name: orchestrate-map-reduce
description: When you need multiple operations to get one solution, use this orchestration strategy to fan out to multiple agents, validate their solutions and find a winning solution.
---

## Types

$Task: any task that an agent can execute (can be a set of instruction, tool call or something else)
$Strategy: accumulate or independent execution (default: accumulate)

## Input

- $transforms: ($Task, $Strategy)
- $validator: $Task
- $return: $Task

### Choosing a Strategy
- **Accumulate**: When the aim is to progressively work toward the best solution
- **Independent**: When the aim is review a diverse set of candidates (can be run in parallel; each prompt should be a variant of $transforms($n))

## Map-Reduce Workflow

1. Create master work package
2. Delegate to sub-agent: summarise the status quo solution and write it to $current
3. FOR EACH $task IN $transforms:
  - Delegate to sub-agent: RENDER(#iteration-manager-prompt WITH ($strategy, $task, $validator IF strategy == accumulate))
4. Collect findings from each iteration manager
5. Update master work package
6. Run the return task

### Iteration Manager Prompt

```md
You are responsible for mapping over Task until it passes Validator.

## Reference

Strategy: {$strategy FROM $transforms}
Task: {$task FROM $transforms}
Validator: {$validator}

## Context 

- $SolutionPath = $n => `/relevant wp path/-candidate-{$n}.md`
- $current: $FilePath = $SolutionPath(0)
- $next: $FilePath = $SolutionPath(1)

## Tracking Candidates

Each proposed solution should be stored in a markdown document titled {$next}.

## Workflow 
1. Create a work package
2. WHILE (not diminishing returns AND $iterations < 5)
  - Delegate to sub-agent with #build-prompt
{{IF (strategy == accumulate) THEN}}
  - delegate to sub-agent #validate-prompt
  - IF (pass) THEN update work package; ELSE continue
  - IF (pass) $current = $next; $next = $SolutionPath($iteration + 1)
3. Return findings
{{ELSE}}
3.  delegate to sub-agent #validate-all-prompt
4. Return findings
{{END}}

## Build Prompt

{$task}

Current solution: {$current}

Write your answer to: {$next} 
```

## Validate Prompt

```md
Validation method: {$validator}

Use validator on proposed solution.

Update {$next} with your findings.
```

## Validate All Prompt

```md
Review all proposed solutions in {$SolutionPath(1)} through {$SolutionPath($iterations)}.

Select the best candidate and update the work package with your findings.
```
