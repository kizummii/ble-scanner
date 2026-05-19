from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from screens.mode_select_screen import ModeSelectScreen
from screens.device_identify_screen import DeviceIdentifyScreen
from screens.ble_scan_screen import BleScanScreen


class BleScannerApp(MDApp):
    current_ble_flag = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.material_style = "M3"

        Builder.load_file("screens/screens.kv")

        sm = ScreenManager()
        sm.add_widget(ModeSelectScreen(name="mode_select"))
        sm.add_widget(DeviceIdentifyScreen(name="device_identify"))
        sm.add_widget(BleScanScreen(name="ble_scan"))

        return sm
