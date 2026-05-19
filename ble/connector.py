from jnius import autoclass
from app.config import SERVICE_UUID, WRITE_NOTIFY_UUID, CCCD_UUID
from ble.callback import GattCallbackBridge


class GattEventListener:
    """Override methods to receive GATT events."""

    def on_connected(self, mac, status):
        pass

    def on_disconnected(self, mac, status):
        pass

    def on_services_discovered(self, mac, services, success):
        pass

    def on_data_received(self, mac, value_bytes):
        pass

    def on_characteristic_write(self, mac, value_bytes, status):
        pass

    def on_characteristic_read(self, mac, value_bytes, status):
        pass

    def on_descriptor_write(self, status):
        pass


class BleConnector:
    def __init__(self, mac_address):
        self.PythonActivity = autoclass("org.kivy.android.PythonActivity")
        self.activity = self.PythonActivity.mActivity
        BluetoothManager = autoclass("android.bluetooth.BluetoothManager")
        self.bluetooth_manager = self.activity.getSystemService("bluetooth")
        self.bluetooth_adapter = self.bluetooth_manager.getAdapter()
        BluetoothDevice = autoclass("android.bluetooth.BluetoothDevice")
        self.device = self.bluetooth_adapter.getRemoteDevice(mac_address.upper())
        self.gatt = None
        self._gatt_callback = None
        self._listener = None
        self.connected = False

    def connect(self, listener=None):
        self._listener = listener or GattEventListener()
        self._gatt_callback = GattCallbackBridge(self._listener)
        Context = autoclass("android.content.Context")
        self.gatt = self.device.connectGatt(
            self.activity, False, self._gatt_callback
        )

    def disconnect(self):
        if self.gatt:
            try:
                self.gatt.disconnect()
            except Exception:
                pass
            try:
                self.gatt.close()
            except Exception:
                pass
            self.connected = False

    def enable_notification(self, service_uuid=None, char_uuid=None):
        if not self.gatt:
            return False
        UUID = autoclass("java.util.UUID")
        service = self.gatt.getService(
            UUID.fromString(service_uuid or SERVICE_UUID)
        )
        if not service:
            return False
        characteristic = service.getCharacteristic(
            UUID.fromString(char_uuid or WRITE_NOTIFY_UUID)
        )
        if not characteristic:
            return False

        self.gatt.setCharacteristicNotification(characteristic, True)

        BluetoothGattDescriptor = autoclass(
            "android.bluetooth.BluetoothGattDescriptor"
        )
        descriptor = characteristic.getDescriptor(
            UUID.fromString(CCCD_UUID)
        )
        if descriptor:
            descriptor.setValue(
                BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
            )
            self.gatt.writeDescriptor(descriptor)
        return True

    def write_characteristic(self, data_bytes, service_uuid=None, char_uuid=None):
        if not self.gatt:
            return False
        UUID = autoclass("java.util.UUID")
        service = self.gatt.getService(
            UUID.fromString(service_uuid or SERVICE_UUID)
        )
        if not service:
            return False
        characteristic = service.getCharacteristic(
            UUID.fromString(char_uuid or WRITE_NOTIFY_UUID)
        )
        if not characteristic:
            return False
        characteristic.setValue(data_bytes)
        characteristic.setWriteType(1)  # WRITE_TYPE_DEFAULT
        return self.gatt.writeCharacteristic(characteristic)

    def send_at_command(self, command_str):
        return self.write_characteristic(command_str.encode("utf-8"))
