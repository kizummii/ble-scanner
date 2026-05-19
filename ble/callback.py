from jnius import PythonJavaClass, java_method, autoclass


class ScanCallbackBridge(PythonJavaClass):
    __javainterfaces__ = ["android/bluetooth/le/ScanCallback"]

    def __init__(self, on_result_cb, on_failed_cb=None):
        super().__init__()
        self._on_result = on_result_cb
        self._on_failed = on_failed_cb

    @java_method("(ILandroid/bluetooth/le/ScanResult;)V")
    def onScanResult(self, callbackType, result):
        if self._on_result:
            self._on_result(callbackType, result)

    @java_method("(I)V")
    def onScanFailed(self, errorCode):
        if self._on_failed:
            self._on_failed(errorCode)


class GattCallbackBridge(PythonJavaClass):
    __javainterfaces__ = ["android/bluetooth/BluetoothGattCallback"]

    def __init__(self, listener):
        super().__init__()
        self.listener = listener

    @java_method("(Landroid/bluetooth/BluetoothGatt;II)V")
    def onConnectionStateChange(self, gatt, status, newState):
        BluetoothProfile = autoclass("android.bluetooth.BluetoothProfile")
        mac = gatt.getDevice().getAddress()
        if newState == BluetoothProfile.STATE_CONNECTED:
            self.listener.on_connected(mac, status)
            gatt.discoverServices()
        elif newState == BluetoothProfile.STATE_DISCONNECTED:
            self.listener.on_disconnected(mac, status)

    @java_method("(Landroid/bluetooth/BluetoothGatt;I)V")
    def onServicesDiscovered(self, gatt, status):
        BluetoothGatt = autoclass("android.bluetooth.BluetoothGatt")
        mac = gatt.getDevice().getAddress()
        success = status == BluetoothGatt.GATT_SUCCESS
        self.listener.on_services_discovered(mac, gatt.getServices(), success)

    @java_method(
        "(Landroid/bluetooth/BluetoothGatt;"
        "Landroid/bluetooth/BluetoothGattCharacteristic;)V"
    )
    def onCharacteristicChanged(self, gatt, characteristic):
        mac = gatt.getDevice().getAddress()
        value = characteristic.getValue()
        self.listener.on_data_received(mac, bytearray(value) if value else b"")

    @java_method(
        "(Landroid/bluetooth/BluetoothGatt;"
        "Landroid/bluetooth/BluetoothGattCharacteristic;I)V"
    )
    def onCharacteristicWrite(self, gatt, characteristic, status):
        mac = gatt.getDevice().getAddress()
        value = characteristic.getValue()
        self.listener.on_characteristic_write(
            mac, bytearray(value) if value else b"", status
        )

    @java_method(
        "(Landroid/bluetooth/BluetoothGatt;"
        "Landroid/bluetooth/BluetoothGattCharacteristic;I)V"
    )
    def onCharacteristicRead(self, gatt, characteristic, status):
        mac = gatt.getDevice().getAddress()
        value = characteristic.getValue()
        self.listener.on_characteristic_read(
            mac, bytearray(value) if value else b"", status
        )

    @java_method("(Landroid/bluetooth/BluetoothGatt;Landroid/bluetooth/BluetoothGattDescriptor;I)V")
    def onDescriptorWrite(self, gatt, descriptor, status):
        self.listener.on_descriptor_write(status)
