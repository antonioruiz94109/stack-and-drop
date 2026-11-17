# Stack & Drop sustaining agreement

Last reviewed: November 17, 2026. Status: **Sustaining — weekly maintenance review active**. Publication remains approval-gated. A full autonomous research or software-repair service is not claimed.

## Scope and authority

Stack & Drop remains standalone at https://antonioruiz94109.github.io/stack-and-drop/, with this repository's main branch as the published source. Preserve the separate Product Fit Kit project and existing work. The catalog rules in scripts/CHECKER.md apply: exact model/generation/gender/variant evidence, manufacturer release evidence for additions, correct price basis, and explicit unknowns. Never invent facts or bypass manufacturer access restrictions.

| Actor | Responsibility |
| --- | --- |
| Qwen | Primary maintainer: review findings and prepare evidence-backed proposed corrections |
| Hermes Desktop | Local scheduled dispatch, saved execution receipts and visible failure reporting |
| ChatGPT | Collect verified artifacts and independently review actual Qwen results, tests and proposed diffs |
| GitHub Actions | Read-only manufacturer monitoring and PR regression checks |
| Antonio | Product owner, recovery operator and final publication approval |

No unattended merge, publication, purchases or security changes. AI review is not authenticated human approval. CLI is backup only after a demonstrated Desktop limitation.

## Weekly cadence

- Monday 13:23 UTC: GitHub's existing catalog checker captures report/artifact and reports incomplete coverage honestly.
- Monday 10:00 America/Chicago: existing scheduled reviewer preserves the current week's verified report, catalog and run/commit provenance.
- Monday 10:30 America/Chicago: Hermes dispatches Qwen to execute the reviewed triage helper and save a dated maintenance assessment.
- Monday noon America/Chicago: existing scheduled reviewer independently checks Qwen's handoff and reports proposals or blockers to Antonio.

The private handoff contract specifies paths and source hashes. Require current-week report date, run ID, artifact ID, catalog commit, exact input hashes, reviewed script hash, execution result, Qwen's assessment and independent review. Preserve separate receipts for reruns. Missing, stale, changed or incomplete evidence is BLOCKED, never a substitute success. A deterministic helper result alone is not a completed Qwen review.

Local prerequisites are an awake Mac, running Hermes background scheduler and available LM Studio model. No protection or sleep settings are changed by this agreement. A missing noon handoff must be surfaced to Antonio that day. Antonio is the recovery operator; this does not guarantee a human response time.

## Maintainer proposal and review

`scripts/triage_report.py --report REPORT --catalog CATALOG --output RESULTS` performs offline triage only. Qwen authored the identity repair; ChatGPT supplied independent tests and packaged required CLI paths. Candidate labels/slugs cannot establish identity. Exact nonempty IDs must identify one entry; ambiguous or missing IDs are held. Specification matching preserves the raw gender/variant-specific entry. Track spikes are excluded. Seven adversarial tests cover the prior defects.

This helper neither fetches manufacturer pages nor clears the research backlog. Holds require Qwen's separate evidence review before any addition or correction is proposed. Material fixes require a branch/PR, meaningful tests, independent review, Antonio's approval and post-publication verification. No-change reviews are valid outcomes; unresolved source coverage remains visible maintenance work.

## Acceptance evidence

- Hermes Desktop and actual local Qwen inference/tool execution verified.
- Qwen authored and corrected a real identity-matching defect; independent seven-test suite passes.
- Draft PR #3 contains the sanitized helper and tests; code head 3239bf35 passed PR validation run 44127078366. The public app/catalog have not changed.
- November 16 scheduled checker run 43901597589 retained artifact 14241158601: 203 checks, 142 fetches, 110 coverage problems, 11 leads and one excerpt flag. Final coverage gate failed as designed; these are not 110 proven incorrect shoes.
- Independent live desktop/mobile smoke passed against 203 entries.
- Deliberately missing input produced an automatic explicit failed job and visible Desktop recovery message on November 16.
- Successful scheduled handoff: November 17, 10:33–10:37 America/Chicago, real local Qwen execution, saved review, matching input/result hashes, successful local delivery and separate independent review. Reviewer corrected one narrative count: Nike had 36 pages fetched, 35 specs extracted, 38 entries. No catalog impact.
- Recurring Hermes job active: Mondays 10:30 local Central time; next verified occurrence November 23. Existing 10AM/noon reviewer cadence remains active. Failure and successful delivery paths have both been demonstrated.

## Recovery and escalation

Immediate: broken app, unexpected catalog changes, missing artifacts, regression failure or incorrect published evidence. Weekly: access/extraction gaps, candidate holds and suspected source changes. Preserve evidence and report BLOCKED when the model or handoff is unavailable; do not silently substitute ChatGPT as maintainer. Restore the current verified inputs or local runtime, rerun the same reviewed job, and independently review its new receipt. Never rewrite the checker just to turn its coverage gate green.

Track outstanding work in issue #2. PR #3 remains draft/unmerged until the owner authorizes its merge; that approval queue is separate from local read-only maintenance activation.
