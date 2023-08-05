from datetime import datetime
from typing import NamedTuple, List, Any, Optional
from uuid import UUID


class DataGatewayResponseModel(NamedTuple):
    """
    Gateway

    Parameters:
        name (str): name of input system
    """
    name: str


class NetworkResponseModel(NamedTuple):
    """
    Internal network

    Parameters:
        data_gateway: [DataGatewayResponseModel](DataGatewayResponseModel.md)
        name (str): network's name
        type_network (str): type of network, can be output or input
    """
    data_gateway: DataGatewayResponseModel
    name: str
    type_network: str


class ProtokolResponseModel(NamedTuple):
    """
    Protocol's name

    Parameters:
        name (str): protocol's name
    """
    name: str


class DataGatewayNetworkResponseModel(NamedTuple):
    """
    Gateway

    Parameters:
        network: [NetworkResponseModel](NetworkResponseModel.md)
        protocol: [ProtokolResponseModel](ProtokolResponseModel.md)
        mac (int): unique identifier of the device in the network
    """
    network: NetworkResponseModel
    protocol: ProtokolResponseModel
    mac: int


class DeviceMeterResponseModel(NamedTuple):
    """
    Device meter information

    Parameters:
        last_value (float): last counter value (cubic meter(m3))
        last_value_date (datetime): date of last receipt of readings (datetime)
        unit_multiplier (float): recalculates measurements (between database and user)
        value_multiplier (float): recalculates measurements (between meter and database)
    """
    last_value: Optional[float]
    last_value_date: Optional[datetime]
    unit_multiplier: float
    value_multiplier: float


class DeviceChannelResponseModel(NamedTuple):
    """
    Device channel information

    Parameters:
        inactivity_limit (int): idle time to create a non-arrival data event (second)
        last_date_event_no_data (datetime): last date of non-arrival event
        serial_number (int): channel serial number (1,2,3,4,5)
    """
    inactivity_limit: int
    last_date_event_no_data: Optional[datetime]
    serial_number: int
    device_meters: List[DeviceMeterResponseModel]


class DeviceManufacturerResponseModel(NamedTuple):
    """
    The manufacturer's name

    Parameters:
        name (str): manufacturer's name
    """
    name: str


class DeviceMeteringType(NamedTuple):
    """
    Type of measuring system (gas, water)

    Parameters:
        name_ru (str): name of the measuring system in Russian/English (for the user)
        name_en (str): name of the measuring system in Russian/English (for the user)
        sys_name (str): name of the measuring system in the system (code)
    """
    name_en: str
    name_ru: str
    sys_name: str


class DeviceModificationTypeResponseModel(NamedTuple):
    """
    Device model

    Parameters:
        device_metering_type: [DeviceMeteringType](DeviceMeteringType.md)
        name_ru_en (str): name of the device model in Russian/English (for the user)
        sys_name (str): name of the device model in the system (code)
        type (str): smart_meter/modem
    """
    device_metering_type: DeviceMeteringType
    name_en: str
    name_ru: str
    sys_name: str
    type: str


class DeviceModificationResponseModel(NamedTuple):
    """
    Device modification

    Parameters:
        device_modification_type: [DeviceModificationTypeResponseModel](DeviceModificationTypeResponseModel.md)
        name (str): device modification's name
    """
    device_modification_type: DeviceModificationTypeResponseModel
    name: str


class GetDeviceListInfoPayloadResponse(NamedTuple):
    """
    Device information

    Parameters:
        data_gateway_network_device: [DataGatewayNetworkResponseModel](DataGatewayNetworkResponseModel.md)
        device_channel (list): [DeviceChannelResponseModel](DeviceChannelResponseModel.md)
        device_manufacturer: [DeviceManufacturerResponseModel](DeviceManufacturerResponseModel.md)
        device_modification: [DeviceModificationResponseModel](DeviceModificationResponseModel.md)
        date_produced (datetime): date of manufacture of the device
        firmware_version (str): software version
        hardware_version (str): hardware version
        id (UUID): system identifier
        manufacturer_serial_number (str): manufacturer-serial number
    """
    data_gateway_network_device: DataGatewayNetworkResponseModel
    device_channel: List[DeviceChannelResponseModel]
    device_manufacturer: DeviceManufacturerResponseModel
    device_modification: DeviceModificationResponseModel
    date_produced: datetime
    firmware_version: Optional[str]
    hardware_version: Optional[str]
    id: UUID
    manufacturer_serial_number: str


class GetDeviceListInfoResponse(NamedTuple):
    """
    Device information list

    Parameters:
        count (int): object's limit count
        errors (any): presence of errors
        ok (bool): validity
        total_count (int): object's total count
        payload (list): [GetDeviceListInfoPayloadResponse](GetDeviceListInfoPayloadResponse.md)
    """
    count: int
    errors: List[Any]
    ok: bool
    total_count: int
    payload: List[GetDeviceListInfoPayloadResponse]


class GetDeviceInfoResponse(NamedTuple):
    """
    Device information list

    Parameters:
        errors (any): presence of errors
        ok (bool): successful request
        payload: [GetDeviceListInfoPayloadResponse](GetDeviceListInfoPayloadResponse.md)
    """
    errors: List[Any]
    ok: bool
    payload: GetDeviceListInfoPayloadResponse


class GetDeviceChannelValuePayloadResponse(NamedTuple):  #
    """
    Device channel values

    Parameters:
        channel_number (int): channel number
        date (datetime): date and time of receipt
        date_created (datetime): date and time the entry was created
        device_id (UUID): unique device identifier in the system
        value (float): product of value_raw and value_multiplier (recalculated values)
        value_raw (float): initial value
        value_type (str): device_data(meter reading), interpolated_linear(interpolated reading)
    """
    channel_number: int
    date: datetime
    date_created: datetime
    device_id: UUID
    value: Optional[float]
    value_raw: Optional[float]
    value_type: str


class GetDeviceValueResponse(NamedTuple):
    """
    Device channel information list

   Parameters:
        count (int): object's limit count
        errors (any): presence of errors
        ok (bool): validity
        total_count (int): object's total count
        payload (list): [GetDeviceChannelValuePayloadResponse](GetDeviceChannelValuePayloadResponse.md)
    """
    count: int
    errors: List[Any]
    ok: bool
    total_count: int
    payload: List[GetDeviceChannelValuePayloadResponse]
