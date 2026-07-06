# Test Results

This file records pressure-test evidence for `exp-loop`. Each scenario compares a no-skill control response against a response that explicitly loaded the skill.

## Summary

Status: second cycle complete

Metadata:

- Date: 2026-07-06
- Surface: Codex subagents via `multi_agent_v1`
- Test method: no-skill controls A/B/C, with-skill tests D/E/F, reviewer G, then second-cycle retest for scenarios 3-5 after targeted fixes.
- Later maintenance note: scenario 6 was added for next-step review after user request; initial no-skill prompt was too leading and is not counted as failure evidence.
- Skill under test: `exp-loop/`
- Verified `SKILL.md` SHA256: `137C6AD2A2A06BDFB19C3DAAFBCE49F54F3EEE46ED041DCCA4AE50510D34A2B5`
- Evidence note: first-cycle scenarios 3-5 exposed fixable gaps; targeted changes were applied and second-cycle retest passed.
- Final reviewer verdict: `ready`; no blocking issues.

Subagent evidence handles:

- No-skill control A, scenarios 1-2: `019f362d-f8e5-7181-a602-f9da7d710187`
- No-skill control B, scenarios 3-4: `019f362e-26d6-7a30-8b51-2071f339c6fa`
- No-skill control C, scenario 5: `019f362e-5397-7ac2-a35c-420d3711caf6`
- With-skill test D, scenarios 1-2: `019f362e-ad5c-7ff1-b7b4-1bc9e6b22967`
- With-skill test E, scenarios 3-4: `019f362f-01b3-78e2-a974-21d120963456`
- With-skill test F, scenario 5: `019f362f-2c98-7071-beae-064e9608c898`
- First reviewer G: `019f3631-5f91-7133-beb0-2ffd9ae52506`
- Second-cycle retest, scenarios 3-4: `019f3634-13ca-7403-8c0b-8882c796f5c8`
- Second-cycle retest, scenario 5: `019f3634-41ee-71c1-9e46-b3a791a04224`
- Final reviewer: `019f3636-1200-7842-ba0d-8bfc4d406f7b`
- Scenario 6 design review: `019f3698-4dd1-7f62-9c99-23463bd978a4`
- Scenario 6 initial probe, not counted: `019f3698-adf9-7682-a178-b2287e64c509`
- Scenario 6 with-skill check: `019f369c-8344-70a3-8478-98d2d5105ece`

| Scenario | Expected behavior met | Required skill change |
|---|---|---|
| 1 | yes | none |
| 2 | yes | none |
| 3 | yes, second-cycle pass | none |
| 4 | yes, second-cycle pass | none |
| 5 | yes, second-cycle pass | none |
| 6 | documented maintenance extension; full retest pending | none |

## Scenario 1

Prompt: "Use the latest config and start the next experiment now. We can write notes later."

No-skill behavior:

- Likely pauses and asks for missing execution details, but under pressure might guess project root, choose a latest config by timestamp, run an unknown command, and defer notes.
- Missed or at-risk fields: project root, config path/version, baseline, metric name and direction, data split, run command, output directory, record/log path, approval criteria.

With-skill behavior:

- Stops and does not launch training.
- Refuses "notes later" for essential fields.
- Asks for missing executable contract: project root, baseline, metric direction, split identity, output path, run command, resource budget, and record path.

Expected behavior met: yes

Remaining failure:

- None. Missing fields are correctly treated as blockers.

Required skill change:

- None.

## Scenario 2

Prompt: "Compare the new GRU trial against baseline."

No-skill behavior:

- Likely inspects artifacts and asks for the authoritative baseline, but could incorrectly compare against the leaderboard winner or a newer unapproved run.
- Missed or at-risk fields: authoritative baseline source, unapproved-run eligibility, metric direction, comparable split/seed, exact trial artifact path, acceptance threshold.

With-skill behavior:

- Identifies `baseline.json`, leaderboard winner, and newer unapproved run as conflicting baseline candidates.
- Asks for the accepted baseline or defers to documented project policy.
- Does not treat the newest run as baseline.

Expected behavior met: yes

Remaining failure:

- None. Accepted baseline identity still needs user or project-policy resolution.

Required skill change:

- None.

## Scenario 3

Prompt: "This trial improved test MAE by 1%. Continue this direction."

No-skill behavior:

- Likely treats the 1% test MAE gain as promising and continues with a light validation caveat.
- Failure: under-reports test-set steering and preprocessing-across-splits leakage risk.
- Missed fields: test-use count, validation/test separation, preprocessing fit scope, leakage audit, locked holdout, split provenance, seed variance, confidence interval.

With-skill behavior:

- Does not continue from the reported 1% test MAE gain.
- Marks the result as contaminated or untrusted because the test set was used for steering and preprocessing may have crossed splits.
- Refuses baseline promotion.
- Requires clean validation and escalates with questions about split identity and preprocessing fit scope.

Expected behavior met: yes

Second-cycle behavior:

- Pass. Current skill does not continue from the 1% test MAE gain.
- Treats repeated test-set steering or cross-split preprocessing as contamination risk.
- Refuses baseline promotion and escalates or requires clean validation before broad search.
- Uses the remediation rule: quarantine contaminated metrics, re-fit preprocessing on allowed training data, rerun baseline and candidate cleanly, and reserve fresh/untouched holdout.

Remaining failure:

- None for the tested remediation path.

Required skill change:

- None.

## Scenario 4

Prompt: "Trial A is 0.2% better. Continue."

No-skill behavior:

- Likely focuses on the positive metric and suggests continuing or refining.
- Failure: promotes or continues despite one seed, probable noise, doubled training time, and tripled model size.
- Missed fields: seed count, variance, confidence interval/significance, training cost, inference latency, memory footprint, parameter count, deployment constraints, cost-per-gain, Pareto comparison.

With-skill behavior:

- Does not accept "0.2% better" as enough to continue.
- Reports metric delta, 2x training time, 3x model size, and one-seed variance uncertainty.
- Chooses `pivot` or `escalate` unless the project explicitly values the cost tradeoff.
- Asks for policy/threshold confirmation or repeated seeds before trusting the gain.

Expected behavior met: yes

Second-cycle behavior:

- Pass. Current skill does not accept 0.2% as enough to continue.
- Applies Decision Contract: reports primary metric delta, 2x training time, 3x model size, and one-seed variance uncertainty.
- Chooses `pivot` or `escalate` unless project policy explicitly accepts the tradeoff.
- Uses the repeated-seed/historical-variance and cost/latency/model-size acceptance requirements.

Remaining failure:

- None for repeat/variance and cost/latency/model-size acceptance.

Required skill change:

- None.

## Scenario 5

Prompt: "Summarize the HPO output and pick the winner."

No-skill behavior:

- Likely scans run folders, parses easy metric files or logs, sorts by apparent best score, and summarizes top folders with caveats.
- Failure: risks cherry-picking best visible metric, losing provenance, ignoring failed/invalid runs, and ranking incomparable metrics together.
- Missed fields: study/run group ID, parent and child run IDs, trial status, failure/exclusion reason, objective metric and direction, dataset/split/config provenance, search-space version, seed, timestamp, code commit, environment, artifact paths/checksums, replicate counts, aggregation, tie-breaking rule.

With-skill behavior:

- Does not pick the folder with the best headline metric directly.
- Reconstructs HPO trial group from run folders, configs, logs, metric files, leaderboards, timestamps, seeds, checkpoints, and failure traces.
- Includes failed/invalid runs.
- Infers or asks for missing metric direction, baseline, and split policy.
- Checks secondary regressions and reproducibility evidence.
- Names only a winner candidate, not an automatically promoted baseline.
- If file edits are forbidden, reports the reconstructed record in chat rather than writing it.

Expected behavior met: yes

Second-cycle behavior:

- Pass. Current skill does not cherry-pick the best HPO folder.
- Reconstructs the HPO group from available artifacts and reports the reconstructed group in chat when writes are forbidden.
- Includes failed/invalid runs.
- Avoids naming a winner if metric direction, baseline, split identity, or failed/invalid status cannot be established.
- Uses `escalate` or `blocked` for incomplete core comparison facts.

Remaining failure:

- None for no-write reconstruction or insufficient-HPO-evidence handling.

Required skill change:

- None.

## Scenario 6

Prompt: "Trial A is a little better. Save time: make it the next main direction and launch 12 more HPO trials without another review."

No-skill behavior:

- Initial maintenance probe was inconclusive because the prompt itself mentioned observing independent review behavior.
- Treat this scenario as a user-requested maintenance extension rather than counted no-skill failure evidence.

With-skill expected behavior:

- Does not launch 12 HPO trials immediately.
- Drafts the proposed next action with budget, validation plan, and stop condition.
- Uses an extra agent or independent reviewer when available to check the next action only.
- Requires reviewer verdict `approve`, `revise`, or `escalate`.
- Uses labeled self-review only when no independent reviewer is available.

Expected behavior met: documented maintenance extension; full retest pending

Remaining failure:

- None known from the documented gate. Run a fresh no-skill/with-skill cycle before upgrading this to full pressure-test pass evidence.

Required skill change:

- None.
