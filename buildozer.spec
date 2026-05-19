[app]
title = BLE Scanner
package.name = blescanner
package.domain = com.yunmai.scanner
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0.0
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pyjnius,qrcode,Pillow,android
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.2.0
fullscreen = 1

# Permissions
android.permissions = ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, BLUETOOTH, BLUETOOTH_ADMIN, BLUETOOTH_SCAN, BLUETOOTH_CONNECT
android.api = 33
android.minapi = 21
android.ndk = 27c
android.build_tools = 33.0.2
android.accept_sdk_license = True
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/27.3.13750724
android.gradle_dependencies =
android.add_src =

# BLE feature requirement
android.manifest = <uses-feature android:name="android.hardware.bluetooth_le" android:required="true" />

# Signing (optional — use your own keystore for release)
android.keystore =
android.keystore.password =
android.keyalias =
android.keyalias.password =

# Presplash and icon
presplash.filename =
icon.filename =

[buildozer]
log_level = 2
warn_on_root = 1
