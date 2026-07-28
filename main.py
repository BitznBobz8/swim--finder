"""
main.py
----------
Entry point for Swim Finder AI. Defines the Kivy App and the two Screens (Input / Results),
reads the form values, calls the analysis engines in logic/, and renders the results dynamically
onto the results screen.

HOW TO RUN IN PYDROID 3:
1. Copy the whole "swim_finder_ai" folder onto your device (keep the folder structure
   exactly as-is - main.py, swimfinder.kv, data/, logic/ must all stay together).
2. Make sure the "kivy" package is installed in Pydroid 3.
3. Open main.py in Pydroid 3 and press Run.
"""

import os
import threading
import certifi

# ---------------------------------------------------------------------------
# SSL & Map Network Configuration
# ---------------------------------------------------------------------------
# Point OpenSSL / urllib to certifi's bundle so Android can make HTTPS calls
os.environ['SSL_CERT_FILE'] = certifi.where()

try:
    from kivy_garden.mapview import MapSource
    # Set custom User-Agent to comply with OpenStreetMap tile server policies
    MapSource.user_agent = "SwimFinderAI/1.0 (Android)"
except ImportError:
    pass

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

from logic.swim_analysis import analyse_swim as run_swim_analysis
from logic.tackle_engine import recommend_tackle
from logic.fish_predictor import predict_species
from logic.advice_generator import generate_advice
from logic.weather_service import fetch_weather

MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
]


class InputScreen(Screen):
    """The form where the angler enters swim/location/condition details."""
    pass


class ResultsScreen(Screen):
    """Displays the Swim Analysis, Tackle Recommendation, Fish Prediction and Fishing Advice results."""
    pass


class SwimFinderApp(App):

    def build(self):
        self.title = "Swim Finder AI"
        Window.clearcolor = (0.07, 0.09, 0.11, 1)

        self.sm = ScreenManager()
        self.input_screen = InputScreen(name='input')
        self.results_screen = ResultsScreen(name='results')

        self.sm.add_widget(self.input_screen)
        self.sm.add_widget(self.results_screen)

        self._gps_fix_received = False
        return self.sm

    # ------------------------------------------------------------------
    # Input handling
    # ------------------------------------------------------------------
    def _read_inputs(self):
        """Reads and validates all form fields from the input screen."""
        ids = self.input_screen.ids
        error = None

        def to_float(text_input, default=None, field_name=""):
            nonlocal error
            text = text_input.text.strip()
            if not text:
                if default is not None:
                    return default
                error = f"Please enter a value for {field_name}."
                return None
            try:
                return float(text)
            except ValueError:
                error = f"Please enter a valid number for {field_name}."
                return None

        lat = to_float(ids.lat_input, field_name="GPS Latitude")
        lon = to_float(ids.lon_input, field_name="GPS Longitude")
        wind_speed = to_float(ids.wind_speed_input, default=0.0)
        pressure = to_float(ids.pressure_input, default=1013.0)

        month_name = ids.month_spinner.text

        inputs = {
            "lat": lat,
            "lon": lon,
            "water_type": ids.water_type_spinner.text,
            "species": ids.species_spinner.text,
            "time_of_day": ids.time_spinner.text,
            "month": month_name,
            "month_num": MONTHS.index(month_name) + 1,
            "weather": ids.weather_spinner.text,
            "wind_dir": ids.wind_dir_spinner.text,
            "wind_speed_mph": wind_speed,
            "pressure_hpa": pressure,
        }
        return inputs, error

    # ------------------------------------------------------------------
    # Button actions (called from swimfinder.kv)
    # ------------------------------------------------------------------
    def analyse_swim(self):
        inputs, error = self._read_inputs()
        error_label = self.input_screen.ids.error_label
        if error:
            error_label.text = error
            return
        error_label.text = ''

        swim = run_swim_analysis(inputs)
        tackle = recommend_tackle(inputs, swim)
        predictions = predict_species(inputs)
        advice = generate_advice(inputs, swim, tackle, predictions)

        self._render_results(inputs, swim, tackle, predictions, advice)
        self.sm.current = 'results'

    def go_back(self):
        self.sm.current = 'input'

    def open_maps_at_location(self):
        """Centers the embedded MapView on the user-entered coordinates."""
        inputs, error = self._read_inputs()
        if error or inputs['lat'] is None or inputs['lon'] is None:
            self.input_screen.ids.error_label.text = "Enter valid latitude and longitude first"
            return

        lat = inputs['lat']
        lon = inputs['lon']

        ids = self.input_screen.ids
        if hasattr(ids, 'map_view'):
            ids.map_view.center_on(lat, lon)
            ids.map_view.zoom = 14

        self.input_screen.ids.error_label.text = ""

    # ------------------------------------------------------------------
    # Auto-fetch GPS location + current weather/wind/pressure
    # ------------------------------------------------------------------
    def fetch_location_and_weather(self):
        self._gps_fix_received = False
        self.input_screen.ids.location_status.text = "Requesting location permission..."
        self._request_android_permissions(self._on_permissions_result)

    def _request_android_permissions(self, callback):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions(
                [Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_COARSE_LOCATION],
                callback,
            )
        except ImportError:
            # Fallback for desktop testing environments
            callback([], [True, True])

    def _on_permissions_result(self, permissions, grant_results):
        if grant_results and not all(grant_results):
            Clock.schedule_once(
                lambda dt: self._show_location_error(
                    "Location permission was denied. Enable it in Android Settings to use this feature."
                ),
                0,
            )
            return
        Clock.schedule_once(lambda dt: self._start_gps(), 0)

    def _start_gps(self):
        self.input_screen.ids.location_status.text = "Getting GPS location..."
        try:
            from plyer import gps
            gps.configure(
                on_location=self._on_gps_location,
                on_status=self._on_gps_status,
            )
            gps.start(minTime=1000, minDistance=0)
            Clock.schedule_once(self._gps_timeout, 25)
        except NotImplementedError:
            self._show_location_error("GPS is not available on this device.")
        except Exception as exc:
            self._show_location_error(f"Could not start GPS: {exc}")

    def _on_gps_location(self, **kwargs):
        lat = kwargs.get('lat')
        lon = kwargs.get('lon')
        Clock.schedule_once(lambda dt: self._handle_gps_fix(lat, lon), 0)

    def _on_gps_status(self, **kwargs):
        pass

    def _handle_gps_fix(self, lat, lon):
        if self._gps_fix_received or lat is None or lon is None:
            return
        self._gps_fix_received = True
        self._stop_gps()

        ids = self.input_screen.ids
        ids.lat_input.text = f"{lat:.5f}"
        ids.lon_input.text = f"{lon:.5f}"

        # Center MapView on GPS location
        if hasattr(ids, 'map_view'):
            ids.map_view.center_on(lat, lon)
            ids.map_view.zoom = 14

        ids.location_status.text = "Location found. Fetching weather..."
        threading.Thread(target=self._weather_worker, args=(lat, lon), daemon=True).start()

    def _gps_timeout(self, dt):
        if not self._gps_fix_received:
            self._stop_gps()
            self._show_location_error("GPS search timed out - check device Location setting.")

    def _stop_gps(self):
        try:
            from plyer import gps
            gps.stop()
        except Exception:
            pass

    def _weather_worker(self, lat, lon):
        try:
            weather = fetch_weather(lat, lon)
            Clock.schedule_once(lambda dt: self._on_weather_fetched(weather), 0)
        except Exception as exc:
            Clock.schedule_once(lambda dt: self._show_location_error(f"Weather fetch failed: {exc}"), 0)

    def _on_weather_fetched(self, weather):
        ids = self.input_screen.ids
        ids.weather_spinner.text = weather["weather"]
        ids.wind_dir_spinner.text = weather["wind_dir"]

        if weather["wind_speed_mph"] is not None:
            ids.wind_speed_input.text = str(weather["wind_speed_mph"])
        if weather["pressure_hpa"] is not None:
            ids.pressure_input.text = str(weather["pressure_hpa"])

        ids.location_status.text = (
            f"Updated. Sunrise {weather['sunrise']} · Sunset {weather['sunset']}"
        )

    def _show_location_error(self, message):
        self.input_screen.ids.location_status.text = message

    def on_stop(self):
        self._stop_gps()

    # ------------------------------------------------------------------
    # Results rendering helpers
    # ------------------------------------------------------------------
    def _style_card(self, widget):
        with widget.canvas.before:
            Color(0.13, 0.16, 0.19, 1)
            rect = RoundedRectangle(pos=widget.pos, size=widget.size, radius=[12])
            widget.bind(pos=lambda inst, val: setattr(rect, 'pos', val))
            widget.bind(size=lambda inst, val: setattr(rect, 'size', val))

    def _make_card(self, title_text, rows):
        card = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(4), size_hint_y=None)
        card.bind(minimum_height=card.setter('height'))
        self._style_card(card)

        title = Label(
            text=title_text,
            bold=True,
            font_size='16sp',
            color=(0.3, 0.85, 0.65, 1),
            size_hint_y=None,
            height=dp(26),
            halign='left',
            valign='middle',
        )
        title.bind(size=title.setter('text_size'))
        card.add_widget(title)

        for label_text, value_text in rows:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(24), spacing=dp(8))
            label_widget = Label(
                text=str(label_text),
                color=(0.7, 0.78, 0.78, 1),
                font_size='13sp',
                halign='left',
                valign='middle',
                size_hint_x=0.45,
            )
            label_widget.bind(size=label_widget.setter('text_size'))

            value_widget = Label(
                text=str(value_text),
                color=(0.95, 0.95, 0.95, 1),
                font_size='13sp',
                halign='left',
                valign='middle',
                size_hint_x=0.55,
            )
            value_widget.bind(size=value_widget.setter('text_size'))

            row.add_widget(label_widget)
            row.add_widget(value_widget)
            card.add_widget(row)

        return card

    def _make_advice_card(self, advice_text):
        card = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(6), size_hint_y=None)
        card.bind(minimum_height=card.setter('height'))
        self._style_card(card)

        title = Label(
            text="Fishing Advice",
            bold=True,
            font_size='16sp',
            color=(0.3, 0.85, 0.65, 1),
            size_hint_y=None,
            height=dp(26),
            halign='left',
            valign='middle',
        )
        title.bind(size=title.setter('text_size'))
        card.add_widget(title)

        body = Label(
            text=advice_text,
            color=(0.9, 0.92, 0.92, 1),
            size_hint_y=None,
            halign='left',
            valign='top',
            font_size='13sp',
        )
        body.bind(width=lambda inst, w: setattr(inst, 'text_size', (w, None)))
        body.bind(texture_size=lambda inst, ts: setattr(inst, 'height', ts[1]))
        card.add_widget(body)

        return card

    def _render_results(self, inputs, swim, tackle, predictions, advice):
        box = self.results_screen.ids.results_box
        box.clear_widgets()

        box.add_widget(self._make_card("Swim Analysis", [
            ("Estimated water depth", f"{swim['depth_m']} m"),
            ("Suggested casting distance", f"{swim['casting_distance_m']} m"),
            ("Likely feeding areas", "; ".join(swim['feeding_areas'])),
            ("Recommended zone", swim['zone_recommendation']),
            ("Snag risk", swim['snag_risk']),
            ("Confidence score", f"{swim['confidence_pct']}%"),
        ]))

        box.add_widget(self._make_card("Tackle Recommendation", [
            ("Rod type", tackle['rod_type']),
            ("Rod length", f"{tackle['rod_length_ft']} ft"),
            ("Reel size", tackle['reel_size']),
            ("Main line", tackle['mainline']),
            ("Hooklength", tackle['hooklength']),
            ("Hook size", tackle['hook_size']),
            ("Method", tackle['method']),
            ("Feeder weight", tackle['feeder_weight']),
            ("Lead size", tackle['lead_size']),
            ("Recommended bait", tackle['bait']),
            ("Groundbait", tackle['groundbait']),
            ("Loose feed", tackle['loose_feed']),
        ]))

        sorted_predictions = sorted(predictions.items(), key=lambda kv: kv[1], reverse=True)
        box.add_widget(self._make_card("Fish Prediction", [
            (species, f"{pct}%") for species, pct in sorted_predictions
        ]))

        box.add_widget(self._make_advice_card(advice))


if __name__ == '__main__':
    SwimFinderApp().run()
