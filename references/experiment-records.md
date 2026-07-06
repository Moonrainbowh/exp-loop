# Experiment Records

Read this file when writing or updating experiment records, result cards, failed-trial summaries, asset manifests, final loop reports, or direction judgments.

## Group Record

Each trial group record must include:

- Group id or parent run id.
- Baseline parent reference and scoring method.
- Preflight status: project root, run command, output path, record path, resource budget, and metric direction.
- Validation policy: split identity, test-set policy, preprocessing fit scope, and model-selection policy.
- Trial matrix with status for every child trial.
- Code state.
- Data state.
- Environment state.
- Resource budget and actual resource use.
- Known contamination risks.
- Asset manifest.
- Result card with primary metric, important secondary metrics, comparison table or plot references, and worst regressions.
- Failure or anomaly notes for every failed or invalid trial.
- Direction judgment: `continue`, `pivot`, `abandon`, or `escalate`.
- Baseline-candidate evidence, if any.
- Next-step candidates grounded in observed results.

## Trial Matrix

Write configurable changes as dimensions and values when possible. Prefer this shape over prose-only descriptions:

```text
Trial:
Changed variables:
Fixed controls:
Expected effect:
Risk:
Status:
Result:
```

## Asset Manifest

List artifacts needed to audit or reproduce the result:

- Git commit, branch, and dirty diff or patch summary.
- Configs and command lines.
- Dependency lockfile, environment export, container image, or runtime version.
- Logs and error outputs.
- Seeds and data split identifiers.
- Dataset version, dataset hash, split file hash, and feature schema where available.
- Checkpoints or model artifacts.
- Prediction files.
- Metric files and scoring config.
- Plots, dashboards, reports, or comparison tables.
- Scripts or notebooks used for training, scoring, or analysis.

## State Fields

Use these fields when the project has no stricter template:

```text
Code state:
  commit:
  branch:
  dirty diff:
  dependency state:

Data state:
  dataset version/hash:
  split ids/hash:
  feature schema:
  preprocessing fit scope:

Environment:
  runtime:
  hardware:
  seeds:

Resource budget:
  planned:
  actual:
  stop condition:

Validation policy:
  validation set use:
  test set use:
  model selection rule:

Known contamination risks:
  leakage risks:
  repeated test-set tuning:
  unresolved concerns:
```

## Failed Trial Card

Record failed, interrupted, or invalid trials with this minimum card:

```text
Trial:
Status: failed/interrupted/invalid
Failure class: environment/data/config/code/resource/metric/unknown
Failed stage:
Error summary:
Reusable evidence:
Rerun recommendation: rerun/fix-first/ignore
Effect on group conclusion:
```

## Three Judgments

Separate these before deciding the next action:

- **Metric judgment**: Did the group improve the target metric and key secondary metrics against the baseline?
- **Engineering judgment**: Is the result reproducible, resource-acceptable, compatible with project constraints, and free of severe regressions or leakage risks?
- **Research judgment**: What did this group teach about the hypothesis, failure mode, or next search space?

Every decision must mention primary metric delta, secondary regressions, resource delta, variance/repeat evidence, reproducibility evidence, and whether continuing is worth the next run cost.

## Contamination Remediation

When a metric is contaminated by test-set steering, cross-split preprocessing, target leakage, or unclear split policy:

- Quarantine the contaminated metric from baseline promotion and broad-search decisions.
- Record the contamination source and affected runs.
- Re-fit preprocessing, scaling, imputation, feature selection, target transforms, and model selection only on allowed training data.
- Rerun baseline and candidate under the same clean protocol.
- Reserve a fresh or untouched holdout for final reporting when available.
- Use `escalate` if clean validation cannot be constructed from current artifacts.

## HPO Reconstruction Without Writes

If the user forbids file edits or persistent record creation:

- Produce a non-persistent reconstructed group report in the response.
- Mark it as needing durable recording later.
- Include parent group candidate, child trial list, trial statuses, objective metric, direction, baseline, split identity, failed/invalid run handling, and artifact references.
- If metric direction, baseline, split identity, or failed/invalid run status cannot be established, output `escalate` or `blocked` instead of selecting a winner.

## Tiny Gain Rule

For small metric gains, especially when resource use worsens:

- Require repeated seeds, confidence intervals, or historical variance comparison before trusting the gain.
- Compare cost-normalized value: training time, inference latency, memory, model size, parameter count, and failed-run rate.
- Continue only if the project has explicit acceptance criteria for the resource tradeoff.
- Otherwise choose `pivot` or `escalate`.

## Report Shape

Use this shape for progress reports and final summaries:

```text
Experiment loop: running/completed/blocked
Project:
Baseline:
Goal:
Trial group:
Results:
Key finding:
Direction judgment: continue/pivot/abandon/escalate
Baseline candidate:
Next step:
```

Keep reports concise. Include exact paths, commands, and metric values when they matter for reproducibility.

## Common Mistakes

- Hard-coding paths, runtime environments, note directories, or project names.
- Introducing a new tracker, sweep framework, or orchestrator without user approval or repository evidence.
- Treating the newest run as the baseline without evidence.
- Running without project root, baseline, metric direction, split identity, output path, run command, resource budget, or record path.
- Comparing trials without checking leakage, split contamination, preprocessing fit scope, or test-set steering policy.
- Recording metrics without code version, dirty diff, data version/hash, split hash, dependency state, or seeds.
- Running single isolated trials when a small comparison matrix is needed.
- Running 2-6 trials by default without classifying smoke/formal/ablation/HPO mode or estimating cost.
- Hiding the parent-child relationship between a trial group and its trials.
- Describing trial changes in prose when a config matrix would make attribution clearer.
- Optimizing the headline metric while ignoring secondary regressions, variance, training cost, inference cost, model size, or failure rate.
- Reading raw logs while ignoring existing leaderboards, comparison tables, plots, or dashboards.
- Updating an index but leaving no durable explanation of failed trials.
- Dropping failed or invalid trials from the record.
- Recording failed trials without classifying environment/data/config/code/resource/metric failure.
- Repeating a failed direction because it is easy to run.
- Promoting a baseline automatically when the project expects human review.
- Selecting an HPO winner when metric direction, baseline, split identity, or failed-run status is unknown.
- Treating a tiny one-seed gain as meaningful when resource use worsens and variance is unknown.
