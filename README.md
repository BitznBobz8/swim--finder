# Swim Finder AI — Version 1

An intelligent coarse fishing assistant that recommends swim location,
tackle setup and fish catch probabilities based on venue, species and
conditions. Built in Python with Kivy so it runs directly in Pydroid 3,
and is structured to convert cleanly to a standalone Android app with
Buildozer later.

## How to run in Pydroid 3

1. Copy the entire `swim_finder_ai` folder onto your device, keeping the
   folder structure exactly as-is (`main.py`, `swimfinder.kv`, `data/`,
   `logic/` must all stay together, in the same parent folder).
2. In Pydroid 3, open **Pip** and install `kivy` if it isn't already
   installed.
3. Open `main.py` inside that folder in Pydroid 3 and press **Run**.

## Folder structure

```
swim_finder_ai/
├── main.py                    # App entry point — screens, event wiring, results rendering
├── swimfinder.kv              # Kivy UI layout (widgets, colours, styling)
├── data/
│   ├── water_data.py          # Baseline depth/casting-distance/snag data per water type
│   ├── species_data.py        # Seasonal activity & feeding-zone data per species
│   └── tackle_data.py         # Baseline rod/reel/line/hook/bait setup per species
└── logic/
    ├── swim_analysis.py       # Works out depth, casting distance, feeding areas, snag risk, confidence
    ├── tackle_engine.py       # Turns species + swim analysis into a tackle recommendation
    ├── fish_predictor.py      # Estimates catch probability per species
    └── advice_generator.py    # Writes the plain-English advice paragraph
```

### What each file does

- **main.py** — Defines the `SwimFinderApp` Kivy App and two screens
  (`InputScreen`, `ResultsScreen`). Reads and validates the form fields,
  calls the four logic engines in order, and builds the results screen
  widgets dynamically (so the number of fish species / rows can change
  without touching the UI layout file).
- **swimfinder.kv** — All UI layout and styling in Kivy language: the
  form on the input screen, the card-based dark theme, buttons, spinners
  and text inputs. Kivy loads this automatically because its filename
  matches the App class name.
- **data/water_data.py** — Realistic baseline depth ranges, casting
  distance ranges and snag-risk levels for Lake / Canal / River /
  Reservoir.
- **data/species_data.py** — Which months each species is most active,
  which parts of the swim it favours (margins / shelf / open water /
  features), and whether it's wary of low pressure.
- **data/tackle_data.py** — Baseline rod, reel, line, hook, feeder/lead
  weight, bait, groundbait and loose feed for each of the 8 species.
- **logic/swim_analysis.py** — Combines water type + species + weather
  + wind + pressure into an estimated depth, casting distance, feeding
  areas, margin/shelf/open-water recommendation, snag risk and a
  confidence score. Results are seeded on GPS + conditions, so the same
  inputs always give the same analysis (not a different random answer
  each time you press the button).
- **logic/tackle_engine.py** — Takes the species baseline tackle and
  adjusts feeder/lead weight for casting distance, and chooses
  float-vs-feeder based on range and water type.
- **logic/fish_predictor.py** — Scores every species (not just the
  target) against season, weather, pressure, time of day and wind to
  produce a catch-probability percentage for each.
- **logic/advice_generator.py** — Builds the short "why / where to
  cast / how often to feed / what to change if weather shifts"
  paragraph from the other three engines' output.

## Notes on the Version 1 model

There's no live mapping, weather or historical-catch data yet — depth,
snag risk, and catch probabilities come from a rules-based model using
realistic UK coarse-fishing heuristics (season, water type, species
behaviour, weather, wind, pressure). This is intentional groundwork:
Version 2 adds live GPS/weather, Version 3 adds a catch log, and
Version 4 uses that catch log to make the predictions genuinely
learn from your own results.

## Roadmap (not yet built)

- **V2** — Auto-fetch GPS, weather, wind, pressure, sunrise/sunset.
- **V3** — SQLite catch log (venue, rig, bait, species, weight, notes, photos).
- **V4** — Use catch-log history to refine predictions per venue/conditions.
- **V5** — Maps, saved venues, offline mode, Excel export, catch charts,
  moon phase, solunar times, water temperature, rainfall history.

When you're ready, tell me which version to build next and I'll only
add/change the files needed for that feature — the rest of the project
stays untouched.
