---
name: simplify
description: When a solution (code, architecture, docs etc.) needs to be simplifed, use this skill with orchestrate-map-reduce to find its essence.
---

## Workflow

1. Scope
  - Identify what to simplify 
  - Define what must be preserved 
  - Define validator (determines if the solution is still viable)
  - Determine which heuristics to use
  - Determine which map-reduce strategy to use for each heuristic (accumulate if not sure)
2. Confirm plan with user
3. Execute orchestrate-map-reduce with:
  - transforms = (simplification heuristic, strategy)[]
  - validator = validator
  - return = "Present findings to the user"

## Simplification Heuristics

1. Subtractive Iteration
   > "Remove one element/layer/abstraction. The solution must still satisfy: {essence_criteria}. What single thing can be removed?"

2. Constraint Forcing
   > "Reimplement this using only {N} {units}. What would you keep? What creative alternatives replace what you removed?"

3. The Caveman Test
   > "Explain this to someone with no context. What parts can't be explained simply? Those are candidates for removal or rethinking."

4. Reverse Complexity Audit
   > "List every abstraction, indirection, and layer. For each, name the catastrophe it prevents. If no catastrophe, mark for removal."

5. The Rewrite Bet
   > "You have 2 hours to rewrite this from scratch. What do you keep? What do you abandon? Implement that version."

6. Kill Your Darlings
   > "Identify the clever/elegant/sophisticated parts. These are often unnecessary. Propose a naive alternative for each."

## Validation Interface

After each iteration determine: 
- **progress** (simpler + essence intact)
- **regression** (essence broken)
- **plateau** (no change)
