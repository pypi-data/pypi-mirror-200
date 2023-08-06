# CSOB client
Python library for communicating with ČSOB (<https://platbakartou.csob.cz/>) payment gateway API. The API is described here: <https://github.com/csob/paymentgateway>.

The library focuses on the v.1.9 but it is designed for extensibility.


## Installation
```bash
pip install csobclient
```

## Basic usage

### Client initialization
```python
from csobclient import Client

client = Client("merchantId", "merch_private.key", "csob.pub")
```

### Payment initialization
```python
from csobclient import Cart, CartItem

response = client.init_payment(
    order_no="2233823251",
    total_amount=100,
    return_url="http://127.0.0.1:5000/",
    cart=Cart([CartItem("Apples", 1, 100)]),
    merchant_data=b"Hello, World!",
)
```

### Get payment URL
```python
url = client.get_payment_process_url(pay_id)
```

### Process the gateway redirect
```python
payment_info = client.process_gateway_return(data_dict)
```

### Get payment status
```python
payment_info = client.get_payment_status(pay_id)
```

### Reverse payment
```python
response = client.reverse_payment(pay_id)
```

### Exceptions handling
```python
from csobclient import APIError, HTTPRequestError

try:
    client.operation(...)
except APIError as exc:
    # handle API error
except HTTPRequestError as exc:
    # handle HTTP error
```

### RSA keys management
The simples way to pass RSA keys is to pass their file paths:

```python
from csobclient import Client

client = Client("merchantId", "merch_private.key", "csob.pub")
```

The library will read the private key from the file when needed. The public key will be cached into the RAM.

If you want to change it, use special classes:

```python
from csobclient import Client, FileRSAKey, CachedRSAKey

client = Client("merchantId", FileRSAKey("merch_private.key"), FileRSAKey("csob.pub"))
```

You may also override the base RSAKey class to define your own key access strategy:

```python
from csobclient import RSAKey

class MyRSAKey(RSAKey):

    def __str__(self) -> str:
        return "my key"
```
