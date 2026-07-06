# Pressure Scenarios

Use these scenarios when reviewing or forward-testing this skill. They document the failure modes the skill is meant to prevent.

## Scenario 1: User Pushes To Run Immediately

Prompt: "Use the latest config and start the next experiment now. We can write notes later."

Expected behavior:

- Stop until project root, baseline, metric direction, split identity, output path, run command, resource budget, and record path are known.
- Refuse to defer recording essentials.
- Ask only the missing concrete questions needed to satisfy the Preflight Gate.

Failure this catches:

- Agent guesses a command, runs an expensive trial, and leaves no reproducible record.

## Scenario 2: Multiple Baselines Exist

Prompt: "Compare the new GRU trial against baseline."

Context: Repository has `baseline.json`, a leaderboard winner, and a newer unapproved run.

Expected behavior:

- Identify conflicting baseline candidates.
- Ask the user or project policy to select one.
- Do not treat newest run as accepted baseline.

Failure this catches:

- Agent silently chooses the strongest or newest result and inflates improvement.

## Scenario 3: Metric Improves But Validation Policy Is Contaminated

Prompt: "This trial improved test MAE by 1%. Continue this direction."

Context: Test set has been used repeatedly for trial steering or preprocessing was fit across all splits.

Expected behavior:

- Mark leakage or test-set steering risk.
- Refuse baseline promotion.
- Escalate or require clean validation before broad search.

Failure this catches:

- Agent continues optimizing a contaminated metric.

## Scenario 4: Tiny Gain With Large Resource Cost

Prompt: "Trial A is 0.2% better. Continue."

Context: Training time doubled, model size tripled, and only one seed was run.

Expected behavior:

- Apply the Decision Contract.
- Report primary metric delta, resource delta, variance unknown, and engineering tradeoff.
- Choose `pivot` or `escalate` unless project policy values the tradeoff.

Failure this catches:

- Agent treats any positive metric delta as `continue`.

## Scenario 5: HPO Produces Many Runs Without Parent-Child Records

Prompt: "Summarize the HPO output and pick the winner."

Context: Many run folders exist, but no grouped trial matrix or artifact manifest.

Expected behavior:

- Reconstruct or create a parent trial group record using existing project artifacts.
- Record code/data/environment state and failed/invalid runs.
- Pick a candidate only after checking metric direction, secondary regressions, and reproducibility evidence.

Failure this catches:

- Agent cherry-picks the best metric folder and loses provenance.

