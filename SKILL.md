---
name: exp-loop
description: Use when users ask to run or manage iterative machine-learning experiments, baseline comparison, HPO, ablation, experiment tracking, failed trial diagnosis, model selection, or deciding whether an experiment direction should continue, pivot, stop, or need human input.
---

# Exp Loop

## Overview

Use this skill to turn project evidence into bounded trial groups, compare them against a baseline, record what happened, and decide the next move.

Discover paths, environments, metrics, training commands, and note systems from the current repository and the user's latest instructions.

Do not add a new tracking or orchestration tool unless the user explicitly asks for it or the repository already contains clear evidence that the tool is part of the project workflow.

## Core Contract

Each loop cycle has four phases:

1. **Discover** project conventions, current baseline, scoring method, run commands, and experiment-record location.
2. **Plan** one coherent trial group around a falsifiable hypothesis.
3. **Run** trials using the project's own training and scoring entry points.
4. **Wrap** results into durable records, then decide `continue`, `pivot`, `abandon`, or `escalate`.

Keep these responsibilities together in this skill. Do not split the work into separate "new experiment" or "wrap experiment" skills unless the user explicitly asks for a project-specific automation layer.

## Preflight Gate

Before changing code or launching training, inspect the project and establish the minimum executable contract.

- Instructions: `AGENTS.md`, `CLAUDE.md`, README, docs, or runbooks.
- History: experiment dirs, logs, indexes, notebooks, notes, dashboards, or prior summaries.
- Baseline: checked-in config, registry, result table, accepted experiment, or user-provided baseline.
- Scoring: primary metric, comparison direction, aggregation, tie-breakers, thresholds, and secondary regressions.
- Validation: train/validation/test split identity, split storage, test-set policy, and preprocessing fit scope.
- Execution: environment, train/score commands, outputs, resource limits, and resume behavior.
- Records: where plans, trial matrices, result cards, conclusions, and next candidates live.
- Tooling: trackers, sweep/HPO tools, config systems, workflow runners, dashboards, notebooks, or scripts already used by the project.

Do not run an experiment until these are known: project root, baseline, metric direction, data split, output path, run command, resource budget, and record path. If any are missing or multiple plausible answers exist, stop and ask the user to choose.

## Leakage And Reproducibility Gate

Treat leakage and irreproducibility as blockers, not record-keeping details.

- Confirm train/validation/test split identity before comparing trials.
- Confirm preprocessing, scaling, feature selection, imputation, target transforms, and model selection are fit only on allowed training data.
- Do not use the test set for routine trial steering unless the project policy explicitly allows it; if it has already happened, record contamination risk and escalate.
- Record code version, dirty diff, data version, split identifiers, dependency environment, random seeds, and resource budget before trusting a result.
- If any leakage or split-contamination risk cannot be ruled out, do not promote a baseline or continue broad search from that metric.
- For contaminated metrics, quarantine the result, re-fit preprocessing on allowed training data, rerun baseline and candidate under the same clean protocol, and reserve a fresh or untouched holdout for final reporting.

## Tool Boundary

- Preserve existing tracker, sweeper, config-runner, or orchestrator semantics when the repo already uses them.
- If no such system exists, use repository-native records such as markdown, JSON, CSV, logs, or existing scripts.
- Do not install, initialize, migrate to, or recommend a new tracking or orchestration tool during normal loop execution.
- If a new tool appears useful, report the tradeoff and ask before changing dependencies or workflow.

## Planning A Trial Group

A trial group is a parent record containing comparable child trials around one theme. Prefer 2-6 trials unless the user requests a different budget or the project convention says otherwise.

Define:

- Group id or run id, following the project naming convention.
- Baseline parent reference and comparison metric.
- Hypothesis and expected behavior change.
- Trial matrix: variable changes, fixed controls, expected effects, and risks.
- Attribution boundary: constants that make results interpretable.
- Stop condition: target metric, maximum trials, time/compute budget, or decision checkpoint.

Classify the run before sizing the matrix: smoke trial, formal comparison, ablation, or HPO/sweep. Estimate cost before launching. The 2-6 trial default does not override resource limits or repeated-seed needs.

Use history before invention. Repeat a failed direction only when the new trial changes a key premise. Use a hand-designed matrix for hypotheses, ablations, architecture changes, and small budgets; use existing sweep/HPO tooling only when the repo already has it and the question is parameter search.

## Running Trials

Follow established commands and file layout. If no command is documented, infer the narrowest likely command from scripts/configs and report the assumption before long-running work.

During execution:

- Run one trial at a time unless the project explicitly supports parallel runs.
- Preserve logs, configs, seeds, checkpoints, outputs, and metric files.
- Report each completed trial with path, key metric, and immediate interpretation.
- Record failed, interrupted, or invalid trials instead of hiding them.
- Do not rename existing experiment output directories after results exist unless project tooling supports it.

Parallelize only when output dirs, run ids, seeds, devices, logs, and checkpoint names are isolated. If unclear, run sequentially.

## Wrapping Results

After a trial group finishes, update project records with project tools when available. Otherwise write the smallest durable record future agents can find.

Read [experiment-records.md](references/experiment-records.md) when writing experiment records, result cards, failed-trial summaries, asset manifests, or final loop reports.

Read [pressure-scenarios.md](references/pressure-scenarios.md) when reviewing or updating this skill, or when forward-testing whether an agent will stop on missing preflight data, leakage risk, weak baselines, expensive tiny gains, or ungrouped HPO output.

Read [test-results.md](references/test-results.md) when reviewing deployment readiness or checking whether prior pressure-test failures have been fixed.

Separate mechanical scoring from judgment. Scripts may compute metrics; the agent explains direction value and next action.

Prefer existing comparison tables, leaderboards, plots, dashboards, or result cards over isolated logs.

If persistent record creation is not allowed, produce a non-persistent reconstructed group report in the response and mark it as needing durable recording later. If metric direction, baseline, split identity, or failed/invalid run status cannot be established, output `escalate` or `blocked` instead of selecting a winner.

## Decision Contract

Use these judgments after each trial group:

| Judgment | Use when | Next action |
|---|---|---|
| `continue` | The direction improves the target without unacceptable regressions. | Expand or refine the strongest variant. |
| `pivot` | Part of the idea works but causes clear tradeoffs or exposes a better question. | Keep the useful part and constrain the failure mode. |
| `abandon` | The direction repeatedly fails and no new premise explains a retry. | Stop spending compute on this direction. |
| `escalate` | Baseline choice, metric priority, data quality, resource limits, or product tradeoffs need human judgment. | Ask the user a concrete decision question. |

Every conclusion must state:

- Primary metric delta versus baseline.
- Secondary regressions and worst affected slice/group/stage, if known.
- Resource delta: training time, inference cost, memory, model size, or failed-run rate when available.
- Variance evidence: repeated seeds, confidence interval, historical run variance, or an explicit note that variance is unknown.
- Reproducibility evidence: code state, data state, split identity, environment, seeds, and artifact paths.
- Decision: `continue`, `pivot`, `abandon`, or `escalate`, with why the next action is worth the cost.

Before choosing the next action, separate metric judgment, engineering judgment, and research judgment. Quantify first, explain second, modify third. A tiny metric gain with large cost, variance uncertainty, leakage risk, or severe secondary regression is not enough for `continue`.

For sub-threshold or tiny gains, require repeated seeds or historical variance evidence before trusting the gain. Require explicit cost, latency, memory, model-size, and failure-rate acceptance criteria before `continue` when resource use worsens.

Never automatically promote a baseline unless the user or project policy explicitly authorizes automatic promotion. By default, produce a baseline candidate with evidence and wait for human confirmation.

## Stopping Conditions

Stop the loop and report when any condition applies:

- User-specified target, budget, or maximum round count is reached.
- The same direction fails for 3 consecutive trial groups without a new explanation.
- Metrics conflict with user goals and need a priority decision.
- Data, environment, hardware, or repository state blocks trustworthy execution.
- The next step would require broad refactoring, data changes, or baseline promotion not already authorized.

If the user gives no maximum round count, run one complete trial group and ask before continuing.
