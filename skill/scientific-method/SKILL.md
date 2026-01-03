---
name: scientific-method
description: When a task requires observation and verification, use this skill to extend work packages to deliver hypothesis-driven iteration.
---

## Workflow

1. **Evaluate** the current state (screenshot, read output, check files)
2. **Hypothesize** what you think will reach the desired state (or have no effect, if stating a null hypothesis)
3. **Predict** what will be the effect of your intervention (if any)
3. **Act** by implementing your proposed solution
4. **Observe** the impact of the intervention
5. **Verify** if the hypothesis was correct
5. **Repeat** until goal achieved

Note: in certain circumstances e.g. performance testing, debugging etc., you might want to state a null hypothesis e.g. "The 3rd party API latency is unrelated to the crash time". In most cases this is not required.

## Tracking 

Track the iterations an experiment in a work package.

Include in it:

```markdown
## Hypothesis
{What you think is happening and what you predict will fix it}

## Results

### Iteration {n}
- Hypothesis: {The theory being tested}
- Action: {The specific step taken}
- Prediction: {The expected observable result if the hypothesis is true}
- Observed: {The actual result}
- Conclusion: {Validated or falsified? What is the next step?}
```

Update this document as you iterate.

## Finish When

- Goal achieved
- Hypothesis proven wrong with no alternative
- Diminishing returns
