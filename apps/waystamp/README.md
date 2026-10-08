# Waystamp

Collect an illustrated stamp for every heritage place, summit and trail you visit. Tap it, pick the date, and it gets inked into your book.

- **300 heritage places** across England, Scotland, Wales and Northern Ireland: houses, castles, gardens, abbeys, coast and countryside
- **526 summits**, including all 282 Munros and all 214 Wainwrights, each stamp showing its height
- **104 saunas** across Britain in a tab of their own, with hut, barrel, lakeside, seaside and floating sauna stamps
- **21 long-distance trails** (National Trails and Scotland's Great Trails), each stamp showing its length
- **Every stamp is a different original drawing**, with its own frame, ink and angle
- **Add your own** places, summits or trails, and pick a drawing for each so it gets a proper stamp
- **Sets:** ten built-in sets (Three Peaks, Castles of Edward I, Great abbeys and more) plus sets you make yourself
- **Milestone badges** for stamp counts, metres climbed, miles walked, variety and completed sets
- **Your year:** a year in review with totals, a month-by-month chart and highlights, which you can save as an image to share
- **Cover colours:** six colours for your book's cover
- **Map** of everything you've stamped and everything still to go, which works offline
- **Journal:** every stamp and visit in date order, with your notes
- **Repeat visits:** log every time you go back, not just the first
- **Near me:** sorts places, summits, trails or saunas by distance from where you are
- **A stamp thud and buzz** when you stamp (can be turned off), a welcome guide, and Undo
- **Works offline** once opened, so it is fine on a hill with no signal
- **Installs like an app** from the browser, with its own home-screen icon
- **Private:** stamps stay on your device. No accounts, no server, no tracking
- **Backup and restore** as a small JSON file, e.g. when changing phone

Waystamp is an independent, open-source project. It is not affiliated with or endorsed by the National Trust, English Heritage, Cadw, Historic Environment Scotland or any other organisation whose places appear in it. Place names are used only to identify the places. All stamp artwork is original.

## Installing on a phone

- **iPhone / iPad:** open the link in Safari, tap Share, then **Add to Home Screen**.
- **Android:** open the link in Chrome and tap **Install app** at the bottom of the page, or use the ⋮ menu → **Install app**.

## How it is built

Plain static files with no build step and no dependencies:

| File | What it does |
| --- | --- |
| `index.html` | The whole app: place, summit and trail lists, stamp drawings (generated SVG), storage, backup |
| `manifest.webmanifest` | Name, colours and icons for installing |
| `sw.js` | Service worker that caches the app and fonts for offline use |
| `icons/` | App icons |

Stamps live in the browser's `localStorage` under the key `heritage-passport-v1` (kept from the first version so existing stamps carry over).

## Hosting

Serve the folder from any static host. All paths are relative, so it also works from a subfolder such as `/waystamp/`. Keep the trailing slash in links to it.

- **Cloudflare Workers with static assets:** put the files in a folder inside the site's assets directory, then `npx wrangler deploy`.
- **Cloudflare Pages / Netlify / GitHub Pages:** deploy the repo root as-is.

Linking straight to a tab works with `#summits` or `#trails`.

## Releasing an update

1. Edit the files.
2. Change `VERSION` at the top of `sw.js` (e.g. `waystamp-v3`), so installed copies pick up the new version.
3. Deploy. Phones get the update the next time the app is opened.

## Adding to the built-in lists

All lists are near the top of the script in `index.html`:

- **Places** (`RAW`): `Name~Short label|type|motif options`
- **Summits** (`SUMMITS`): `Name~Short label|height in metres|summit s=shape` where shape is `pyr`, `flat`, `twin`, `whale`, `cone`, `crag`, `dome` or `tor`
- **Trails** (`TRAILS`): `Name~Short label|miles|km|trail v=scene` where scene is `coast`, `downs`, `ridge`, `moor`, `wall`, `river` or `glen`

The short label is optional and is used on the stamp when the full name is long.

## Data

Munro and Wainwright names, heights and positions come from the [Database of British and Irish Hills](https://www.hill-bagging.co.uk/) (v17.4, CC BY 4.0). The map outline is from [Natural Earth](https://www.naturalearthdata.com/) (public domain). Positions of heritage places and trails are approximate.

## License

MIT
