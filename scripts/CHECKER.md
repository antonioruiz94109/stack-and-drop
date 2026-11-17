# Weekly catalog checker

Runs Mondays at 13:23 UTC (8:23 a.m. Chicago daylight time / 7:23 a.m. standard time), and manually from Actions → Weekly catalog review → Run workflow. Editing the checker also triggers a verification run.

Reports appear in the workflow run summary and downloadable `catalog-review` artifact (90-day retention). GitHub schedules may be delayed and public-repository schedules can be disabled after 60 days without repository activity.

The workflow has contents: read permission only. It does not update shoes.json, open changes, or publish catalog entries. A checksum verifies shoes.json is untouched. No external AI, purchases or personal credentials are required.

Scope: all ten current catalog brands—Altra, ASICS, Brooks, HOKA, New Balance, Nike, PUMA, Saucony, Topo Athletic and adidas. Checks selected men's/women's manufacturer listings and source URLs for all catalog entries. Per-brand report coverage distinguishes fetched pages from extracted specifications. Listing coverage is not exhaustive. Blocked requests, empty extraction and missing pages appear as coverage problems; they never imply no changes or discontinued shoes. New Balance may reject automated requests with HTTP 403 and then needs manual review.

Candidates are unverified. URL-level normalization removes query strings and New Balance color/size identifiers; reviewers must still eliminate accessories, duplicate models, widths and colors, confirm gender, and verify a manufacturer release date or official launch announcement before proposing an addition. Recency within two years is preferred, not required. Discovery time is not release time.

Labelled specification excerpts are compared to a prior successful snapshot. These are possible source-text changes, not validated numerical corrections, and may include nearby or related-product wording. First-time snapshots show source evidence beside catalog values in report.json. Weight reference sizes and manufacturer claims need review. Prices and missing details are monitored as described below.

Snapshots are cached between runs; if GitHub evicts the cache, the checked-in initial baseline is used. report.json records the comparison date. A failed fetch preserves the last successful snapshot. Review the report before proposing any data change, then run catalog checks. Prepare verified changes for Antonio’s explicit batch approval before publishing. Scheduled reviews must not publish.

Local run: `python3 scripts/check_catalog.py --catalog shoes.json --output checker-report`. Tests: `python3 -m unittest discover -s scripts -p 'test_check_catalog.py'`.

The all-brand trial on October 19 fetched 88/157 source pages locally. New Balance, ASICS, Brooks, HOKA and adidas returned access blocks; monitoring remains enabled to retry weekly, but these brands require manual research while blocked. Candidate counts refer to links, not verified distinct shoes. Brand coverage on GitHub runners may differ. No blocked-access bypass is attempted.

## Held release evidence

The 11 unresolved entries are tracked in release-holds.json. Each Monday the checker revisits their manufacturer pages and known supporting sources, captures nearby exact-model wording, and flags initial evidence, changes or unavailable pages in a separate report section. Prior successful evidence is retained on fetch failures. Published model/gender versions are skipped. This is a known-source watch, not an exhaustive web search; report.json also supplies follow-up search queries for the reviewer. New dates may describe reviews, restocks, colorways or other variants and never clear a hold automatically. Verify the exact model/version and regional context before publication; missing release-date evidence blocks new additions; existing entries with unknown dates are not automatically removed.

## Current publication policy

October 26, 2026 rules supersede earlier addition policies:
- New entries require a verified manufacturer release date or official launch announcement, with region and date precision. A page publication/review date is not a release date. Hold additions lacking this evidence; do not automatically remove existing unknown-date entries.
- Recency within two years remains preferred, not mandatory. Never invent dates or measurements.
- Compare exact model family, generation, gender and variant against the catalog. Prefer the newest verified version; add the verified successor before removing its predecessor. Do not replace GTX with standard versions. Verify each gender independently; unisex counts once and appears in both gender filters. Widths/colors are not separate entries.
- Road and trail running shoes only; exclude track/XC spikes, hiking-only and lifestyle shoes.
- Append explicitly published manufacturer cushion-level wording with its source; foam names are not cushion levels. Preserve exact manufacturer support wording in a consistent quoted field, without converting it to a standardized gait class.
- Prefer manufacturer US store prices. Manufacturer-hosted US dealer listings qualify only after own-store absence is established; blocked access is not absence. Keep exact price source and checked date. Label dealer prices “Dealer price, checked [date]”; sort after manufacturer prices in both directions, unknowns last.
- Never use Brooks ReStart or other resale/used/refurbished/pre-owned sources for prices. Replace adidas announcement price sources with exact verified adidas.com US product pages when available; retain launch evidence separately and preserve caveats when no replacement is verified.
- Qwen is the designated primary maintainer; Hermes orchestrates handoffs; ChatGPT independently reviews actual proposals. Their operational activation is gated by SUSTAINING.md. Antonio must explicitly approve each material/catalog publication batch. Scheduled reviews and this Python checker must not publish.

## Price and completeness review

Every run inventories missing prices, weight, drop, heel/forefoot stack, midsole, summary, toe-box and manufacturer support wording. It revisits primary manufacturer pages plus per-field completion source URLs on the same brand’s official domains, including regional and store pages. The report includes existing catalog values, price basis, contextual price/detail excerpts, fetch failures and follow-up research queries. Successful evidence is compared with the last successful snapshot; blocked/empty checks preserve that snapshot. First observations are review baselines, never automatic corrections.

The maintainer’s Monday review researches avoidable gaps beyond these known URLs and verifies changed or stale values with manufacturer evidence. Price excerpts can refer to sales, related products, regions or colorways: distinguish US regular/list prices from current listed/store prices, preserve source/date and caveats, and never infer MSRP from a range or comparison price. Match gender, model generation, GTX/standard variant and reference size. Unchanged snippets do not establish accuracy. Unsupported fields remain blank; verified corrections require Antonio’s explicit batch approval before publishing. Scheduled reviews must not publish. Reports include missing-field totals so progress is measurable.

## Coverage quality gate (November 2026)

Each report prominently states complete/incomplete coverage and shows per-brand fetched, extracted and discovery counts. After retaining the report and preserving successful comparison evidence, Actions deliberately fails its final coverage gate when sources or labelled specifications are unavailable. This is not a scraper crash, nor a claim that the catalog has no changes. Read the report's exact failures. The local CLI still exits successfully after producing its report; consult `coverage_status` for coverage quality.

ASICS corporate press and adidas Running news are supplemental official announcement leads, separately labelled and not counted as repaired product coverage. They may include non-shoe announcements and do not prove model, gender, release date or specifications. Nike embedded product details are read without executing JavaScript, restricted to the matching product route and exact SKU when supplied; recommendations and other colors are not substitutes. Missing source measurements remain missing. Access blocks and oversized pages remain explicit; no access-control bypass is attempted. Catalog publication still requires separately verified changes.
