# Unicboard billing api is available on PyPI:

## Requires:

Python >=3.6

## install:

python -m pip install unicboard_billing_sdk

## usage:

```python
from unicboard_billing_sdk import BillingApiSdk

Api = BillingApiSdk(
    api_billing_url="unicboard url",
    api_token="yours token",
) 
```
### get list devices
```python
devices = Api.get_device_list_info() # default limit = 1000

devices = Api.get_device_list_info(limit: int, offset: int) #  for custom limit/offset

list_device_id = [device.id for device in devices] 
list_device_mac = [device.data_gateway_network_device.mac for device in devices]
```

### get device by device_id
```python
device = Api.get_device_info(UUID(device_id))
```

### get device by device_id
```python
devices_values = Api.get_device_value(
    devices_id=list_device_id,
    period_from: datetime,
    period_to: Optional[datetime],  # default now
)
```
