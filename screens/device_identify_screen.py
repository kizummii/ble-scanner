from kivy.clock import Clock
from kivy.app import App
from kivymd.uix.screen import MDScreen
from app.config import QR_ADV_DATA_TEMPLATE
from services.qr_service import generate_qr_texture
from services.flag_generator import generate_ble_flag


class DeviceIdentifyScreen(MDScreen):
    def on_enter(self):
        app = App.get_running_app()
        self.ble_flag = generate_ble_flag()
        app.current_ble_flag = self.ble_flag

        Clock.schedule_once(self._setup_qr, 0.1)

    def _setup_qr(self, dt):
        content = QR_ADV_DATA_TEMPLATE.format(self.ble_flag)
        texture = generate_qr_texture(content)
        self.ids.qr_image.texture = texture.texture
        self.ids.tv_flag.text = self.ble_flag

    def on_connect(self):
        from jnius import autoclass

        BluetoothAdapter = autoclass("android.bluetooth.BluetoothAdapter")
        adapter = BluetoothAdapter.getDefaultAdapter()

        if adapter and adapter.isEnabled():
            self.manager.current = "ble_scan"
        else:
            activity = autoclass("org.kivy.android.PythonActivity").mActivity
            intent = autoclass("android.content.Intent")(
                BluetoothAdapter.ACTION_REQUEST_ENABLE
            )
            activity.startActivity(intent)
            # Navigate after user enables BT (simplified: assume they did)
            self.manager.current = "ble_scan"
