from jnius import autoclass, PythonJavaClass, java_method
from ble.callback import ScanCallbackBridge


class BleScanner:
    def __init__(self):
        self.PythonActivity = autoclass("org.kivy.android.PythonActivity")
        self.activity = self.PythonActivity.mActivity
        BluetoothManager = autoclass("android.bluetooth.BluetoothManager")
        self.bluetooth_manager = self.activity.getSystemService("bluetooth")
        self.bluetooth_adapter = self.bluetooth_manager.getAdapter()
        self.bluetooth_le_scanner = self.bluetooth_adapter.getBluetoothLeScanner()
        self._scan_callback = None
        self._handler = None
        self._scan_stop = None
        self.is_scanning = False

    def start_scan(self, filters, on_result, period_ms=10000):
        if self.is_scanning:
            self.stop_scan()

        self._scan_callback = ScanCallbackBridge(on_result)
        ScanSettingsBuilder = autoclass("android.bluetooth.le.ScanSettings$Builder")
        settings = ScanSettingsBuilder().setScanMode(1).build()

        filter_list = None
        if filters:
            ArrayList = autoclass("java.util.ArrayList")
            filter_list = ArrayList()
            for f in filters:
                filter_list.add(f)

        self.bluetooth_le_scanner.startScan(filter_list, settings, self._scan_callback)
        self.is_scanning = True

        # Auto-stop after period
        Looper = autoclass("android.os.Looper")
        self._handler = autoclass("android.os.Handler")(Looper.getMainLooper())
        self._scan_stop = Runnable(self.stop_scan)
        self._handler.postDelayed(self._scan_stop, period_ms)

    def stop_scan(self):
        if self.is_scanning and self._scan_callback:
            try:
                self.bluetooth_le_scanner.stopScan(self._scan_callback)
            except Exception:
                pass
            self.is_scanning = False
        if self._handler and self._scan_stop:
            self._handler.removeCallbacks(self._scan_stop)

    def build_filter(self, service_uuid=None, device_name=None):
        ScanFilterBuilder = autoclass("android.bluetooth.le.ScanFilter$Builder")
        builder = ScanFilterBuilder()
        if service_uuid:
            ParcelUuid = autoclass("android.os.ParcelUuid")
            UUID = autoclass("java.util.UUID")
            builder.setServiceUuid(ParcelUuid(UUID.fromString(service_uuid)))
        if device_name:
            builder.setDeviceName(device_name)
        return builder.build()

    def is_bluetooth_enabled(self):
        return self.bluetooth_adapter.isEnabled()


class Runnable(PythonJavaClass):
    __javainterfaces__ = ["java/lang/Runnable"]

    def __init__(self, func):
        super().__init__()
        self.func = func

    @java_method("()V")
    def run(self):
        self.func()
