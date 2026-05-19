from kivy.clock import Clock
from kivy.uix.image import Image as KivyImage
from kivymd.uix.screen import MDScreen
from app.config import QR_MODE_SWITCH
from services.qr_service import generate_qr_texture
from utils.android_perms import check_and_request_permissions


class ModeSelectScreen(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self._setup_qr, 0.1)

    def _setup_qr(self, dt):
        texture = generate_qr_texture(QR_MODE_SWITCH)
        qr_widget = self.ids.qr_image
        qr_widget.texture = texture.texture

    def on_continue(self):
        perms_ok = check_and_request_permissions()
        if perms_ok:
            self.manager.current = "device_identify"
