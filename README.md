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
├── main.py                    # App entry point — screens, event wiring, results rendering, GPS/weather flow
├── swimfinder.kv              # Kivy UI layout (widgets, colours, styling)
├── data/
│   ├── water_data.py          # Baseline depth/casting-distance/snag data per water type
│   ├── species_data.py        # Seasonal activity & feeding-zone data per species
│   ├── tackle_data.py         # Baseline rod/reel/line/hook/bait setup per species
│   └── weather_codes.py       # Maps Open-Meteo weather/wind codes to the app's spinner text
└── logic/
    ├── swim_analysis.py       # Works out depth, casting distance, feeding areas, snag risk, confidence
    ├── tackle_engine.py       # Turns species + swim analysis into a tackle recommendation
    ├── fish_predictor.py      # Estimates catch probability per species
    ├── advice_generator.py    # Writes the plain-English advice paragraph
    └── weather_service.py     # Fetches current weather/wind/pressure/sunrise/sunset (V2)
```

### What each file does

- **main.py** — Defines the `SwimFinderApp` Kivy App and two screens
  (`InputScreen`, `ResultsScreen`). Reads and validates the form fields,
  calls the four logic engines in order, and builds the results screen
  widgets dynamically (so the number of fish species / rows can change
  without touching the UI layout file). Also owns the V2 GPS + weather
  auto-fetch flow: requesting location permission, starting/stopping
  GPS, and running the weather API call on a background thread so the
  UI never freezes.
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
- **data/weather_codes.py** — Converts Open-Meteo's raw weather codes
  and wind bearing (degrees) into the same plain-English options
  already used by the Weather and Wind Direction spinners.
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
- **logic/weather_service.py** — Calls the free Open-Meteo API (no key
  needed) for a given GPS fix and returns current weather, wind
  direction/speed, pressure, and today's sunrise/sunset, already
  converted into the app's field formats.

## Version 2 — auto GPS + weather

Tap **"Use My Location & Weather"** on the input screen and the app
will:
1. Ask for location permission (compiled APK only — see note below).
2. Get a GPS fix and fill in Latitude/Longitude.
3. Fetch current weather, wind direction/speed and pressure for that
   location from Open-Meteo and fill those fields in too.
4. Show today's sunrise/sunset time under the button.

You can still edit any auto-filled field by hand afterwards before
pressing Analyse Swim.

**Running this in Pydroid 3:** install `plyer` via Pydroid's Pip
screen (`pip install plyer`). Pydroid 3 itself is the app requesting
location access on Android — there's no in-app permission popup like
in the compiled APK, so you'll need to grant Location to the **Pydroid
3** app once via Android Settings → Apps → Pydroid 3 → Permissions.

**Running this as the compiled APK:** no setup needed — `plyer` is
already bundled in via `buildozer.spec`, and the app will show
Android's normal "Allow Swim Finder AI to access this device's
location?" prompt the first time you tap the button.

Either way, GPS needs a real fix to work — it may take a few seconds
outdoors, and can time out (after 20 seconds) or fail indoors/without
a clear sky view. You can always fall back to typing the coordinates
in manually.



## Notes on the Version 1 model

There's no live mapping, weather or historical-catch data yet — depth,
snag risk, and catch probabilities come from a rules-based model using
realistic UK coarse-fishing heuristics (season, water type, species
behaviour, weather, wind, pressure). This is intentional groundwork:
Version 2 adds live GPS/weather, Version 3 adds a catch log, and
Version 4 uses that catch log to make the predictions genuinely
learn from your own results.

## Roadmap (not yet built)

- ~~**V2** — Auto-fetch GPS, weather, wind, pressure, sunrise/sunset.~~ ✅ Done
- **V3** — SQLite catch log (venue, rig, bait, species, weight, notes, photos).
- **V4** — Use catch-log history to refine predictions per venue/conditions.
- **V5** — Maps, saved venues, offline mode, Excel export, catch charts,
  moon phase, solunar times, water temperature, rainfall history.

When you're ready, tell me which version to build next and I'll only
add/change the files needed for that feature — the rest of the project
stays untouched.
