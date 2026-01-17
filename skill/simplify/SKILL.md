---
name: simplify
description: When a solution needs simplifying, load this skill with the map-reduce skill to find its essence.
---

## ::input::

$target: what to simplify
$essence: what must be preserved

## ::context::

$relevantHeuristics: a list of heuristics picked from #heuristics
  
## ::workflow::

FOR $heuristic IN $relevantHeuristics
  Apply to $target
  Check if $essence is preserved
  IF simpler and essence intact THEN
    Keep the change
  END
END

## Heuristics

1. Subtractive Iteration: remove one element and check if it still works. 
2. Forced Constraints: reimplement with half the lines and note what survives. 
3. Explain to Caveman: if you can't explain it simply, simplify it. 
4. Reverse Complexity Audit: list every abstraction and name the catastrophe it prevents. 
5. Rewrite Bet: two hours to rewrite from scratch, note what you keep.
