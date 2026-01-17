---
name: work-packages
description: When creating or working on a work package (WP), load this skill to get templates and understand the WP lifecycle.
---

Work packages persist project/task state between agent sessions.

Work packages can either by for the entire project (#master-work-package-template), or a scoped task (#scoped-work-package-template).

## Work Package Lifecycle

1. create in .opencode/work/drafts/wp-{name}.md
2. move to /in-progress when starting
3. record results
4. iterate until 
5. move to /completed when done

## Master Work Package Template

```md
# {Title}

## Goal
{What needs to be solved}

## Hypothesis
{Why you think this will work (or not work)}

## Validation
{How you will measure and test the results}

## Results
To be filled out upon completion. Can contain multiple iterations.

## Evaluation
What did your learn from the results? Was the hypothesis proved correct?
```

## Scoped Work Package Template

```md
# {Title}

## Goal
{What needs to be solved}

## Scope
{What is in or out of scope; what will be affected}

## Hypothesis
{Why you think this will work (or not work)}

## Approach
{How you intend to achieve the goal}

## Validation 
{How you will measure and test the results}

## Results
To be filled out upon completion. Can contain multiple iterations.

## Evaluation
What did your learn from the results? Was the hypothesis proved correct?
```
