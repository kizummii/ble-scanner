from kivy.clock import Clock
from kivy.app import App
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivymd.uix.screen import MDScreen
from app.config import SERVICE_UUID, DEVICE_NAME, SCAN_PERIOD_MS
from app.config import AT_VIBRATE_ON, AT_VIBRATE_OFF, AT_BUZZER_ON, AT_BUZZER_OFF
from ble.scanner import BleScanner
from ble.connector import BleConnector, GattEventListener
from ble.broadcast_parser import get_custom_data
from utils.byte_utils import to_string


class _GattHandler(GattEventListener):
    """Bridges GATT callbacks to the Kivy main thread."""

    def __init__(self, screen):
        self.screen = screen

    def on_connected(self, mac, status):
        Clock.schedule_once(lambda dt: self.screen._on_connected(mac, status))

    def on_disconnected(self, mac, status):
        Clock.schedule_once(lambda dt: self.screen._on_disconnected(mac, status))

    def on_services_discovered(self, mac, services, success):
        Clock.schedule_once(
            lambda dt: self.screen._on_services(mac, services, success)
        )

    def on_data_received(self, mac, value_bytes):
        Clock.schedule_once(
            lambda dt: self.screen._on_data(mac, value_bytes)
        )

    def on_characteristic_write(self, mac, value_bytes, status):
        Clock.schedule_once(
            lambda dt: self.screen._on_write_result(mac, value_bytes, status)
        )


class BleScanScreen(MDScreen):
    device_name = StringProperty("---")
    device_mac = StringProperty("---")
    device_rssi = StringProperty("---")
    connection_status = StringProperty("设备连接中")  # 设备连接中
    scan_data = ListProperty([])
    btn_conn_enabled = BooleanProperty(False)
    btn_disconn_enabled = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scanner = None
        self.connector = None
        self._gatt_handler = _GattHandler(self)
        self._ble_flag = None

    def on_enter(self):
        app = App.get_running_app()
        self._ble_flag = app.current_ble_flag
        self.scan_data = []
        self.connection_status = "扫描中..."  # 扫描中...
        self.btn_conn_enabled = False
        self.btn_disconn_enabled = False

        Clock.schedule_once(self._start_scan, 0.3)

    def _start_scan(self, dt):
        self.scanner = BleScanner()

        scan_filter = self.scanner.build_filter(
            service_uuid=SERVICE_UUID, device_name=DEVICE_NAME
        )

        self.scanner.start_scan(
            filters=[scan_filter],
            on_result=self._on_scan_result,
            period_ms=SCAN_PERIOD_MS,
        )

    def _on_scan_result(self, callback_type, scan_result):
        device = scan_result.getDevice()
        address = device.getAddress()
        name = device.getName()

        scan_record = scan_result.getScanRecord()
        if not scan_record:
            return

        adv_bytes = scan_record.getBytes()
        if not adv_bytes:
            return

        custom_data = get_custom_data(bytearray(adv_bytes))
        if custom_data and custom_data == self._ble_flag:
            self.device_name = name or "LYM"
            self.device_mac = address
            self.device_rssi = str(scan_result.getRssi())
            self._auto_connect()

    def _auto_connect(self):
        if self.scanner:
            self.scanner.stop_scan()
            self.scanner = None

        self.connection_status = "连接中..."  # 连接中...
        self.connector = BleConnector(self.device_mac)
        self.connector.connect(self._gatt_handler)

    def _on_connected(self, mac, status):
        self.connection_status = "已连接"  # 已连接
        self.connected = True
        self.btn_conn_enabled = False
        self.btn_disconn_enabled = True

    def _on_disconnected(self, mac, status):
        self.connection_status = "已断开"  # 已断开
        self.connected = False
        self.btn_conn_enabled = True
        self.btn_disconn_enabled = False

    def _on_services(self, mac, services, success):
        if success and self.connector:
            self.connector.enable_notification()

    def _on_data(self, mac, value_bytes):
        text = to_string(value_bytes)
        if text:
            self.scan_data.append(text)

    def _on_write_result(self, mac, value_bytes, status):
        pass  # Write confirmed

    def send_at_command(self, command):
        if self.connector:
            self.connector.send_at_command(command)

    def on_connect_click(self):
        if self.connector and not self.connected:
            self.connector.connect(self._gatt_handler)

    def on_disconnect_click(self):
        if self.connector:
            self.connector.disconnect()

    def on_back(self):
        if self.scanner:
            self.scanner.stop_scan()
        if self.connector:
            self.connector.disconnect()
        self.manager.current = "device_identify"

    def on_leave(self):
        if self.scanner:
            self.scanner.stop_scan()
            self.scanner = None
