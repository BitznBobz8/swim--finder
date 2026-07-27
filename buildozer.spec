[app]

# (str) Title of your application
title = Swim Finder AI

# (str) Package name (no spaces, used internally by Android)
package.name = swimfinderai

# (str) Package domain (reverse-DNS style, unique to your app - change
# the "swimfinder" part if you ever plan to publish to the Play Store,
# but any value works fine for a personal/sideloaded install)
package.domain = org.swimfinder

# (str) Source code where main.py lives
source.dir = .

# (list) File types to include from source.dir
source.include_exts = py,kv,png,jpg,jpeg,atlas

# (str) Version of your application
version = 0.1

# (list) Application requirements — python3 + kivy is all V1 needs.
# When V2 adds live GPS/weather this list will grow (e.g. plyer, requests).
requirements = python3,kivy==2.3.1

# (str) Icon of the application (optional - add a 512x512 png later and
# uncomment this line to give the app a custom home-screen icon)
#icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation: landscape, sensorLandscape, portrait or all
orientation = portrait

# (bool) Fullscreen (0 = keep the Android status bar visible)
fullscreen = 0

# (list) Android permissions. Empty for V1 (no network/GPS calls yet).
# V2 will need: android.permissions = INTERNET, ACCESS_FINE_LOCATION
android.permissions =

# (int) Target Android API - should be as high as practical
android.api = 33

# (int) Minimum Android API the APK will install on (24 = Android 7.0+,
# covers the vast majority of phones in use)
android.minapi = 24

# (list) Android CPU architectures to build for. These two cover
# effectively all Android phones from the last several years.
android.archs = arm64-v8a, armeabi-v7a

# (bool) Whether the app can be backed up via Android's auto-backup
android.allow_backup = 1

# (bool) Automatically accept the Android SDK license. Required for
# non-interactive builds (like GitHub Actions) - there's no terminal
# for a human to type "y" at the license prompt, so without this the
# build just hangs/fails waiting for an answer that never comes.
android.accept_sdk_license = 1

[buildozer]

# (int) Log level: 0 = error only, 1 = info, 2 = debug (verbose is
# helpful the first time you build, in case something fails)
log_level = 2

# (int) Warn if buildozer is run as root (leave as-is)
warn_on_root = 1
