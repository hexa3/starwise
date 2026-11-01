# Starwise

A live sky map of all 5,070 naked-eye stars that tells you **where** every star is and **why** it's there.

**Live:** https://hexa3.github.io/starwise/

Click any star to get:

- **Where to look right now:** compass direction, altitude (in fists at arm's length), and rise, highest-point and set times for your location.
- **Why it's there:** its fixed spot on the sky, Earth's spin, your latitude, the season, and slow drift from precession and the star's own motion.
- **Why it looks like it does:** distance, when its light left it, luminosity compared with the Sun, temperature and spectral type.
- **3D view:** see a constellation from Earth, then turn sideways to see how far apart its stars really are.
- **Deep time:** scrub ±60,000 years to watch the pole star change and constellations deform.

It's a single self-contained `index.html` with no build step.

## Data

- Stars: [HYG Database v3.8](https://github.com/astronexus/HYG-Database) (Hipparcos, Yale Bright Star, Gliese), CC BY-SA 4.0
- Constellation figures: [d3-celestial](https://github.com/ofrohn/d3-celestial), BSD-3-Clause

`prep.py` is the script that built the embedded catalog.
