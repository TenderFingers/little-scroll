# Little Scroll

A photo scroller for toddlers. Parents pick family photos; the child sees them one at a time in an endless shuffled scroll. Photos and recordings stay on the phone.

## What is where

- `source/little-scroll.html` is the app. All the code lives in this one file. Edit this one.
- `source/build_dist.py` builds the four files GitHub Pages serves from the main folder: `index.html`, `sw.js`, `manifest.webmanifest`, `icon.png`. Do not edit `index.html` by hand; the next build replaces it.

## Updating the app

1. Edit `source/little-scroll.html` and change `VERSION` near the top of the script.
2. Run `python3 source/build_dist.py`.
3. Commit and push. GitHub Pages republishes in a minute or two.
4. Open the app from the Home Screen icon while online, close it fully, and open it again. The menu shows the version number.
