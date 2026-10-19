# CadenceIndex

A free, static running-shoe directory and learning project. The catalog contains 17 shoes: nine with manufacturer sources (three each from Altra, Topo Athletic and Nike), plus eight original AI-assisted entries awaiting source verification. No automated catalog ingestion is implemented.

## Website

Open `index.html` through a local HTTP server. For example, run `python3 -m http.server 8000` and visit `http://localhost:8000`.

The application uses browser JavaScript, inline CSS, system fonts and `./shoes.json`. There are no runtime libraries, external scripts, analytics, signup services, images or build steps.

## GitHub Pages

Publish the reviewed `index.html`, `shoes.json` and `.nojekyll` files. In repository Settings → Pages, choose **Deploy from a branch**, **main**, **/(root)**. The relative data URL supports a project subpath such as `/CadenceIndex/`.

Never upload the entire local folder. `.env`, credentials, backup files and local publisher configuration must stay private. The legacy Netlify publisher is separate from the Pages deployment.

## Catalog limitations

Nine records carry manufacturer source URLs, sourcing dates, weight reference sizes where available, and field caveats. Their prices are US list prices rather than live offers. Missing specifications are null and displayed as a dash. Descriptions paraphrase manufacturers, not independent wear tests. The eight original records remain provisional and are labeled individually. Brand and product names belong to their respective owners; no affiliation is implied. No third-party visual assets or libraries are distributed. No open-source license has been selected for this project.

The smallest next catalog improvement is to verify one existing shoe against its manufacturer page, record the source URL, reference size and verification date, and reuse that process before expanding the catalog.
