import qrcode
from io import BytesIO
from kivy.core.image import Image as CoreImage


def generate_qr_texture(content, size=240):
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return CoreImage(buffer, ext="png")
