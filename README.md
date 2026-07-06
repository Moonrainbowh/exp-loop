# exp-loop

`exp-loop` is a Codex skill for disciplined iterative machine-learning experiments. It is designed to stop agents from running expensive or contaminated experiments before baseline, metric direction, data split, execution command, resource budget, and recording rules are known.

## What It Enforces

- Preflight gate before running experiments.
- Leakage and reproducibility checks before trusting results.
- Trial-group structure for ablation, HPO, and model-selection work.
- Decision contract for `continue`, `pivot`, `abandon`, and `escalate`.
- Next-step review gate before resource-consuming follow-up actions.
- Reproducible experiment records with code, data, environment, resources, failed-trial status, and artifact manifest.

## Repository Layout

```text
SKILL.md
agents/openai.yaml
references/
  experiment-records.md
  pressure-scenarios.md
  test-results.md
scripts/
  check_skill.py
```

## Install

Clone this repository into a Codex skills directory, or copy the folder as `exp-loop` under your existing skills root.

```bash
git clone https://github.com/Moonrainbowh/exp-loop.git exp-loop
```

## Validate

Run the local static checks:

```bash
python scripts/check_skill.py
```

If you also have Codex's bundled skill validator available, run it against the repository root:

```bash
python path/to/quick_validate.py .
```

## Maintenance Rule

Changes to this skill should be driven by observed failure modes. When behavior changes:

1. Add or update a pressure scenario.
2. Run a no-skill or baseline comparison when useful.
3. Run a with-skill retest.
4. Update `references/test-results.md`.
5. Keep `SKILL.md` focused; move record templates and review evidence into `references/`.

## Deployment State

The current version has completed two pressure-test cycles and received a final `ready` review. See `references/test-results.md` for evidence.
