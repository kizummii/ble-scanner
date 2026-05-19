# BLE GAP Advertisement Data Type constants
AD_TYPE_FLAGS = 0x01
AD_TYPE_16BIT_SERVICE_UUID_PARTIAL = 0x02
AD_TYPE_16BIT_SERVICE_UUID_COMPLETE = 0x03
AD_TYPE_32BIT_SERVICE_UUID_PARTIAL = 0x04
AD_TYPE_32BIT_SERVICE_UUID_COMPLETE = 0x05
AD_TYPE_128BIT_SERVICE_UUID_PARTIAL = 0x06
AD_TYPE_128BIT_SERVICE_UUID_COMPLETE = 0x07
AD_TYPE_COMPLETE_LOCAL_NAME = 0x09
AD_TYPE_TX_POWER_LEVEL = 0x0A
AD_TYPE_MANUFACTURER_SPECIFIC_DATA = 0xFF


def adv_report_parse(data_type, adv_data):
    """Parse BLE advertisement data by AD type."""
    if not adv_data:
        return None
    index = 0
    length = len(adv_data)
    while index < length:
        try:
            field_length = adv_data[index]
            if field_length == 0:
                break
            field_type = adv_data[index + 1]
        except IndexError:
            return None
        if field_type == data_type:
            data_len = field_length - 1
            return adv_data[index + 2 : index + 2 + data_len]
        index += field_length + 1
        if index >= length:
            break
    return None


def get_custom_data(adv_data):
    """Extract manufacturer-specific data (AD type 0xFF) as hex string."""
    data = adv_report_parse(AD_TYPE_MANUFACTURER_SPECIFIC_DATA, adv_data)
    if data:
        return "".join(f"{b:02X}" for b in data)
    return None


def get_local_name(adv_data):
    """Extract complete local name from advertisement data."""
    data = adv_report_parse(AD_TYPE_COMPLETE_LOCAL_NAME, adv_data)
    if data:
        try:
            return data.decode("utf-8", errors="replace")
        except Exception:
            return None
    return None


def get_16bit_service_uuids(adv_data):
    """Extract 16-bit service UUIDs from advertisement data."""
    data = adv_report_parse(AD_TYPE_16BIT_SERVICE_UUID_COMPLETE, adv_data)
    if not data:
        data = adv_report_parse(AD_TYPE_16BIT_SERVICE_UUID_PARTIAL, adv_data)
    if not data:
        return []
    uuids = []
    for i in range(0, len(data), 2):
        uuid_hex = f"{data[i+1]:02X}{data[i]:02X}"
        uuids.append(uuid_hex)
    return uuids
