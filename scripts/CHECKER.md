# Weekly catalog checker

Runs Mondays at 13:23 UTC (8:23 a.m. Chicago daylight time / 7:23 a.m. standard time), and manually from Actions → Weekly catalog review → Run workflow. Editing the checker also triggers a verification run.

Reports appear in the workflow run summary and downloadable `catalog-review` artifact (90-day retention). GitHub schedules may be delayed and public-repository schedules can be disabled after 60 days without repository activity.

The workflow has contents: read permission only. It does not update shoes.json, open changes, or publish catalog entries. A checksum verifies shoes.json is untouched. No external AI, purchases or personal credentials are required.

Scope: Altra and Topo new-arrival pages; New Balance men's/women's running listings; manufacturer URLs for all current entries from those brands. Listing coverage is not exhaustive. Blocked requests, empty extraction and missing pages appear as coverage problems; they never imply no changes or discontinued shoes. New Balance may reject automated requests with HTTP 403 and then needs manual review.

Candidates are unverified. URL-level normalization removes query strings and New Balance color/size identifiers; reviewers must still eliminate accessories, duplicate models, widths and colors, confirm gender, and establish release within the rolling two-year window. Discovery time is not release time.

Labelled specification excerpts are compared to a prior successful snapshot. These are possible source-text changes, not validated numerical corrections, and may include nearby or related-product wording. First-time snapshots show source evidence beside catalog values in report.json. Weight reference sizes and manufacturer claims need review. Prices are not monitored.

Snapshots are cached between runs; if GitHub evicts the cache, the checked-in initial baseline is used. report.json records the comparison date. A failed fetch preserves the last successful snapshot. Review the report before proposing any data change, then run catalog checks and approve publication separately.

Local run: `python3 scripts/check_catalog.py --catalog shoes.json --output checker-report`. Tests: `python3 -m unittest discover -s scripts -p 'test_check_catalog.py'`.
