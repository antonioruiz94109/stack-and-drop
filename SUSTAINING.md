# Stack & Drop — sustaining operating agreement (pilot)

Status: **proposed, not activated**. Last reviewed: 2026-11-15. This file defines a target workflow, not evidence that Hermes/Qwen currently run it.

## Scope and source of truth
- Live app: https://antonioruiz94109.github.io/stack-and-drop/
- Source: this repository, `main` branch. Do not merge into Product Fit Kit, resurrect the legacy Netlify deployment, or move hosting without authorization.
- Catalog: `shoes.json`; published values must have individually verified, variant-matched evidence. Missing/uncertain measurements and prices remain blank.
- Checker: `.github/workflows/catalog-checker.yml`, `scripts/CHECKER.md`. Monday 13:23 UTC. It is intentionally **read-only** and its final coverage-quality gate can be red when manufacturer coverage is incomplete. A red coverage gate is not necessarily a broken app or broken checker.

## Roles and authority
| Actor | Responsibility | Authority |
| --- | --- | --- |
| GitHub Actions/Python | Scheduled manufacturer checks, artifact/summary capture, automated regression and PR checks | Read-only for catalog; status checks, no publication approval |
| Hermes (local harness; **unverified**) | Initiate handoffs, dispatch jobs to Qwen, record run IDs/evidence, report blocked local connectivity | No automatic direct-to-main writes, no merge authority, no secrets/access changes |
| Qwen (local model; **unverified**) | Primary proposed maintainer: classify report findings, reproduce issues, prepare tested fixes on feature branches and PRs | Can propose, cannot self-certify or publish |
| ChatGPT | Separate code/data/evidence reviewer when explicitly invoked; examine actual diff and test results | Independent assessment; no presumed unattended execution or GitHub approval |
| Antonio | Product owner: decide scope, review risk, authorize publication, security/access changes and consequential merges | Final decision-maker |

Do not represent an AI review comment as an authenticated GitHub human approval. Use genuine repository permissions and branch protections if available; those are **not configured by this file**. The author cannot sign off their own change.

## Weekly sustaining procedure
1. Every Monday, locate the newest scheduled `Weekly catalog review` run in GitHub Actions. Confirm `event=schedule`, timestamp, SHA, unit-test result, source-check execution, checksum, report upload and cache outcome.
2. Download/read the latest `catalog-review-<run id>` report before interpreting green/red. Report **source checks, fetched pages, coverage problems, candidates, possible changes, and per-brand categories**; distinguish blocked fetch, extraction gap, missing value, potentially changed text, and confirmed defect. Record comparisons to the prior run. Do not silently suppress coverage failures.
3. Hermes may pass *sanitized* report paths/URLs and a task description to Qwen. Qwen records exact commands, runtime/model availability, SHA, evidence, limitations, and whether it actually executed locally. Do not claim success from an offline or failed model endpoint.
4. Qwen may research and propose corrections only after verifying manufacturer identity, exact model/gender/variant, weight reference size, date/region, and price basis. Manufacturer marketing text is not an objective measurement. No access-control bypass or invented values.
5. For a proposed change, create a branch and PR. Attach source links, before/after evidence, tests, impact and rollback. Run the PR validation workflow and catalog checker where relevant; the coverage-quality gate may remain intentionally red and must be explained.
6. ChatGPT separately reviews the **actual PR diff** and reports PASS / CHANGES REQUESTED / BLOCKED against correctness, tests, scope, security, source evidence and regression risks. Do not certify an unavailable reviewer.
7. Antonio decides whether to publish code/catalog changes. Publication is not automatic. Merge only after required checks and explicit approval for material/catalog changes. Verify GitHub Pages deployment and smoke-test live behavior afterward.
8. Update the open sustaining issue/board card with report, findings, decisions, owner and next date. Artifacts expire after 90 days; retain concise durable issue/PR records.

## Escalation
- **Immediate review**: broken live app, unexpected change to `shoes.json`, runtime/checker crash, missing artifact, failed regression suite, security issue, incorrect published evidence.
- **Weekly review**: any coverage-quality red status, access blocks, source extraction failures, new candidates, suspected specification changes, rising coverage issues. A red status alone does not force an emergency rewrite.
- **Manual follow-up**: prolonged GitHub Actions schedule gap, stale catalog content, model/harness unavailable, source blocked by manufacturer.
- Avoid rewriting the checker solely to turn a red coverage gate green. No scraping bypasses, secret sharing, unauthorized model API subscriptions or purchases.

## Pilot acceptance test (must pass before claiming Qwen/Hermes own sustaining)
- [ ] Verify the actual Mac's Hermes runner and Qwen model/backend are reachable (record endpoint, version/model and safe execution permission *without publishing passwords or private network endpoints*).
- [ ] Run a **read-only** end-to-end review of an existing report using Hermes → Qwen. Save exact run timestamp, input artifact reference, output and error log. Correctly identify intentional coverage failures.
- [ ] Independently spot-check Qwen's classifications against the raw report.
- [ ] Give Qwen a small, reversible real issue or pre-approved seeded defect; demand reproduction, minimal proposed fix, tests and PR, without touching `main`.
- [ ] ChatGPT reviews PR diff independently; GitHub PR-validation checks execute. Compare reviewers' findings. No self-approval.
- [ ] Owner explicitly approves any material publication and confirms rollback/verification.
- [ ] Record owner, backup, cadence and escalation destination. Then mark this workflow **active** and consider project Sustaining.

## Current checkpoint: 2026-11-15
PR #1 merged 2026-11-11; 13 checker tests passed. Current-version push run https://github.com/antonioruiz94109/stack-and-drop/actions/runs/43088432699 reported **203 source checks, 143 fetches, 109 coverage problems**, 11 candidates and 11 possible changes; final quality gate intentionally failed and report artifact was retained. The most recent scheduled run observed was 2026-11-09, before the change. GitHub Pages build https://github.com/antonioruiz94109/stack-and-drop/actions/runs/43088431315 succeeded. Track handover in https://github.com/antonioruiz94109/stack-and-drop/issues/2. That original checkpoint did not test Qwen or Hermes; the subsequent connectivity attempt below remains blocked.

## Handoff contract and recovery
Every maintenance job must retain a private receipt with:
- Job ID, UTC timestamps, triggering workflow run/event and artifact ID, report SHA-256, catalog SHA-256, exact base and proposal commit SHAs.
- Hermes invocation and exit status; model/backend identity and a successful inference response. A CLI installation or a responding model list alone does not prove Qwen executed the task.
- Qwen output and errors, commands actually run, test results, proposed diff or explicit no-change/blocked disposition.
- Per-brand classifications and traceable report locations. Counts of coverage problems are not counts of incorrect shoes; excerpts and candidate links are unverified leads.
- Separate ChatGPT review of that exact proposal SHA, discrepancies found and resolved, and Antonio's batch approval reference if publication is requested.
Keep credentials, personal paths, private network addresses, correspondence and raw private logs out of this public repository. Publish only a sanitized outcome and evidence references.

Use current catalog rules in scripts/CHECKER.md. Do not rerun completed source checks merely to obtain green status. Reject stale input or mismatched SHAs; never overwrite an existing local checkout. On a blocked harness/model, record BLOCKED and escalate to Antonio. Do not silently substitute ChatGPT as the Qwen author or claim a manual task proves autonomous operation.

Weekly ownership: Qwen prepares; Hermes dispatches and records; ChatGPT reviews when invoked; Antonio resolves blocked handoffs and approves publication. A verified backup operator, response window and escalation delivery mechanism remain activation gates. A document is not a scheduler: GitHub's Monday 13:23 UTC trigger exists, but an unattended Hermes dispatch and unattended independent review have not been demonstrated. Preserve existing review schedules until their replacement is explicitly approved.

## Follow-up checkpoint: 2026-11-15
- ChatGPT independently inspected original PR head 507431585d11ae6696b4d2ee3e126cb567103e8a. PR validation run 43768964693 succeeded. The workflow grants contents: read, does not persist checkout credentials, and contains no merge/publication step. It checks syntax, 13 regression tests, JSON parsing and entrypoint presence; it does not verify catalog facts, UI behavior, or enforce independent approval.
- The local Hermes launcher was found but refused startup because its install-state lock was not writable from the execution session. The LM Studio CLI reported commit dcefd5a; its service probe did not complete and was interrupted. The expected local model endpoint was unreachable from that session. Service-down versus session-access restriction is unresolved. No Qwen inference or Hermes-to-Qwen pilot completed.
- The November 11 Actions log confirms 13 tests passed, 203 source checks, 143 fetches, 109 coverage problems, 11 candidate leads, 11 possible changes, and successful catalog checksum verification. Upload and cache steps succeeded; only the final coverage-quality gate failed.
- The old checker documentation permitted undated additions; this draft now restores the October 26 manufacturer-release requirement and other catalog rules. These documentation corrections are authored by ChatGPT, not Qwen, and are not an independent Qwen pilot.
- **Readiness: BLOCKED / not activated.** Keep PR #3 draft and unmerged. Required next evidence: successful Hermes-to-Qwen report review, a Qwen-authored tested maintenance proposal and independent review, current live desktop/mobile smoke test using the actual catalog count (203 at this checkpoint), the November 16 scheduled run, confirmed backup/escalation, and Antonio's approval.
