def check_and_request_permissions():
    """Check and request Android BLE permissions.
    Returns True if permissions already granted, False if request was initiated.
    """
    try:
        from jnius import autoclass

        Build = autoclass("android.os.Build")
        Manifest = autoclass("android.Manifest")
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        activity = PythonActivity.mActivity
        ActivityCompat = autoclass(
            "androidx.core.app.ActivityCompat"
        )

        permissions = []

        # Android 12+ (API 31) needs BLUETOOTH_SCAN and BLUETOOTH_CONNECT
        if Build.VERSION.SDK_INT >= 31:
            permissions.append(Manifest.permission.BLUETOOTH_SCAN)
            permissions.append(Manifest.permission.BLUETOOTH_CONNECT)
        else:
            permissions.append(Manifest.permission.BLUETOOTH)
            permissions.append(Manifest.permission.BLUETOOTH_ADMIN)

        permissions.append(Manifest.permission.ACCESS_FINE_LOCATION)
        permissions.append(Manifest.permission.ACCESS_COARSE_LOCATION)

        # Check which ones are not granted
        missing = []
        for perm in permissions:
            if ActivityCompat.checkSelfPermission(activity, perm) != 0:
                missing.append(perm)

        if missing:
            ActivityCompat.requestPermissions(
                activity, missing, 1001
            )
            return False

        return True

    except Exception:
        # Not on Android (desktop development)
        return True
