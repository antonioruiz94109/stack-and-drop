# Stack & Drop

A free, static running-shoe directory and learning project. All 227 shoe versions have manufacturer source links and sourcing dates. The original eight entries have been checked and corrected against manufacturer pages. No automated catalog ingestion is implemented.

## Website

Live site: https://antonioruiz94109.github.io/stack-and-drop/

Open `index.html` through a local HTTP server. For example, run `python3 -m http.server 8000` and visit `http://localhost:8000`.

The application uses browser JavaScript, inline CSS, system fonts and `./shoes.json`. There are no runtime libraries, external scripts, analytics, signup services, images or build steps.

## GitHub Pages

Publish the reviewed `index.html`, `shoes.json` and `README.md` files. In repository Settings → Pages, choose **Deploy from a branch**, **main**, **/(root)**. The relative data URL supports a project subpath such as `/stack-and-drop/`.

Never upload the entire local folder. `.env`, credentials, backup files and local publisher configuration must stay private. The legacy Netlify publisher is separate from the Pages deployment.

## Catalog limitations

All 227 records carry manufacturer source URLs, sourcing dates, weight reference sizes where available, and field caveats. Price badges show List for verified manufacturer list prices, Price for manufacturer website or brand-store offers not confirmed as list prices, and Dealer for independent retailer prices. Original price basis, exact sources and qualifications remain in Sources & notes. Dealer badges retain the checked date. Both price sort directions place manufacturer prices first, dealer prices second and unknown prices last. Prices are not live offers. Missing specifications are null and displayed as a dash. Descriptions paraphrase manufacturers, not independent wear tests. Manufacturer data can still be incomplete or inconsistent: Torin 9 lists conflicting ounce/gram weights, and some stack heights and weight reference sizes are not supplied. These caveats are shown on the cards. Brand and product names belong to their respective owners; no affiliation is implied. No third-party visual assets or libraries are distributed. No open-source license has been selected for this project.

For future additions, record the manufacturer URL, sourcing date, reference size and field caveats before publishing. Manufacturer sourcing is not independent laboratory validation.

The Men’s / Women’s filter uses separately sourced versions: 111 men’s entries, 112 women’s entries and four unisex entries (227 total). Men’s and women’s versions count separately; colorways and widths do not. Reference sizes differ, so weights are not directly comparable.

The latest 50 additions cover 25 models with separate men's and women's entries, adding adidas and PUMA for ten brands total. The expansion preserved the preceding 84 entries. Across both expansion batches, 100 entries include manufacturer specification sources and separate linked model-release evidence within October 18, 2024–October 18, 2026. The original 34 have now been audited; see the results below.

Release dates can vary by market. Month-only evidence is retained at month precision. Sources include manufacturer announcements, launch coverage and released-status editorial calendars; linked evidence and caveats are displayed on cards. These are model releases, not new colorway dates. Some launch dates document regional availability.

New source conflicts are disclosed: women’s Endorphin Trainer weight has inconsistent units; women’s Mafate 5 differs between the product listing and launch announcement; women’s Speedgoat 7 repeats a men's weight without a reference size. Those uncertain weights are withheld. Other missing measurements remain blank.

Missing prices, stack heights, toe-box classifications and reference sizes are intentionally left blank. Specification sourcing is not laboratory verification. No automated ingestion is implemented.

## Manufacturer support wording

Cards show short, attributed excerpts from manufacturer model pages where verified, with a separate source link and check date. The linked model page may show a different gender, width or region. These are manufacturer descriptions, not standardized categories or gait recommendations. No gait or support filter is added. Unverified wording is explicitly labeled; no classification is inferred from shoe geometry, marketing names or reviews.

## Keyword search

Search updates as you type and combines with existing filters. It matches a case-insensitive literal phrase in brands, models, intended uses, toe-box descriptions, catalog summaries and quoted manufacturer support wording. Each result shows the matching field and highlights the matched text. Catalog descriptions and manufacturer quotes are labeled separately. It does not search source URLs or infer synonyms or fit suitability. Reset clears both search and filters.

## Release-date audit and replacements — October 19, 2026

The original 34-entry audit found 27 entries within the window, five older and two with uncertain cutoff eligibility. The seven flagged entries have now been replaced with verified 2025–2026 releases: Atmos 2, Fli-Lyte 6 and Ultrafly 6 (men); Pursuit 3 and Olympus 275 (men and women). The replacement window is October 19, 2024–October 19, 2026. The catalog remains 134 entries, 67 men and 67 women across ten brands. The other 127 entries are unchanged.

Every replacement has gender-specific manufacturer specifications and linked model-release evidence. Month/year precision and regional-launch caveats are preserved; a new color does not reset model age. Olympus 275 uses year precision because July general launch followed reported early exclusive availability. Altra does not supply its weight reference size.

Specifications come from manufacturer sources and have not been independently lab-tested by Stack & Drop. The release audit does not independently validate performance or specifications.

## Weekly review checker

A read-only weekly GitHub Actions checker monitors all ten catalog brands: Altra, ASICS, Brooks, HOKA, New Balance, Nike, PUMA, Saucony, Topo Athletic and adidas. Reports flag candidates, possible specification changes, aging releases and incomplete coverage. New entries and specification updates require review before publication. See [checker instructions](scripts/CHECKER.md) and [workflow reports](https://github.com/antonioruiz94109/stack-and-drop/actions/workflows/catalog-checker.yml).

## Reviewed running additions — October 19, 2026

Added 23 reviewed running entries (12 men, 11 women), bringing the catalog to 157 entries: 79 men and 78 women. Both gender versions of Traverse 2 and Trailventure 3 GTX remain held and were not added. Existing 134 records are unchanged. Both Vanish Tempo 2 prices are null; the women’s card discloses 200 g / 7.05 oz on the current manufacturer page versus 208 g in launch coverage. Release evidence retains year/month precision and regional caveats. No catalog changes are made by the weekly checker.

## Approved candidate additions — October 19, 2026

Added 41 reviewed entries: 17 men, 20 women and four unisex. The preceding 157 records are unchanged. Total: 198 entries across ten brands. Unisex records count once and appear under both men’s and women’s filters (100 and 102 results respectively). All 41 new prices remain null. Uncertain measurements, toe-box descriptions and unverified support wording remain unclassified. Additional manufacturer specification evidence is linked where it differs from the product page.

Release evidence falls within October 19, 2024–October 19, 2026: 31 additions have manufacturer-issued evidence and ten have specialist-retailer evidence, identified on cards. Month/year precision, regional timing and limited-release caveats are preserved. Conflicting Endorphin Pro 5 and Elite 3 measurements remain blank. The women’s Deviate NITRO 4 weight follows the gender-specific manufacturer announcement, with the conflicting product-page value disclosed. Held candidates and hiking entries were not published.

## Approved release-review additions — October 19, 2026

Added 14 cleared entries: six men’s and eight women’s. Current total: 212 entries (102 men’s, 106 women’s, four unisex) across ten brands. Unisex entries appear in both gender filters, giving 106 men’s and 110 women’s results. The preceding 198 records are unchanged. The other 11 release-review candidates remain on hold and are not published.

All 14 prices and uncertain specifications remain blank. Manufacturer product links and release evidence are included on every card. Release evidence comes from original launch reporting (eight entries) and specialist retailers (six entries), rather than manufacturer-issued launch announcements. Year-only Nike dates, regional Saucony GTX launch timing and conflicting women’s Echelon 11 release dates are disclosed. Release evidence falls within October 19, 2024–October 19, 2026.

## Flexible recency policy — October 19, 2026

Current total: 223 entries, comprising 108 men’s, 111 women’s and four unisex versions. Added the 11 previously held release-date entries after confirming manufacturer identity and checking duplicates. The user relaxed the strict two-year cutoff: recency remains a preference, not an exclusion rule. Missing or approximate original release dates alone no longer block otherwise reliable running-shoe entries. These 11 dates remain null and are visibly labeled not verified; no release date has been inferred from current availability. Unknown prices and measurements remain blank. Xodus Ultra 4 GTX panel measurements were withheld because the panel names the standard model. Echelon 10 uses a men’s Wide manufacturer source, without counting width separately. Earlier hold and strict-window statements describe historical reviews, superseded by this policy. Separate hiking, future-release and unresolved identity holds remain unchanged.

## Weekly workflow test — October 19, 2026

Current catalog: 227 entries (111 men, 112 women, four unisex). Re-reviewed four formerly age-excluded, nonduplicate running shoes under the flexible recency policy: Nike Alphafly 3 men/women, PUMA Deviate NITRO Elite 3 men, and Saucony Ride TR2 GTX men. Manufacturer specifications and original 2024 launch sources are linked; uncertain fields and prices remain blank. Corrected women’s Magnify NITRO 3 to road running; it was incorrectly included in the trail filter. Earlier totals and holds above are historical snapshots.

## Sharing a view

Search, gender, brand, drop, intended use, listed weight and sort are saved in URL query parameters (`q`, `gender`, `brand`, `drop`, `use`, `weight`, `sort`). Copy link shares the current view; if clipboard access is unavailable, a selectable link appears for manual copying. Reopening the link restores the controls and results. Browser Back and Forward restore previous selections; search edits are grouped after a short typing pause. Reset all removes the catalog parameters. Unsupported select values fall back to All; unrelated query parameters and URL fragments are preserved. Search text in a shared URL is visible to anyone receiving it.

On phones, a compact bar appears after the original results controls scroll above the screen. It shows the active filter count and matching shoe count. Filters opens and returns to the existing filter panel; Sort returns to and focuses the existing sort selector. The bar stays hidden on desktop and while the original controls are in view.
