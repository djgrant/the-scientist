---
name: work-packages
description: When asked to create a work package (aka WP), or are given a work package to complete, use this skill to understand the correct methodology.
---

## Work Package Structure

```markdown
# {Title}

## Problem
{What is the problem that needs to be solved}

## Scope  
{Which files/packages this touches}

## Approach
{How to do it}

## Hypothesis
{How and why do you think this will work}

## Results
{To be filled out upon completion. Can contain multiple iterations.}

## Evaluation
{What did your learn from the results? Was the hypothesis proved correct?}
```

## Lifecycle

Work packages enable large tasks to be handled my multiple agents. The state of the task is persisted between agent session. As such, each stage of the work package does not necessarily need to be handled by a single agent.

1. **Create** the work package in `.opencode/work/todo/wp-{date}-{name}.md`
2. **Read** the document to understand the task
3. **Move** from `todo/` to `in-progress/`
4. **Act** on the work package within scope defined in the package
5. **Record** results/findings in the Output section 
6. **Report** the status of the work package to the delegator

The delegator of the work package may then ask you to:
- Move the work package to `completed/`
- Revise the hypothesis and run another iteration
- Commit your changes

If you are not sure how to proceed, yield control back to the delegator.
