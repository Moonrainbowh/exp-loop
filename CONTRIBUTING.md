# Contributing

This repository is maintained as a deployable Codex skill, not a general essay about ML experimentation.

## Change Policy

- Prefer small changes tied to a concrete failure mode.
- Do not add new tracking or orchestration tools to the skill unless the user explicitly asks for them or the target repository already uses them.
- Keep `SKILL.md` as the default-load path. Move detailed record templates, test evidence, and maintenance notes into `references/`.
- Do not remove hard gates without adding equivalent pressure-test evidence.

## Required Checks

Before committing:

```bash
python scripts/check_skill.py
```

Also run any available host-level skill validator, such as `quick_validate.py`, when working inside Codex.

## Review Checklist

- Description still covers HPO, ablation, baseline comparison, failed-trial diagnosis, and model selection.
- Preflight gate still blocks missing project root, baseline, metric direction, data split, output path, run command, resource budget, and record path.
- Leakage/reproducibility gate still blocks unresolved test-set steering or cross-split preprocessing.
- Decision contract still prevents `continue` for tiny gains with unknown variance or worse resource cost.
- Experiment records still capture code state, data state, environment, resource use, failed-trial class, and artifact manifest.
- `references/test-results.md` is current when behavior changes.
