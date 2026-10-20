# Weekly catalog checker

Runs Mondays at 13:23 UTC (8:23 a.m. Chicago daylight time / 7:23 a.m. standard time), and manually from Actions → Weekly catalog review → Run workflow. Editing the checker also triggers a verification run.

Reports appear in the workflow run summary and downloadable `catalog-review` artifact (90-day retention). GitHub schedules may be delayed and public-repository schedules can be disabled after 60 days without repository activity.

The workflow has contents: read permission only. It does not update shoes.json, open changes, or publish catalog entries. A checksum verifies shoes.json is untouched. No external AI, purchases or personal credentials are required.

Scope: all ten current catalog brands—Altra, ASICS, Brooks, HOKA, New Balance, Nike, PUMA, Saucony, Topo Athletic and adidas. Checks selected men's/women's manufacturer listings and source URLs for all catalog entries. Per-brand report coverage distinguishes fetched pages from extracted specifications. Listing coverage is not exhaustive. Blocked requests, empty extraction and missing pages appear as coverage problems; they never imply no changes or discontinued shoes. New Balance may reject automated requests with HTTP 403 and then needs manual review.

Candidates are unverified. URL-level normalization removes query strings and New Balance color/size identifiers; reviewers must still eliminate accessories, duplicate models, widths and colors, confirm gender, and assess release evidence where available. Recency within two years is preferred, not required. Discovery time is not release time.

Labelled specification excerpts are compared to a prior successful snapshot. These are possible source-text changes, not validated numerical corrections, and may include nearby or related-product wording. First-time snapshots show source evidence beside catalog values in report.json. Weight reference sizes and manufacturer claims need review. Prices and missing details are monitored as described below.

Snapshots are cached between runs; if GitHub evicts the cache, the checked-in initial baseline is used. report.json records the comparison date. A failed fetch preserves the last successful snapshot. Review the report before proposing any data change, then run catalog checks. Prepare verified changes for Antonio’s explicit batch approval before publishing. Scheduled reviews must not publish.

Local run: `python3 scripts/check_catalog.py --catalog shoes.json --output checker-report`. Tests: `python3 -m unittest discover -s scripts -p 'test_check_catalog.py'`.

The all-brand trial on October 19 fetched 88/157 source pages locally. New Balance, ASICS, Brooks, HOKA and adidas returned access blocks; monitoring remains enabled to retry weekly, but these brands require manual research while blocked. Candidate counts refer to links, not verified distinct shoes. Brand coverage on GitHub runners may differ. No blocked-access bypass is attempted.

## Held release evidence

The 11 unresolved entries are tracked in release-holds.json. Each Monday the checker revisits their manufacturer pages and known supporting sources, captures nearby exact-model wording, and flags initial evidence, changes or unavailable pages in a separate report section. Prior successful evidence is retained on fetch failures. Published model/gender versions are skipped. This is a known-source watch, not an exhaustive web search; report.json also supplies follow-up search queries for the reviewer. New dates may describe reviews, restocks, colorways or other variants and never clear a hold automatically. Verify the exact model/version and regional context before publication; missing date evidence alone is not an exclusion.

## Current publication policy

October 19, 2026: the user authorized flexible recency. Two years is a preference, not a mandatory cutoff. Missing original release evidence alone does not block a nonduplicate running shoe whose manufacturer identity and included information are reliable. Never invent dates; display unverified release dates explicitly, with uncertain specs/prices blank. Age flags are advisory. The former 11 release holds have been published; the watch skips versions already in the catalog. Historical hold requirements above are superseded by this policy. ChatGPT verifies and prepares changes for Antonio’s explicit batch approval before publishing. Scheduled reviews must not publish; this Python checker itself stays read-only.

## Price and completeness review

Every run inventories missing prices, weight, drop, heel/forefoot stack, midsole, summary, toe-box and manufacturer support wording. It revisits primary manufacturer pages plus per-field completion source URLs on the same brand’s official domains, including regional and store pages. The report includes existing catalog values, price basis, contextual price/detail excerpts, fetch failures and follow-up research queries. Successful evidence is compared with the last successful snapshot; blocked/empty checks preserve that snapshot. First observations are review baselines, never automatic corrections.

ChatGPT’s Monday review researches avoidable gaps beyond these known URLs and verifies changed or stale values with manufacturer evidence. Price excerpts can refer to sales, related products, regions or colorways: distinguish US regular/list prices from current listed/store prices, preserve source/date and caveats, and never infer MSRP from a range or comparison price. Match gender, model generation, GTX/standard variant and reference size. Unchanged snippets do not establish accuracy. Unsupported fields remain blank; verified corrections require Antonio’s explicit batch approval before publishing. Scheduled reviews must not publish. Reports include missing-field totals so progress is measurable.
