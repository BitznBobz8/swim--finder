[app]

# (str) Title of your application
title = Swim Finder AI

# (str) Package name (no spaces, used internally by Android)
package.name = swimfinderai

# (str) Package domain (reverse-DNS style, unique to your app)
package.domain = org.swimfinder

# (str) Source code where main.py lives
source.dir = .

# (list) File types to include from source.dir
source.include_exts = py,kv,png,jpg,jpeg,atlas

# (str) Version of your application
version = 0.1

# (list) Application requirements — includes kivy, plyer for GPS, kivy_garden.mapview for maps, and build tools
requirements = hostpython3,python3,kivy==2.3.1,plyer,kivy_garden.mapview,requests,urllib3,certifi,idna,chardet,openssl

# (str) Icon of the application (optional - add a 512x512 png later)
#icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation: landscape, sensorLandscape, portrait or all
orientation = portrait

# (bool) Fullscreen (0 = keep the Android status bar visible)
fullscreen = 0

# (list) Android permissions. Needs INTERNET and location permissions for GPS.
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION

# (int) Target Android API
android.api = 33

# (int) Minimum Android API the APK will install on
android.minapi = 24

# (list) Android CPU architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Whether the app can be backed up via Android's auto-backup
android.allow_backup = 1

# (bool) Automatically accept the Android SDK license
android.accept_sdk_license = 1

[buildozer]

# (int) Log level: 0 = error only, 1 = info, 2 = debug
log_level = 2

# (int) Warn if buildozer is run as root
warn_on_root = 1
