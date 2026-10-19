# CadenceIndex

A free, static running-shoe directory and learning project. All 134 shoe versions have manufacturer source links and sourcing dates. The original eight entries have been checked and corrected against manufacturer pages. No automated catalog ingestion is implemented.

## Website

Open `index.html` through a local HTTP server. For example, run `python3 -m http.server 8000` and visit `http://localhost:8000`.

The application uses browser JavaScript, inline CSS, system fonts and `./shoes.json`. There are no runtime libraries, external scripts, analytics, signup services, images or build steps.

## GitHub Pages

Publish the reviewed `index.html`, `shoes.json` and `README.md` files. In repository Settings → Pages, choose **Deploy from a branch**, **main**, **/(root)**. The relative data URL supports a project subpath such as `/CadenceIndex/`.

Never upload the entire local folder. `.env`, credentials, backup files and local publisher configuration must stay private. The legacy Netlify publisher is separate from the Pages deployment.

## Catalog limitations

All 134 records carry manufacturer source URLs, sourcing dates, weight reference sizes where available, and field caveats. Their prices are US list prices rather than live offers. Missing specifications are null and displayed as a dash. Descriptions paraphrase manufacturers, not independent wear tests. Manufacturer data can still be incomplete or inconsistent: Torin 9 lists conflicting ounce/gram weights, and some stack heights and weight reference sizes are not supplied. These caveats are shown on the cards. Brand and product names belong to their respective owners; no affiliation is implied. No third-party visual assets or libraries are distributed. No open-source license has been selected for this project.

For future additions, record the manufacturer URL, sourcing date, reference size and field caveats before publishing. Manufacturer sourcing is not independent laboratory validation.

The Men’s / Women’s filter uses separately sourced versions: 67 men’s entries and 67 women’s entries (134 total). Men’s and women’s versions count separately; colorways and widths do not. Reference sizes differ, so weights are not directly comparable.

The latest 50 additions cover 25 models with separate men's and women's entries, adding adidas and PUMA for ten brands total. The expansion preserved the preceding 84 entries. Across both expansion batches, 100 entries include manufacturer specification sources and separate linked model-release evidence within October 18, 2024–October 18, 2026. The original 34 have now been audited; see the results below.

Release dates can vary by market. Month-only evidence is retained at month precision. Sources include manufacturer announcements, launch coverage and released-status editorial calendars; linked evidence and caveats are displayed on cards. These are model releases, not new colorway dates. Some launch dates document regional availability.

New source conflicts are disclosed: women’s Endorphin Trainer weight has inconsistent units; women’s Mafate 5 differs between the product listing and launch announcement; women’s Speedgoat 7 repeats a men's weight without a reference size. Those uncertain weights are withheld. Other missing measurements remain blank.

Missing prices, stack heights, toe-box classifications and reference sizes are intentionally left blank. Specification sourcing is not laboratory verification. No automated ingestion is implemented.

## Manufacturer support wording

Cards show short, attributed excerpts from manufacturer model pages where verified, with a separate source link and check date. The linked model page may show a different gender, width or region. These are manufacturer descriptions, not standardized categories or gait recommendations. No gait or support filter is added. Unverified wording is explicitly labeled; no classification is inferred from shoe geometry, marketing names or reviews.

## Keyword search

Search updates as you type and combines with existing filters. It matches a case-insensitive literal phrase in brands, models, intended uses, toe-box descriptions, catalog summaries and quoted manufacturer support wording. Each result shows the matching field and highlights the matched text. Catalog descriptions and manufacturer quotes are labeled separately. It does not search source URLs or infer synonyms or fit suitability. Reset clears both search and filters.

## Original 34 release-date audit — October 19, 2026

Audited against the original October 18, 2024–October 18, 2026 window: 27 entries within the window, five older, two uncertain around the cutoff. All 134 entries are retained; older and uncertain entries are visibly labeled. Older models: Olympus 6 (one entry), Escalante 4 (two), Specter 2 (one), Atmos (one). Ultraventure 4 (two) is documented as available by October 30, 2024, but first-sale timing relative to October 18 remains unresolved. Model launches are distinct from later colorways and regional releases. Month/year precision and source caveats are preserved. Release dates apply at model level to gender variants unless noted.

Specifications come from manufacturer sources and have not been independently lab-tested by CadenceIndex. The release audit does not independently validate performance or specifications.
