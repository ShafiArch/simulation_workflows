# Simulation Workflows

Daylight and wind simulation workflows for handloom worker housing in Tangail, Bangladesh,
by Shafiul Islam. One page: https://shafiarch.github.io/simulation_workflows/

## Publish

Settings, Pages, Build and deployment: Deploy from a branch, `main`, folder `/ (root)`.
No build step; `.nojekyll` makes GitHub serve the files as they are.

## What is where

| What | Where |
| --- | --- |
| The page | `index.html`, `assets/style.css`, `assets/site.js` |
| Pictures the page shows (small, and `-l` for the click to enlarge) | `img/` |
| Original exports, never changed | `Handloom/`, `Handloom Script Final.jpg` |
| The script that makes `img/` from the originals | `tools/build_img.py` |

## The page

1. **Daylight** (Radiance, ClimateStudio in Grasshopper, HDRscope, TT Toolbox and Design
   Explorer, Octopus). Existing room at noon on the 21st of March, June, September and December:
   illuminance, false colour luminance, histogram, and the Reinhart and Ward tone mapped views,
   one column per month. Annual metrics (UDI, sDA, ASE, average lux) existing against
   optimized, in the same columns, then the multi-objective search (Pareto front, Design Explorer).
2. **Wind.** Butterfly CFD, six iterations of window size, location and spacing, vectors and
   pressure side by side, the full Grasshopper definition and the steps as pseudo code.
3. **Thermal.** An empty section waiting for the thermal study.

December's illuminance (mean about 740, median about 560 lux) is a draft read from the colours
of the map against the 100 to 3000 lux scale, marked "draft" on the page; the same reading
gives March, June and September medians within 2% of the presentation. Replace it in
`index.html` with the simulated value.

Sequences (the assembly, the four months, existing and optimized, the six wind iterations)
play by themselves while on screen and stop when a step is clicked; they use the same small
pictures as the comparison grids, so they cost nothing extra to load. They always run by
default. The assembly builds up layer by layer with a slow fade (`data-build`, `--fade` on the
player in `index.html`); the others cross fade. One accent colour, orange red, for the whole page.

## Adding the thermal study

Export the pictures into a new folder such as `Handloom/Thermal/`, make web copies in
`tools/build_img.py` the same way as the others (one crop box for every image in a series, so
they line up), run `python3 tools/build_img.py` (needs `pip install pillow python-pptx`), and
replace the empty `.placeholder` in the Thermal section of `index.html` with a `.cmp` grid like
the wind one. Whenever `assets/style.css` or `assets/site.js` changes, raise `?v=N` on both tags
in `index.html`.

## Themes

Trace (default), Night and Clay, the same as the works site and Fabrication Works, remembered
under the same key (`site-theme`), so a visitor's choice carries across the sites. The page is
one plain canvas, with no cards: pictures exported on white paper (wind, dashboards, charts,
legends, the script sheet) are made transparent by `tools/build_img.py`, greys and lines
turning into ink. Each comes twice, `name.webp` with dark ink for Trace and Clay and
`name-n.webp` with light ink for Night; the page swaps them with the classes `v-light` and `v-dark`.

## Rules

- No em dashes or en dashes in text, code comments or docs; commas, semicolons, parentheses
  or periods instead.
- Commits are authored and committed as Shafiul Islam
  (`145989139+ShafiArch@users.noreply.github.com`), with no co-author lines.
