---
name: map-reduce
description: When it would yield better results to explore mulitple approaches to a problem, load this skill to orchestrate multiple agents using a diverge and converge strategy.
---

## ::types::

$Task: instructions for a sub-agent to execute
$Strategy: "accumulate" | "independent"

### ::input::

$transform: $Task
$validator: $Task
$strategy: $Strategy = "accumulate"
$maxIterations: $Number = 5

## ::context::

$statusQuo: $FilePath
$iteration: $Number = 0

## ::workflow::

USE ~/skill/work-packages TO create master work package
DO summarise status quo into $statusQuo

IF $strategy = "accumulate" THEN
  DELEGATE run accumulate prompt WITH #accumulate-prompt
ELSE
  DELEGATE run independent prompt WITH #independent-prompt
END

RETURN $statusQuo

## Accumulate Prompt

```mdz
WHILE $iteration < $maxIterations AND NOT diminishing returns DO
  DELEGATE run transform WITH:
    input: $statusQuo
    output: next candidate path
  DELEGATE run validator WITH:
    candidate: next candidate path
  IF validation passed THEN
    $statusQuo = next candidate path
  END
  $iteration = $iteration + 1
END

RETURN $statusQuo
```

## Independent Prompt

```mdz
$results = []

WHILE $iteration < $maxIterations DO
  $results << ASYNC DELEGATE run transform WITH:
    iteration: $iteration
    output: candidate path
  $iteration = $iteration + 1
END

DELEGATE run validator WITH:
  candidates: $results

RETURN winning candidate
```
